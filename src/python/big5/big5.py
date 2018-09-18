import logging
import os
import sys
from db.setup import SessionWrapper
from logger import logging_config

from orm.personality_tables import *
from save_liwc_scores.orm.scores_tables import *

from twit_personality.training.datasetUtils import parseFastText
from twit_personality.training.embeddings import transformTextForTesting
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib
import numpy as np

#References
#[1] T. Yarkoni, "Personality in 100,000 words: A large-scale analysis of personality and word use among bloggers," Journal of research in
#personality, vol. 44, no. 3, pp.363-373, 2010

def get_openness(score):

    value = (   - 0.21 * score.pronoun - 0.16 * score.i - 0.1 * score.we - 0.12 * score.you - 0.13 * score.negate - 0.11 * score.assent
                + 0.2 * score.article - 0.12 * score.affect - 0.15 * score.posemo 
                - 0.12 * score.discrep - 0.08 * score.hear - 0.14 * score.social - 0.17 * score.family - 0.22 * score.time
                - 0.11 * score.space - 0.22 * score.motion - 0.17 * score.leisure
                - 0.2 * score.home + 0.15 * score.death - 0.15 * score.ingest)

    if tool == 'liwc07':
        #categories indicated by Yarkoni[1] missing in liwc 2007 dictionary: first person, positive feelings, sensory processes, other references,
        # sports, physical states, sleep, grooming
        value = value + 0.17 * score.preps - 0.09 * score.cogmech - 0.16 * score.past - 0.16 * score.present - 0.09 * score.humans - 0.11 * score.incl
    elif tool == 'liwc15':
        #categories indicated by Yarkoni[1] missing in liwc 2015 dictionary: first person, positive feelings, sensory processes, other references,
        # humans, inclusive, sports, physical states, sleep, grooming
        value = value + 0.17 * score.prep - 0.09 * score.cogproc - 0.16 * score.focuspast - 0.16 * score.focuspresent
    
    return value


def get_conscientiousness(score):
    value = (   - 0.17 * score.negate - 0.18 * score.negemo - 0.19 * score.anger - 0.11 * score.sad - 0.12 * score.cause
                - 0.13 * score.discrep - 0.1 * score.tentat - 0.1 * score.certain - 0.12 * score.hear + 0.09 * score.time + 0.14 * score.achieve
                - 0.12 * score.death - 0.14 * score.swear)
    
    if tool == 'liwc07':
        #categories indicated by Yarkoni[1] missing in liwc 2007 dictionary:  sensory processes, music
        value = value - 0.11 * score.cogmech - 0.12 * score.humans - 0.16 * score.excl
    elif tool == 'liwc15':
        #categories indicated by Yarkoni[1] missing in liwc 2015 dictionary:  sensory processes, humans, exclusive, music
        value = value - 0.11 * score.cogproc
    
    return value


def get_extraversion(score):
    value = (   0.11 * score.we + 0.16 * score.you - 0.12 * score.number + 0.1 * score.posemo - 0.09 * score.cause - 0.11 * score.tentat
                + 0.1 * score.certain + 0.12 * score.hear + 0.15 * score.social + 0.15 * score.friend + 0.09 * score.family
                - 0.08 * score.work - 0.09 * score.achieve + 0.08 * score.leisure + 0.11 * score.relig + 0.1 * score.body
                + 0.17 * score.sexual)
    
    if tool == 'liwc07':
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

    if tool == 'liwc07':
        #categories indicated by Yarkoni[1] missing in liwc 2007 dictionary: positive feelings, other references, music, physical states, sleep
        value = value + 0.1 * score.past + 0.18 * score.incl
    elif tool == 'liwc15':
        #categories indicated by Yarkoni[1] missing in liwc 2015 dictionary: positive feelings, other references, inclusive, music, physical states, sleep
        value = value + 0.1 * score.focuspast 
    
    return value

def get_neuroticism(score):
    value = (   0.12 * score.i - 0.15 * score.you + 0.11 * score.negate - 0.11 * score.article + 0.16 * score.negemo + 0.17 * score.anx
                + 0.13 * score.anger + 0.1 * score.sad + 0.11 * score.cause + 0.13 * score.discrep
                + 0.12 * score.tentat + 0.13 * score.certain + 0.1 * score.feel - 0.08 * score.friend - 0.09 * score.space + 0.11 + score.swear)
    
    if tool == 'liwc07':
        #categories indicated by Yarkoni[1] missing in liwc 2007 dictionary: first person, other references, sleep
        value = value + 0.13 * score.cogmech + 0.1 * score.excl 
    elif tool == 'liwc15':
        #categories indicated by Yarkoni[1] missing in liwc 2015 dictionary: first person, other references, exclusive, sleep
        value = value + 0.13 * score.cogproc 
    
    return value


