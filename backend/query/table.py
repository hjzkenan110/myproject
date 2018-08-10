from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, desc, func
from sqlalchemy.orm import sessionmaker
import datetime 

Base = declarative_base()

class timelion(Base):
    __tablename__ = 'timelion'

    url = Column(String(30), ForeignKey('info.url'), primary_key=True)
    tpostnum = Column(Integer)
    updatetime = Column(DateTime, primary_key=True)
    unum = Column(Integer)

    def __repr__(self):
        return 'url:{},updatetime:{},unum:{}'.format(self.url, self.updatetime, self.unum)


class info(Base):
    __tablename__ = 'info'

    url = Column(String(length=50),  primary_key=True)
    fname = Column(String(length=50))

    def __repr__(self):
        return 'url:{},fname:{}'.format(self.url, self.fname)


engine = create_engine('mysql+pymysql://itoffice:itoffice@192.168.127.129:3306/hp')
info.__table__
timelion.__table__
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()
# a = session.query(func.date_format(timelion.updatetime, '%Y-%m-%d').label('date'), func.count('*').label('cnt')).filter(...).group_by('date').all()
# print(a)
# print(type(a))
# pass
# session.query(timelion).filter(timelion.fid=='ddd').order_by(desc.desc(timelion.updatetime)).first()