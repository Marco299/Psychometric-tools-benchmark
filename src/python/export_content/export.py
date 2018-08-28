import logging
import re
import sys
import os
from datetime import datetime
from itertools import groupby

from bs4 import BeautifulSoup as BS4
from sqlalchemy import or_, and_
from sqlalchemy import orm

from commons.aliasing import load_alias_map, get_alias_ids
from db.setup import SessionWrapper
from logger import logging_config

from export_content.orm.tables import *

from rpy2.robjects.packages import importr
import rpy2.robjects as robjects


def training_nlon():
    nlon = importr('NLoN')
    robjects.r['load']("training_data.rda")

    return nlon, nlon.NLoNModel(robjects.r['text'], robjects.r['rater'])


def clean_up(message_bodies, nlon, nlon_model):
    cleansed = list()
    words_number = 0
    words_limit = 10000
    for message_body in message_bodies:
        try:
            soup = BS4(message_body, 'html.parser')
            clean_message_body = soup.text
        except Exception as e:
            logger.error('Error with BS4 on text:\n\n%s\n\n' % message_body, str(e))
            clean_message_body = message_body.strip()

        clean_message_body = re.sub(r'^\s*>+( .*)?', '', clean_message_body, flags=re.MULTILINE)
        clean_message_body = re.sub(r'^\s*\+', '', clean_message_body, flags=re.MULTILINE)
        clean_message_body = re.sub(r'^\s*---\+', '', clean_message_body, flags=re.MULTILINE)
        clean_message_body = re.sub(r'\n[\t\s]*\n+', '', clean_message_body, flags=re.MULTILINE)
        clean_message_body = re.sub(r'({+|}+|\++|_+|=+|-+|\*|\\+|/+|@+|\[+|\]+|:+|<+|>+|\(+|\)+)', '',
                                    clean_message_body, flags=re.MULTILINE)
        clean_message_body = re.sub(r'On\s(.[^\sw]*\s)*wrote', '', clean_message_body, flags=re.MULTILINE)
        clean_message_body = re.sub(r'[\n+]Sent from', '', clean_message_body, flags=re.MULTILINE)
        clean_message_body = re.sub(r'https?:\/\/\S*', '', clean_message_body, flags=re.MULTILINE)
        clean_message_body = re.sub(r'[\w\.-]+ @ [\w\.-]+', '', clean_message_body, flags=re.MULTILINE)
        # clean_message_body = clean_message_body.encode('utf-8').strip()

        message_by_lines = clean_message_body.splitlines()
        list_length = len(message_by_lines)
        index = 0
        for count in range(0, list_length):
            text = robjects.StrVector([message_by_lines[index]])
            if nlon.NLoNPredict(nlon_model, text)[0] == 'Not':
                del message_by_lines[index]
            else:
                index = index + 1
        clean_message_body = '\n'.join(message_by_lines)

        split_message = clean_message_body.split()
        words_number += len(split_message)
        if words_number > words_limit:
            split_message = split_message[:(words_limit - words_number)]
            clean_message_body = ' '.join(split_message)
            cleansed.append(clean_message_body.strip())
            break
        cleansed.append(clean_message_body.strip())
    return cleansed


def get_alias_email_addresses(alias_ids):
    alias_email_addresses = set()

    for alias_id in alias_ids:
        if alias_id > 0:
            if alias_id < OFFSET:
                # from GithubDeveloper - local_developers
                try:
                    res = session.query(GithubDeveloper.email).filter_by(id=alias_id).one()
                    alias_email_addresses.add(res.email)
                except (orm.exc.NoResultFound, orm.exc.MultipleResultsFound):
                    continue
            else:  # from MailingListSenderId - people_id
                try:
                    res = session.query(MailingListSenderId.email_address).filter_by(id=alias_id).one()
                    alias_email_addresses.add(res.email_address)
                except (orm.exc.NoResultFound, orm.exc.MultipleResultsFound):
                    continue

    return list(alias_email_addresses)


