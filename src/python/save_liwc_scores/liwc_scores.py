import csv
import logging
import sys
from db.setup import SessionWrapper
from logger import logging_config

from save_liwc_scores.orm.scores_tables import *

def import_result(session, result):
    filename = result['Filename'].replace(".txt", "")
    uid, p_name, month = filename.split("_")

    if dictionary == '2007':
        #missing: clout, female, differ, informal, adj, risk, male, compare,
        # affiliation, netspeak, power, interrog, drives, reward
        ls = Liwc2007Scores(dev_uid=uid, project_name=p_name, month=month, email_count = 0, wc=result["WC"],
                            sixltr=result["Sixltr"].replace(",","."), wps=result["WPS"].replace(",","."),
                            dic=result["Dic"].replace(",","."), family=result["family"].replace(",","."),
                            feel=result["feel"].replace(",","."), money=result["money"].replace(",","."),
                            insight=result["insight"].replace(",","."), number=result["number"].replace(",","."),
                            parenth=result["Parenth"].replace(",","."), otherp=result["OtherP"].replace(",","."),
                            negate=result["negate"].replace(",","."), negemo=result["negemo"].replace(",","."),
                            death=result["death"].replace(",","."), adverb=result["adverb"].replace(",","."),
                            ipron=result["ipron"].replace(",","."), percept=result["percept"].replace(",","."),
                            quant=result["quant"].replace(",","."), exclam=result["Exclam"].replace(",","."),
                            preps=result["preps"].replace(",","."), achieve=result["achieve"].replace(",","."),
                            bio=result["bio"].replace(",","."), leisure=result["leisure"].replace(",","."),
                            quote=result["Quote"].replace(",","."), verb=result["verb"].replace(",","."),
                            hear=result["hear"].replace(",","."), they=result["they"].replace(",","."),
                            affect=result["affect"].replace(",","."), you=result["you"].replace(",","."),
                            work=result["work"].replace(",","."), period=result["Period"].replace(",","."),
                            friend=result["friend"].replace(",","."), auxverb=result["auxverb"].replace(",","."),
                            shehe=result["shehe"].replace(",","."), semic=result["SemiC"].replace(",","."),
                            relig=result["relig"].replace(",","."), pronoun=result["pronoun"].replace(",","."),
                            qmark=result["QMark"].replace(",","."), certain=result["certain"].replace(",","."),
                            assent=result["assent"].replace(",","."), we=result["we"].replace(",","."),
                            sad=result["sad"].replace(",","."), see=result["see"].replace(",","."),
                            anger=result["anger"].replace(",","."), home=result["home"].replace(",","."),
                            conj=result["conj"].replace(",","."), sexual=result["sexual"].replace(",","."),
                            ppron=result["ppron"].replace(",","."), motion=result["motion"].replace(",","."),
                            space=result["space"].replace(",","."), filler=result["filler"].replace(",","."),
                            anx=result["anx"].replace(",","."),  health=result["health"].replace(",","."),
                            discrep=result["discrep"].replace(",","."), relativ=result["relativ"].replace(",","."),
                            colon=result["Colon"].replace(",","."), cause=result["cause"].replace(",","."),
                            body=result["body"].replace(",","."), tentat=result["tentat"].replace(",","."),
                            social=result["social"].replace(",","."),  article=result["article"].replace(",","."),
                            allpunc=result["AllPunc"].replace(",","."), apostro=result["Apostro"].replace(",","."),
                            i=result["i"].replace(",","."), posemo=result["posemo"].replace(",","."),
                            ingest=result["ingest"].replace(",","."), dash=result["Dash"].replace(",","."),
                            swear=result["swear"].replace(",","."), comma=result["Comma"].replace(",","."),
                            time=result["time"].replace(",","."), cogmech=result["cogmech"].replace(",","."),
                            funct=result["funct"].replace(",","."), future=result["future"].replace(",","."),
                            present=result["present"].replace(",","."), past=result["past"].replace(",","."),
                            nonfl=result["nonfl"].replace(",","."), humans=result["humans"].replace(",","."),
                            incl=result["incl"].replace(",","."), excl=result["excl"].replace(",","."))
        
    elif dictionary == '2015':
        ls = Liwc2015Scores(dev_uid=uid, project_name=p_name, month=month, email_count=0, wc=result["WC"],
                        sixltr=result["Sixltr"].replace(",","."), clout=result["Clout"].replace(",","."),
                        wps=result["WPS"].replace(",","."), analytic=result["Analytic"].replace(",","."),
                        tone=result["Tone"].replace(",","."), dic=result["Dic"].replace(",","."),
                        authentic=result["Authentic"].replace(",","."), family=result["family"].replace(",","."),
                        feel=result["feel"].replace(",","."), money=result["money"].replace(",","."),
                        insight=result["insight"].replace(",","."), number=result["number"].replace(",","."),
                        parenth=result["Parenth"].replace(",","."), cogproc=result["cogproc"].replace(",","."),
                        otherp=result["OtherP"].replace(",","."), female=result["female"].replace(",","."),
                        negate=result["negate"].replace(",","."), negemo=result["negemo"].replace(",","."),
                        differ=result["differ"].replace(",","."), death=result["death"].replace(",","."),
                        adverb=result["adverb"].replace(",","."),  informal=result["informal"].replace(",","."),
                        ipron=result["ipron"].replace(",","."), percept=result["percept"].replace(",","."),
                        quant=result["quant"].replace(",","."), exclam=result["Exclam"].replace(",","."),
                        adj=result["adj"].replace(",","."), prep=result["prep"].replace(",","."),
                        achieve=result["achieve"].replace(",","."), function=result["function"].replace(",","."),
                        bio=result["bio"].replace(",","."),  risk=result["risk"].replace(",","."),
                        leisure=result["leisure"].replace(",","."), quote=result["Quote"].replace(",","."),
                        verb=result["verb"].replace(",","."), hear=result["hear"].replace(",","."),
                        they=result["they"].replace(",","."), affect=result["affect"].replace(",","."),
                        you=result["you"].replace(",","."), work=result["work"].replace(",","."),
                        period=result["Period"].replace(",","."), friend=result["friend"].replace(",","."),
                        focusfuture=result["focusfuture"].replace(",","."), auxverb=result["auxverb"].replace(",","."),
                        male=result["male"].replace(",","."), shehe=result["shehe"].replace(",","."),
                        semic=result["SemiC"].replace(",","."), relig=result["relig"].replace(",","."),
                        compare=result["compare"].replace(",","."), pronoun=result["pronoun"].replace(",","."),
                        qmark=result["QMark"].replace(",","."), certain=result["certain"].replace(",","."),
                        assent=result["assent"].replace(",","."), we=result["we"].replace(",","."),
                        sad=result["sad"].replace(",","."), affiliation=result["affiliation"].replace(",","."),
                        see=result["see"].replace(",","."), anger=result["anger"].replace(",","."),
                        home=result["home"].replace(",","."), conj=result["conj"].replace(",","."),
                        sexual=result["sexual"].replace(",","."), ppron=result["ppron"].replace(",","."), 
                        motion=result["motion"].replace(",","."), space=result["space"].replace(",","."),
                        filler=result["filler"].replace(",","."), anx=result["anx"].replace(",","."),
                        focuspresent=result["focuspresent"].replace(",","."), netspeak=result["netspeak"].replace(",","."),
                        health=result["health"].replace(",","."), discrep=result["discrep"].replace(",","."),
                        relativ=result["relativ"].replace(",","."), colon=result["Colon"].replace(",","."),
                        nonflu=result["nonflu"].replace(",","."), cause=result["cause"].replace(",","."),
                        body=result["body"].replace(",","."), tentat=result["tentat"].replace(",","."),
                        power=result["power"].replace(",","."), interrog=result["interrog"].replace(",","."),
                        social=result["social"].replace(",","."), drives=result["drives"].replace(",","."),
                        focuspast=result["focuspast"].replace(",","."), article=result["article"].replace(",","."),
                        allpunc=result["AllPunc"].replace(",","."), apostro=result["Apostro"].replace(",","."),
                        i=result["i"].replace(",","."), posemo=result["posemo"].replace(",","."),
                        ingest=result["ingest"].replace(",","."), dash=result["Dash"].replace(",","."),
                        swear=result["swear"].replace(",","."), comma=result["Comma"].replace(",","."),
                        time=result["time"].replace(",","."), reward=result["reward"].replace(",","."))
        
    session.add(ls)
    session.commit()
    logger.info('Imported results from file: \'%s\'' % result['Filename'])
  
def reset_table():
    if dictionary == '2007':
        session.query(Liwc2007Scores).delete()
    elif dictionary == '2015':
        session.query(Liwc2015Scores).delete()
    
if __name__ == '__main__':
    logger = logging_config.get_logger('save_liwc_scores', console_level=logging.DEBUG)
    SessionWrapper.load_config('../db/cfg/setup.yml')
    session = SessionWrapper.new(init=True)
    
    if len(sys.argv) >= 3:
        dictionary = sys.argv[2]
    else:
        logger.error('Missing mandatory params')
        sys.exit(-1)
    
    reset_table()
     
    try : 
        with open(sys.argv[1]) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                import_result(session, row)
    except FileNotFoundError as e:
        logger.error('No such file or directory')
        sys.exit(-1)
