from django.db import models

# Create your models here.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, desc, func
from sqlalchemy.orm import sessionmaker
import datetime 

Base = declarative_base()

class timelion(Base):
    __tablename__ = 'timelion'

    fid = Column(String(50), ForeignKey('info.fid'), primary_key=True)
    tpostnum = Column(Integer)
    tid = Column(String(length=50))
    updatetime = Column(DateTime, primary_key=True, default=datetime.datetime.now)
    unum = Column(Integer)

    def __repr__(self):
        return 'fid:{},updatetime:{},unum:{}'.format(self.fid, self.updatetime, self.unum)


class info(Base):
    __tablename__ = 'info'

    fid = Column(String(length=10), primary_key=True)
    fname = Column(String(length=50))
    url = Column(String(length=50))

    def __repr__(self):
        return 'fid:{},fname:{},url:{}'.format(self.fid, self.fname, self.url)


engine = create_engine('mysql+pymysql://itoffice:itoffice@192.168.127.129:3306/hp')
#timelion.__table__
#info.__table__
#Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()
# result = session.query(timelion.fid, func.sum(timelion.unum)).filter(timelion.updatetime<now_time, timelion.updatetime>yes_time).group_by(timelion.fid).order_by(desc(func.sum(timelion.unum))).limit(50)	
result = session.query(timelion.fid, timelion.updatetime, func.extract('day', timelion.updatetime).label('day'), func.extract('hour', timelion.updatetime).label('h'), func.sum(timelion.unum)).filter(timelion.fid == "34").group_by('h', 'day').limit(50)
for r in result:
    pass
pass
# pass