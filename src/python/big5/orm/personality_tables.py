from sqlalchemy import String, Column, Integer, BigInteger, Float
from sqlalchemy.dialects.mysql import LONGTEXT

from db.setup import Base


class Liwc2007ProjectMonth(Base):
    __tablename__ = 'liwc_2007_personality'
    __table_args__ = {
        'extend_existing': True,
        'mysql_row_format': 'DYNAMIC'
    }

    dev_uid = Column(BigInteger, primary_key=True)
    project_name = Column(String(255), primary_key=True)
    month = Column(String(8), primary_key=True)
    email_count = Column(Integer)
    word_count = Column(BigInteger)
    scores = Column(LONGTEXT)

    def __init__(self,
                 dev_uid,
                 project_name,
                 month,
                 email_count,
                 word_count,
                 scores):
        self.dev_uid = dev_uid
        self.project_name = project_name
        self.month = month
        self.email_count = email_count
        self.word_count = word_count
        self.scores = scores

    def __repr__(self):
        return 'developer id {0} scores for project {1}, during month {2}'.format(self.dev_uid,
                                                                                  self.project_name,
                                                                                  self.month)
        
class Liwc2015ProjectMonth(Base):
    __tablename__ = 'liwc_2015_personality'
    __table_args__ = {
        'extend_existing': True,
        'mysql_row_format': 'DYNAMIC'
    }

    dev_uid = Column(BigInteger, primary_key=True)
    project_name = Column(String(255), primary_key=True)
    month = Column(String(8), primary_key=True)
    email_count = Column(Integer)
    word_count = Column(BigInteger)
    scores = Column(LONGTEXT)

    def __init__(self,
                 dev_uid,
                 project_name,
                 month,
                 email_count,
                 word_count,
                 scores):
        self.dev_uid = dev_uid
        self.project_name = project_name
        self.month = month
        self.email_count = email_count
        self.word_count = word_count
        self.scores = scores

    def __repr__(self):
        return 'developer id {0} scores for project {1}, during month {2}'.format(self.dev_uid,
                                                                                  self.project_name,
                                                                                  self.month)


class TwitPersProjectMonth(Base):
    __tablename__ = 'twit_personality'
    __table_args__ = {
        'extend_existing': True,
        'mysql_row_format': 'DYNAMIC'
    }

    dev_uid = Column(BigInteger, primary_key=True)
    project_name = Column(String(255), primary_key=True)
    month = Column(String(8), primary_key=True)
    email_count = Column(Integer)
    word_count = Column(BigInteger)
    scores = Column(LONGTEXT)

    def __init__(self,
                 dev_uid,
                 project_name,
                 month,
                 email_count,
                 word_count,
                 scores):
        self.dev_uid = dev_uid
        self.project_name = project_name
        self.month = month
        self.email_count = email_count
        self.word_count = word_count
        self.scores = scores

    def __repr__(self):
        return 'developer id {0} scores for project {1}, during month {2}'.format(self.dev_uid,
                                                                                  self.project_name,
                                                                                  self.month)
