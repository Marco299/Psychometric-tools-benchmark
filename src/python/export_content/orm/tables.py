from sqlalchemy import BigInteger, Column, Integer, String, DateTime, ForeignKeyConstraint
from sqlalchemy import Enum, VARCHAR, ForeignKey, NUMERIC
from sqlalchemy.dialects.mysql import MEDIUMTEXT, TEXT, LONGTEXT
from unidecode import unidecode

from db.setup import Base


class ApacheProject(Base):
    __tablename__ = 'projects'
    __table_args__ = {
        'extend_existing': True,
        'mysql_row_format': 'DYNAMIC'
    }

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    status = Column(String(24))
    category = Column(String(32))
    language = Column(String(24))
    pmc_chair = Column(String(255))  # , ForeignKey("developers.name") ApacheDeveloper
    url = Column(String(255))
    repository_url = Column(String(255), nullable=False)
    repository_type = Column(String(10), nullable=False)
    bug_tracker_url = Column(String(255))
    dev_ml_url = Column(String(255), nullable=False)
    user_ml_url = Column(String(255), nullable=False)

    def __init__(self,
                 name,
                 status,
                 category,
                 language,
                 pmc_chair,
                 url,
                 repository_url,
                 repository_type,
                 bug_tracker_url,
                 dev_ml_url,
                 user_ml_url):
        self.name = name
        self.status = status
        self.category = category
        self.language = language
        self.pmc_chair = pmc_chair
        self.url = url
        self.repository_url = repository_url
        self.repository_type = repository_type
        self.bug_tracker_url = bug_tracker_url
        self.dev_ml_url = dev_ml_url
        self.user_ml_url = user_ml_url


class GithubRepository(Base):
    __tablename__ = 'local_repositories'

    id = Column(BigInteger, primary_key=True)
    slug = Column(String(255), index=True)
    min_commit = Column(DateTime(timezone=True))
    max_commit = Column(DateTime(timezone=True))
    total_commits = Column(Integer)

    def __init__(self,
                 slug,
                 min_commit,
                 max_commit,
                 total_commits):
        self.slug = slug
        self.min_commit = min_commit
        self.max_commit = max_commit
        self.total_commits = total_commits


