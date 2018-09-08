import logging
import sys
from db.setup import SessionWrapper
from logger import logging_config

from orm.personality_tables import *
from save_liwc_scores.orm.scores_tables import *

#References
#[1] T. Yarkoni, "Personality in 100,000 words: A large-scale analysis of personality and word use among bloggers," Journal of research in
#personality, vol. 44, no. 3, pp.363-373, 2010

def get_openness(score):

    value = (   - 0.21 * score.pronoun - 0.16 * score.i - 0.1 * score.we - 0.12 * score.you - 0.13 * score.negate - 0.11 * score.assent
                + 0.2 * score.article - 0.12 * score.affect - 0.15 * score.posemo 
                - 0.12 * score.discrep - 0.08 * score.hear - 0.14 * score.social - 0.17 * score.family - 0.22 * score.time
                - 0.11 * score.space - 0.22 * score.motion - 0.17 * score.leisure
                - 0.2 * score.home + 0.15 * score.death - 0.15 * score.ingest)

    if dictionary == '2007':
        #categories indicated by Yarkoni[1] missing in liwc 2007 dictionary: first person, positive feelings, sensory processes, other references,
        # sports, physical states, sleep, grooming
        value = value + 0.17 * score.preps - 0.09 * score.cogmech - 0.16 * score.past - 0.16 * score.present - 0.09 * score.humans - 0.11 * score.incl
    elif dictionary == '2015':
        #categories indicated by Yarkoni[1] missing in liwc 2015 dictionary: first person, positive feelings, sensory processes, other references,
        # humans, inclusive, sports, physical states, sleep, grooming
        value = value + 0.17 * score.prep - 0.09 * score.cogproc - 0.16 * score.focuspast - 0.16 * score.focuspresent
    
    return value


def get_conscientiousness(score):
    value = (   - 0.17 * score.negate - 0.18 * score.negemo - 0.19 * score.anger - 0.11 * score.sad - 0.12 * score.cause
                - 0.13 * score.discrep - 0.1 * score.tentat - 0.1 * score.certain - 0.12 * score.hear + 0.09 * score.time + 0.14 * score.achieve
                - 0.12 * score.death - 0.14 * score.swear)
    
    if dictionary == '2007':
        #categories indicated by Yarkoni[1] missing in liwc 2007 dictionary:  sensory processes, music
        value = value - 0.11 * score.cogmech - 0.12 * score.humans - 0.16 * score.excl
    elif dictionary == '2015':
        #categories indicated by Yarkoni[1] missing in liwc 2015 dictionary:  sensory processes, humans, exclusive, music
        value = value - 0.11 * score.cogproc
    
    return value


def get_extraversion(score):
    value = (   0.11 * score.we + 0.16 * score.you - 0.12 * score.number + 0.1 * score.posemo - 0.09 * score.cause - 0.11 * score.tentat
                + 0.1 * score.certain + 0.12 * score.hear + 0.15 * score.social + 0.15 * score.friend + 0.09 * score.family
                - 0.08 * score.work - 0.09 * score.achieve + 0.08 * score.leisure + 0.11 * score.relig + 0.1 * score.body
                + 0.17 * score.sexual)
    
    if dictionary == '2007':
        #categories indicated by Yarkoni[1] missing in liwc 2007 dictionary: positive feelings, sensory processes, communication, other references,
        #  occupation, music, physical states
        value = value + 0.13 * score.humans + 0.09 * score.incl

    #categories indicated by Yarkoni[1] missing in liwc 2015 dictionary: positive feelings, sensory processes, communication, other references, humans,
    #  inclusive, occupation, music, physical states
    
    return value


def get_agreeableness(score):
    value = (   0.11 * score.pronoun + 0.18 * score.we + 0.11 * score.number + 0.18 * score.posemo - 0.15 * score.negemo - 0.23 * score.anger
                - 0.11 * score.cause + 0.09 * score.see + 0.1 * score.feel + 0.13 * score.social + 0.11 * score.friend + 0.19 * score.family
                + 0.12 * score.time + 0.16 * score.space + 0.14 * score.motion + 0.15 * score.leisure + 0.19 * score.home
                - 0.11 * score.money - 0.13 * score.death + 0.09 * score.body + 0.08 * score.sexual - 0.21 * score.swear)

    if dictionary == '2007':
        #categories indicated by Yarkoni[1] missing in liwc 2007 dictionary: positive feelings, other references, music, physical states, sleep
        value = value + 0.1 * score.past + 0.18 * score.incl
    elif dictionary == '2015':
        #categories indicated by Yarkoni[1] missing in liwc 2015 dictionary: positive feelings, other references, inclusive, music, physical states, sleep
        value = value + 0.1 * score.focuspast 
    
    return value

def get_neuroticism(score):
    value = (   0.12 * score.i - 0.15 * score.you + 0.11 * score.negate - 0.11 * score.article + 0.16 * score.negemo + 0.17 * score.anx
                + 0.13 * score.anger + 0.1 * score.sad + 0.11 * score.cause + 0.13 * score.discrep
                + 0.12 * score.tentat + 0.13 * score.certain + 0.1 * score.feel - 0.08 * score.friend - 0.09 * score.space + 0.11 + score.swear)
    
    if dictionary == '2007':
        #categories indicated by Yarkoni[1] missing in liwc 2007 dictionary: first person, other references, sleep
        value = value + 0.13 * score.cogmech + 0.1 * score.excl 
    elif dictionary == '2015':
        #categories indicated by Yarkoni[1] missing in liwc 2015 dictionary: first person, other references, exclusive, sleep
        value = value + 0.13 * score.cogproc 
    
    return value


def get_profile_liwc():
    if dictionary == '2007':
        scores = session.query(Liwc2007Scores)
    elif dictionary == '2015':
        scores = session.query(Liwc2015Scores)
        
    for score in scores:
        big5 = {}
        big5['openness'] = get_openness(score)
        big5['conscientiousness'] = get_conscientiousness(score)
        big5['extraversion'] = get_extraversion(score)
        big5['agreeableness'] = get_agreeableness(score)
        big5['neuroticism'] = get_neuroticism(score)

        if dictionary == '2007':
            lpm = Liwc2007ProjectMonth(dev_uid=score.dev_uid, project_name=score.project_name, month=score.month,
                                   email_count=score.email_count, word_count=score.wc, scores=big5)
        elif dictionary == '2015':
            lpm = Liwc2015ProjectMonth(dev_uid=score.dev_uid, project_name=score.project_name, month=score.month,
                                   email_count=score.email_count, word_count=score.wc, scores=big5)
        
        session.add(lpm)
        session.commit()

def reset_table():
    if dictionary == '2007':
        session.query(Liwc2007ProjectMonth).delete()
    elif dictionary == '2015':
        session.query(Liwc2015ProjectMonth).delete()
    
if __name__ == '__main__':
    logger = logging_config.get_logger('big5', console_level=logging.DEBUG)
    SessionWrapper.load_config('../db/cfg/setup.yml')
    session = SessionWrapper.new(init=True)
    
    if len(sys.argv) >= 2:
        dictionary = sys.argv[1]
    else:
        logger.error('Missing mandatory first param for dictionary: \'2007\' or \'2015\' expected')
        sys.exit(-1)
    
    reset_table()
    get_profile_liwc()
    logger.info('Done getting personality scores')
     