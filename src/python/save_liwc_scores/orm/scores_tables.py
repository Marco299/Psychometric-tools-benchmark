from sqlalchemy import String, Column, Integer, BigInteger, Float
from sqlalchemy.dialects.mysql import LONGTEXT

from db.setup import Base


class Liwc2007Scores(Base):
    __tablename__ = 'liwc_2007_scores'
    __table_args__ = {
        'extend_existing': True,
        'mysql_row_format': 'DYNAMIC'
    }

    dev_uid = Column(BigInteger, primary_key=True)
    project_name = Column(String(255), primary_key=True)
    month = Column(String(8), primary_key=True)
    email_count = Column(Integer)
    wc = Column(Integer)
    sixltr = Column(Float)
    wps = Column(Float)
    dic = Column(Float)
    family = Column(Float)
    feel = Column(Float)
    money = Column(Float)
    insight = Column(Float)
    number = Column(Float)
    parenth = Column(Float)
    otherp = Column(Float)
    negate = Column(Float)
    negemo = Column(Float)
    death = Column(Float)
    adverb = Column(Float)
    ipron = Column(Float)
    percept = Column(Float)
    quant = Column(Float)
    exclam = Column(Float)
    preps = Column(Float)
    achieve = Column(Float)
    bio = Column(Float)
    leisure = Column(Float)
    quote = Column(Float)
    verb = Column(Float)
    hear = Column(Float)
    they = Column(Float)
    affect = Column(Float)
    you = Column(Float)
    work = Column(Float)
    period = Column(Float)
    friend = Column(Float)
    auxverb = Column(Float)
    shehe = Column(Float)
    semic = Column(Float)
    relig = Column(Float)
    pronoun = Column(Float)
    qmark = Column(Float)
    certain = Column(Float)
    assent = Column(Float)
    we = Column(Float)
    sad = Column(Float)
    see = Column(Float)
    anger = Column(Float)
    home = Column(Float)
    conj = Column(Float)
    sexual = Column(Float)
    ppron = Column(Float)
    motion = Column(Float)
    space = Column(Float)
    filler = Column(Float)
    anx = Column(Float)
    health = Column(Float)
    discrep = Column(Float)
    relativ = Column(Float)
    colon = Column(Float)
    cause = Column(Float)
    body = Column(Float)
    tentat = Column(Float)
    social = Column(Float)
    article = Column(Float)
    allpunc = Column(Float)
    apostro = Column(Float)
    i = Column(Float)
    posemo = Column(Float)
    ingest = Column(Float)
    dash = Column(Float)
    swear = Column(Float)
    comma = Column(Float)
    time = Column(Float)
    cogmech = Column(Float)
    funct = Column(Float)
    future = Column(Float)
    present = Column(Float)
    past = Column(Float)
    nonfl = Column(Float)
    humans = Column(Float)
    incl = Column(Float)
    excl = Column(Float)
    

    def __init__(self, dev_uid, project_name, month, email_count, wc, sixltr, wps, dic,
                 family, feel, money, insight, number, parenth, otherp, negate, negemo,
                 death, adverb, ipron, percept, quant, exclam, preps, achieve, bio, 
                 leisure, quote, verb, hear, they, affect, you, work, period, friend,
                 auxverb, shehe, semic, relig, pronoun, qmark, certain, assent, we,
                sad, see, anger, home, conj, sexual, ppron, motion, space, filler, anx,
                 health, discrep, relativ, colon, cause, body, tentat, social, article,
                 allpunc, apostro, i, posemo, ingest, dash, swear, comma, time, cogmech,
                 funct, future, present, past, nonfl, humans, incl, excl):
        self.dev_uid = dev_uid
        self.project_name = project_name
        self.month = month
        self.email_count = email_count
        self.wc = wc
        self.sixltr = sixltr
        self.wps = wps
        self.dic = dic
        self.family = family
        self.feel = feel
        self.money = money
        self.insight = insight
        self.number = number
        self.parenth = parenth
        self.otherp = otherp
        self.negate = negate
        self.negemo = negemo
        self.death = death
        self.adverb = adverb
        self.ipron = ipron
        self.percept = percept
        self.quant = quant
        self.exclam = exclam
        self.preps = preps
        self.achieve = achieve
        self.bio = bio
        self.leisure = leisure
        self.quote = quote
        self.verb = verb
        self.hear = hear
        self.they = they
        self.affect = affect
        self.you = you
        self.work = work
        self.period = period
        self.friend = friend
        self.auxverb = auxverb
        self.shehe = shehe
        self.semic = semic
        self.relig = relig
        self.pronoun = pronoun
        self.qmark = qmark
        self.certain = certain
        self.assent = assent
        self.we = we
        self.sad = sad
        self.see = see
        self.anger = anger
        self.home = home
        self.conj = conj
        self.sexual = sexual
        self.ppron = ppron
        self.motion = motion
        self.space = space
        self.filler = filler
        self.anx = anx
        self.health = health
        self.discrep = discrep
        self.relativ = relativ
        self.colon = colon
        self.cause = cause
        self.body = body
        self.tentat = tentat
        self.social = social
        self.article = article
        self.allpunc = allpunc
        self.apostro = apostro
        self.i = i
        self.posemo = posemo
        self.ingest = ingest
        self.dash = dash
        self.swear = swear
        self.comma = comma
        self.time = time
        self.cogmech = cogmech
        self.funct = funct
        self.future = future
        self.present = present
        self.past = past
        self.nonfl = nonfl
        self.humans = humans
        self.incl = incl
        self.excl = excl


