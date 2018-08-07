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


engine = create_engine('mysql+pymysql://itoffice:itoffice@192.168.127.129:3306/test')
timelion.__table__
info.__table__
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()
# a = session.query(func.date_format(timelion.updatetime, '%Y-%m-%d').label('date'), func.count('*').label('cnt')).filter(...).group_by('date').all()
# print(a)
# print(type(a))
# pass
# session.query(timelion).filter(timelion.fid=='ddd').order_by(desc.desc(timelion.updatetime)).first()