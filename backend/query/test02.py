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


engine = create_engine('mysql+pymysql://itoffice:itoffice@192.168.127.129:3306/test')
#timelion.__table__
#info.__table__
#Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()
# result = session.query(timelion.fid, func.sum(timelion.unum)).filter(timelion.updatetime<now_time, timelion.updatetime>yes_time).group_by(timelion.fid).order_by(desc(func.sum(timelion.unum))).limit(50)	
# result = session.query(timelion.fid, timelion.updatetime, func.extract('day', timelion.updatetime).label('day'), func.extract('hour', timelion.updatetime).label('h'), func.sum(timelion.unum)).filter(timelion.fid == "34").group_by('day','h').limit(50)
# for r in result:
#     pass
# pass
# pass

# month = func.extract('month', timelion.updatetime).label('month')
# day = func.extract('day', timelion.updatetime).label('day')
# hour = func.extract('hour', timelion.updatetime).label('hour')
# unum = func.sum(timelion.unum)

# results = session.query(timelion.updatetime, func.sum(timelion.unum), month, day, hour).filter(timelion.fid == "34").order_by(desc(timelion.updatetime)).group_by('hour').limit(50)
# results = session.query(
#             timelion.fid, 
#             timelion.updatetime, 
#             month, 
#             day, 
#             hour, 
#             unum
#         ).group_by('hour', 'day').filter(timelion.fid == "34").all()

# for result in results:
#     time = str(result[1])[:-3]
#     a = {"fid": result[0], 'updatetime': time, "unum": int(result[5])}
#     pass