def get_all_emails(email_addresses, mailing_lists):
    # for address in email_addresses:
    res = session.query(MessagesPeople.message_id, Messages.subject, Messages.first_date,
                        Messages.message_body).filter_by(type_of_recipient='From',
                                                         message_id=Messages.message_id).filter(
        and_(or_(MessagesPeople.email_address == e for e in email_addresses),
             or_(Messages.mailing_list_url == ml for ml in mailing_lists))).distinct().all()
    return res


def save_on_text_file(uid, p_name, usr_emails, nlon, nlon_model):
    # sort emails by date
    usr_emails.sort(key=lambda e: e.first_date)
    # group by month
    for month, eml_list in groupby(usr_emails, key=lambda e: datetime.strftime(e.first_date, "%Y-%m")):
        logger.debug('Cleaning up email bodies')
        clean_emails = clean_up([x.message_body for x in eml_list], nlon, nlon_model)

        file = open(content_folder+'/' + str(uid) + '_' + p_name + '_' + month + '.txt', "w+")
        file.write('\n\n'.join(clean_emails))

        logger.debug('File successfully saved')

        del clean_emails


def main():
    logger.info('Training nlon model')
    nlon, nlon_model = training_nlon()

    alias_map = load_alias_map('idm/dict/alias_map.dict')

    projects = sorted(session.query(ApacheProject.name, ApacheProject.dev_ml_url, ApacheProject.user_ml_url). \
                      filter(
        and_(ApacheProject.name == GithubRepository.slug, GithubRepository.id == Commit.repo_id)).distinct().all())

    contributors = session.query(CommitHistoryDevProject).order_by(CommitHistoryDevProject.dev_uid).distinct().all()

    contributors_set = sorted(set([alias_map[x.dev_uid] for x in contributors]))

    for uid in sorted(set(alias_map.values())):
        # negative ids for ASFers
        # positive for git developers
        # positive, starts from OFFSET ids for emailers
        if uid not in contributors_set:
            logger.debug('%s did not contribute to any project\'s code base, skipping' % uid)
            continue

        aliases = sorted(get_alias_ids(alias_map, uid) + [uid, ])
        alias_email_addresses = get_alias_email_addresses(aliases)
        if not alias_email_addresses:
            logger.debug('%s has no email addresses associated, skipping' % uid)
            continue
        logger.info('Processing uid %s <%s>' % (uid, ','.join(alias_email_addresses)))

        for p in projects:
            logger.info('Processing project %s' % p.name)
            project_mailing_lists = (p.dev_ml_url[:-1], p.user_ml_url[:-1])  # remove trailing slash
            # project_mailing_lists_email_addresses = session.query(MessagesPeople.email_address).filter(
            #    or_(MessagesPeople.mailing_list_url == ml for ml in project_mailing_lists)).distinct().all()

            logger.debug('Retrieving emails from %s' % ', '.join(alias_email_addresses))
            all_emails = get_all_emails(alias_email_addresses, project_mailing_lists)
            if all_emails:
                save_on_text_file(uid, p.name, all_emails, nlon, nlon_model)
                del all_emails
            else:
                logger.debug(
                    'No emails from %s <%s> to project \'%s\' mailing lists' % (uid, alias_email_addresses, p.name))
            logger.info('Done processing project %s' % p.name)
    return False


OFFSET = 900000
if __name__ == '__main__':
    logger = logging_config.get_logger('big5_personality', console_level=logging.DEBUG)
    SessionWrapper.load_config('../db/cfg/setup.yml')
    session = SessionWrapper.new(init=True)

    content_folder = sys.path[0] + '/content'
    if not os.path.exists(content_folder):
        os.makedirs(content_folder)

    try:
        main()
    except KeyboardInterrupt:
        logger.error('Received Ctrl-C or other break signal. Exiting.')