def get_profile_liwc():
    if tool == 'liwc07':
        scores = session.query(Liwc2007Scores)
    elif tool == 'liwc15':
        scores = session.query(Liwc2015Scores)
        
    for score in scores:
        big5 = {}
        big5['openness'] = get_openness(score)
        big5['conscientiousness'] = get_conscientiousness(score)
        big5['extraversion'] = get_extraversion(score)
        big5['agreeableness'] = get_agreeableness(score)
        big5['neuroticism'] = get_neuroticism(score)

        if tool == 'liwc07':
            lpm = Liwc2007ProjectMonth(dev_uid=score.dev_uid, project_name=score.project_name, month=score.month,
                                   email_count=score.email_count, word_count=score.wc, scores=big5)
        elif tool == 'liwc15':
            lpm = Liwc2015ProjectMonth(dev_uid=score.dev_uid, project_name=score.project_name, month=score.month,
                                   email_count=score.email_count, word_count=score.wc, scores=big5)
        
        session.add(lpm)
        session.commit()

def get_profile_twit_pers():
    dataset_path = "twit_personality/FastText/dataset.vec"
    tweet_threshold = 3
    vectorizer = CountVectorizer(stop_words="english", analyzer="word")
    analyzer = vectorizer.build_analyzer()
    
    logger.info('Loading embeddings dataset...')
    wordDictionary = parseFastText(dataset_path)
    logger.info('Data successfully loaded.')
    
    content = os.listdir("../export_content/content/")
    big5 = {}
    i = 0
    for file in content:
        filename = file.split('_')
        uid = filename[0]
        p_name = filename[1]
        _month = filename[2].replace(".txt", "")
        
        lines=[]
        with open('../export_content/content/'+file) as f:
            for line in f:
                lines.append(line)
                
        try:
            content = open("../export_content/content/"+file, "r").read()
            content = transformTextForTesting(wordDictionary, tweet_threshold, lines, "conc")
            logger.info("Embeddings computed.")
        except:
            logger.info("Not enough words for prediction.")
            continue
        
        scores = {}
        for trait in ["O","C","E","A","N"]:
            model = joblib.load("twit_personality/training/Models/SVM/SVM_"+trait+".pkl")
            preds = model.predict(content)
            scores[trait] = float(str(np.mean(np.array(preds) ) ) [0:5] )
           
        big5['openness'] = scores["O"]
        big5['conscientiousness'] = scores["C"]
        big5['extraversion'] = scores["E"]
        big5['agreeableness'] = scores["A"]
        big5['neuroticism'] = scores["N"]
        
        tpm = TwitPersProjectMonth(dev_uid=uid, project_name=p_name, month=_month,
                                   email_count=None, word_count=None, scores=big5)
        
        session.add(tpm)
        session.commit()
    

def reset_table():
    if tool == 'liwc07':
        session.query(Liwc2007ProjectMonth).delete()
    elif tool == 'liwc15':
        session.query(Liwc2015ProjectMonth).delete()
    elif tool == 'twitPers':
        session.query(TwitPersProjectMonth).delete()
    logger.info('Done resetting table')
    
if __name__ == '__main__':
    logger = logging_config.get_logger('big5', console_level=logging.DEBUG)
    SessionWrapper.load_config('../db/cfg/setup.yml')
    session = SessionWrapper.new(init=True)
    
    if len(sys.argv) >= 2:
        tool = sys.argv[1]
    else:
        logger.error('Missing mandatory first param for tool: \'liwc07\', \'liwc15\' or \'twitPers\' expected')
        sys.exit(-1)
    
    try:
        reset_table()
        if tool == 'liwc07' or tool == 'liwc15':
            get_profile_liwc()
        elif tool == 'twitPers':
            get_profile_twit_pers()
        logger.info('Done getting personality scores')
    except KeyboardInterrupt:
        logger.error('Received Ctrl-C or other break signal. Exiting.')
     