class MessagesPeople(Base):
    __tablename__ = 'messages_people'
    __table_args__ = (
        ForeignKeyConstraint(['message_id', 'mailing_list_url'],
                             ['messages.message_id',
                              'messages.mailing_list_url'],
                             onupdate='CASCADE',
                             ondelete='CASCADE'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )

    type_of_recipient = Column(Enum('From', 'To', 'Cc',
                                    native_enum=True,
                                    name='enum_type_of_recipient'),
                               primary_key=True,
                               default='From')
    message_id = Column(VARCHAR(255),
                        primary_key=True,
                        index=True)
    mailing_list_url = Column(VARCHAR(255),
                              primary_key=True)
    email_address = Column(VARCHAR(255),
                           ForeignKey('people.email_address',
                                      onupdate='CASCADE',
                                      ondelete='CASCADE'),
                           primary_key=True)

    def __repr__(self):
        return u"<MessagesPeople(type_of_recipient='{0}', " \
               "message_id='{1}', " \
               "mailing_list_url='{1}', " \
               "email_address='{2}')>".format(self.type_of_recipient,
                                              self.message_id,
                                              self.mailing_list_url,
                                              self.email_address)


class Messages(Base):
    __tablename__ = 'messages'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    message_id = Column(VARCHAR(255), primary_key=True)
    mailing_list_url = Column(VARCHAR(255),
                              ForeignKey('mailing_lists.mailing_list_url',
                                         onupdate='CASCADE',
                                         ondelete='CASCADE'),
                              primary_key=True)
    mailing_list = Column(VARCHAR(255))
    first_date = Column(DateTime)
    first_date_tz = Column(NUMERIC(11))
    arrival_date = Column(DateTime)
    arrival_date_tz = Column(NUMERIC(11))
    subject = Column(VARCHAR(1024))
    message_body = Column(MEDIUMTEXT())
    is_response_of = Column(VARCHAR(255), index=True)
    mail_path = Column(TEXT)

    def __repr__(self):
        return u"<Messages(message_id='{0}', " \
               "mailing_list_url='{1}', " \
               "mailing_list='{2}', " \
               "first_date='{3}', first_date_tz='{4}', " \
               "arrival_date='{5}', arrival_date_tz='{6}', " \
               "subject='{7}', message_body='{8}', " \
               "is_response_of='{9}', " \
               "mail_path='{10}')>".format(self.message_id,
                                           self.mailing_list_url,
                                           self.mailing_list,
                                           self.first_date,
                                           self.first_date_tz,
                                           self.arrival_date,
                                           self.arrival_date_tz,
                                           self.subject,
                                           self.message_body,
                                           self.is_response_of,
                                           self.mail_path)


class MailingListSenderId(Base):
    __tablename__ = 'people_id'

    id = Column(BigInteger)
    email_address = Column(String(255), primary_key=True)
    name = Column(String(255))
    username = Column(String(255))

    def __init__(self,
                 id,
                 email_address,
                 name,
                 username,
                 ):
        self.email_address = email_address
        self.name = name
        self.username = username
        self.id = id


class CommitHistoryDevProject(Base):
    __tablename__ = 'commit_history'

    dev_uid = Column(BigInteger, primary_key=True)
    project_name = Column(String(255), primary_key=True)

    num_authored_commits = Column(Integer)
    num_integrated_commits = Column(Integer)

    author_track_record_days = Column(Integer)  # no of days
    committer_track_record_days = Column(Integer)

    authored_commit_shas = Column(TEXT)  # comma-separated string list
    integrated_commit_shas = Column(TEXT)

    first_authored_sha = Column(String(255))
    first_authored_datetime = Column(DateTime)
    last_authored_sha = Column(String(255))
    last_authored_datetime = Column(DateTime)

    first_integrated_sha = Column(String(255))
    first_integrated_datetime = Column(DateTime)
    last_integrated_sha = Column(String(255))
    last_integrated_datetime = Column(DateTime)

    tot_num_additions_authored = Column(Integer)
    tot_num_deletions_authored = Column(Integer)
    tot_num_files_changed_authored = Column(Integer)
    tot_src_loc_added_authored = Column(Integer)
    tot_src_loc_deleted_authored = Column(Integer)
    tot_src_files_touched_authored = Column(Integer)

    tot_num_additions_integrated = Column(Integer)
    tot_num_deletions_integrated = Column(Integer)
    tot_num_files_changed_integrated = Column(Integer)
    tot_src_loc_added_integrated = Column(Integer)
    tot_src_loc_deleted_integrated = Column(Integer)
    tot_src_files_touched_integrated = Column(Integer)

    def __init__(self,
                 dev_uid,
                 project_name,
                 num_authored_commits,
                 num_integrated_commits,
                 author_track_record_days,
                 committer_track_record_days,
                 authored_commit_shas,
                 integrated_commit_shas,
                 first_authored_sha,
                 first_authored_datetime,
                 last_authored_sha,
                 last_authored_datetime,
                 first_integrated_sha,
                 first_integrated_datetime,
                 last_integrated_sha,
                 last_integrated_datetime,
                 tot_num_additions_authored,
                 tot_num_deletions_authored,
                 tot_num_files_changed_authored,
                 tot_src_loc_added_authored,
                 tot_src_loc_deleted_authored,
                 tot_src_files_touched_authored,
                 tot_num_additions_integrated,
                 tot_num_deletions_integrated,
                 tot_num_files_changed_integrated,
                 tot_src_loc_added_integrated,
                 tot_src_loc_deleted_integrated,
                 tot_src_files_touched_integrated
                 ):
        self.dev_uid = dev_uid
        self.project_name = project_name

        self.num_authored_commits = num_authored_commits
        self.num_integrated_commits = num_integrated_commits

        self.author_track_record_days = author_track_record_days
        self.committer_track_record_days = committer_track_record_days

        self.authored_commit_shas = authored_commit_shas
        self.integrated_commit_shas = integrated_commit_shas

        self.first_authored_sha = first_authored_sha
        self.first_authored_datetime = first_authored_datetime
        self.last_authored_sha = last_authored_sha
        self.last_authored_datetime = last_authored_datetime

        self.first_integrated_sha = first_integrated_sha
        self.first_integrated_datetime = first_integrated_datetime
        self.last_integrated_sha = last_integrated_sha
        self.last_integrated_datetime = last_integrated_datetime

        self.tot_num_additions_authored = tot_num_additions_authored
        self.tot_num_deletions_authored = tot_num_deletions_authored
        self.tot_num_files_changed_authored = tot_num_files_changed_authored
        self.tot_src_loc_added_authored = tot_src_loc_added_authored
        self.tot_src_loc_deleted_authored = tot_src_loc_deleted_authored
        self.tot_src_files_touched_authored = tot_src_files_touched_authored

        self.tot_num_additions_integrated = tot_num_additions_integrated
        self.tot_num_deletions_integrated = tot_num_deletions_integrated
        self.tot_num_files_changed_integrated = tot_num_files_changed_integrated
        self.tot_src_loc_added_integrated = tot_src_loc_added_integrated
        self.tot_src_loc_deleted_integrated = tot_src_loc_deleted_integrated
        self.tot_src_files_touched_integrated = tot_src_files_touched_integrated


class Commit(Base):
    __tablename__ = 'local_commits'

    id = Column(BigInteger, primary_key=True)
    repo_id = Column(BigInteger, nullable=False)
    sha = Column(String(255), index=True, nullable=False)
    timestamp_utc = Column(DateTime(timezone=True))
    author_id = Column(BigInteger, nullable=False)
    committer_id = Column(BigInteger, nullable=False)
    message = Column(LONGTEXT)
    num_parents = Column(Integer)
    num_additions = Column(Integer)
    num_deletions = Column(Integer)
    num_files_changed = Column(Integer)
    files = Column(LONGTEXT)  # comma-separated list of file names
    src_loc_added = Column(Integer)
    src_loc_deleted = Column(Integer)
    num_src_files_touched = Column(Integer)
    src_files = Column(LONGTEXT)  # comma-separated list of file names

    def __init__(self,
                 repo_id,
                 sha,
                 timestamp_utc,
                 author_id,
                 committer_id,
                 message,
                 num_parents,
                 num_additions,
                 num_deletions,
                 num_files_changed,
                 files,
                 src_loc_added,
                 src_loc_deleted,
                 num_src_files_touched,
                 src_files
                 ):
        self.repo_id = repo_id
        self.sha = sha
        self.timestamp_utc = timestamp_utc
        self.author_id = author_id
        self.committer_id = committer_id
        self.message = unidecode(message[:len(message)]).strip()
        self.num_parents = num_parents
        self.num_additions = num_additions
        self.num_deletions = num_deletions
        self.num_files_changed = num_files_changed
        self.src_loc_added = src_loc_added
        self.src_loc_deleted = src_loc_deleted
        self.num_src_files_touched = num_src_files_touched
        self.src_files = src_files
        self.files = files


class GithubDeveloper(Base):
    __tablename__ = 'local_developers'

    id = Column(BigInteger, primary_key=True)
    repo_id = Column(BigInteger, index=True, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    name = Column(TEXT)
    email = Column(TEXT, nullable=False)

    def __init__(self,
                 repo_id,
                 user_id,
                 name,
                 email):
        self.repo_id = repo_id
        self.user_id = user_id
        self.name = unidecode(name[:255]).strip()
        self.email = email