class Liwc2015Scores(Base):
    __tablename__ = 'liwc_2015_scores'
    __table_args__ = {
        'extend_existing': True,
        'mysql_row_format': 'DYNAMIC'
    }

    dev_uid = Column(BigInteger, primary_key=True)
    project_name = Column(String(255), primary_key=True)
    month = Column(String(8), primary_key=True)
    email_count = Column(Integer)
    wc = Column(Integer)
    sixltr = Column(Float)
    clout = Column(Float)
    wps = Column(Float)
    analytic = Column(Float)
    tone = Column(Float)
    dic = Column(Float)
    authentic = Column(Float)
    family = Column(Float)
    feel = Column(Float)
    money = Column(Float)
    insight = Column(Float)
    number = Column(Float)
    parenth = Column(Float)
    cogproc = Column(Float)
    otherp = Column(Float)
    female = Column(Float)
    negate = Column(Float)
    negemo = Column(Float)
    differ = Column(Float)
    death = Column(Float)
    adverb = Column(Float)
    informal = Column(Float)
    ipron = Column(Float)
    percept = Column(Float)
    quant = Column(Float)
    exclam = Column(Float)
    adj = Column(Float)
    prep = Column(Float)
    achieve = Column(Float)
    function = Column(Float)
    bio = Column(Float)
    risk = Column(Float)
    leisure = Column(Float)
    quote = Column(Float)
    verb = Column(Float)
    hear = Column(Float)
    they = Column(Float)
    affect = Column(Float)
    you = Column(Float)
    work = Column(Float)
    period = Column(Float)
    friend = Column(Float)
    focusfuture = Column(Float)
    auxverb = Column(Float)
    male = Column(Float)
    shehe = Column(Float)
    semic = Column(Float)
    relig = Column(Float)
    compare = Column(Float)
    pronoun = Column(Float)
    qmark = Column(Float)
    certain = Column(Float)
    assent = Column(Float)
    we = Column(Float)
    sad = Column(Float)
    affiliation = Column(Float)
    see = Column(Float)
    anger = Column(Float)
    home = Column(Float)
    conj = Column(Float)
    sexual = Column(Float)
    ppron = Column(Float)
    motion = Column(Float)
    space = Column(Float)
    filler = Column(Float)
    anx = Column(Float)
    focuspresent = Column(Float)
    netspeak = Column(Float)
    health = Column(Float)
    discrep = Column(Float)
    relativ = Column(Float)
    colon = Column(Float)
    nonflu = Column(Float)
    cause = Column(Float)
    body = Column(Float)
    tentat = Column(Float)
    power = Column(Float)
    interrog = Column(Float)
    social = Column(Float)
    drives = Column(Float)
    focuspast = Column(Float)
    article = Column(Float)
    allpunc = Column(Float)
    apostro = Column(Float)
    i = Column(Float)
    posemo = Column(Float)
    ingest = Column(Float)
    dash = Column(Float)
    swear = Column(Float)
    comma = Column(Float)
    time = Column(Float)
    reward = Column(Float)

    def __init__(self, dev_uid, project_name, month, email_count, wc, sixltr, clout, wps, analytic, tone, dic,
                 authentic, family, feel, money, insight, number, parenth, cogproc, otherp,
                 female, negate, negemo, differ, death, adverb, informal, ipron, percept, quant, exclam, adj, prep,
                 achieve, function, bio, risk, leisure,
                 quote, verb, hear, they, affect, you, work, period, friend, focusfuture, auxverb, male, shehe, semic,
                 relig, compare, pronoun, qmark, certain,
                 assent, we, sad, affiliation, see, anger, home, conj, sexual, ppron, motion, space, filler, anx,
                 focuspresent, netspeak, health, discrep,
                 relativ, colon, nonflu, cause, body, tentat, power, interrog, social, drives, focuspast, article,
                 allpunc, apostro, i, posemo, ingest, dash,
                 swear, comma, time, reward):
        self.dev_uid = dev_uid
        self.project_name = project_name
        self.month = month
        self.email_count = email_count
        self.wc = wc
        self.sixltr = sixltr
        self.clout = clout
        self.wps = wps
        self.analytic = analytic
        self.tone = tone
        self.dic = dic
        self.authentic = authentic
        self.family = family
        self.feel = feel
        self.money = money
        self.insight = insight
        self.number = number
        self.parenth = parenth
        self.cogproc = cogproc
        self.otherp = otherp
        self.female = female
        self.negate = negate
        self.negemo = negemo
        self.differ = differ
        self.death = death
        self.adverb = adverb
        self.informal = informal
        self.ipron = ipron
        self.percept = percept
        self.quant = quant
        self.exclam = exclam
        self.adj = adj
        self.prep = prep
        self.achieve = achieve
        self.function = function
        self.bio = bio
        self.risk = risk
        self.leisure = leisure
        self.quote = quote
        self.verb = verb
        self.hear = hear
        self.they = they
        self.affect = affect
        self.you = you
        self.work = work
        self.period = period
        self.friend = friend
        self.focusfuture = focusfuture
        self.auxverb = auxverb
        self.male = male
        self.shehe = shehe
        self.semic = semic
        self.relig = relig
        self.compare = compare
        self.pronoun = pronoun
        self.qmark = qmark
        self.certain = certain
        self.assent = assent
        self.we = we
        self.sad = sad
        self.affiliation = affiliation
        self.see = see
        self.anger = anger
        self.home = home
        self.conj = conj
        self.sexual = sexual
        self.ppron = ppron
        self.motion = motion
        self.space = space
        self.filler = filler
        self.anx = anx
        self.focuspresent = focuspresent
        self.netspeak = netspeak
        self.health = health
        self.discrep = discrep
        self.relativ = relativ
        self.colon = colon
        self.nonflu = nonflu
        self.cause = cause
        self.body = body
        self.tentat = tentat
        self.power = power
        self.interrog = interrog
        self.social = social
        self.drives = drives
        self.focuspast = focuspast
        self.article = article
        self.allpunc = allpunc
        self.apostro = apostro
        self.i = i
        self.posemo = posemo
        self.ingest = ingest
        self.dash = dash
        self.swear = swear
        self.comma = comma
        self.time = time
        self.reward = reward