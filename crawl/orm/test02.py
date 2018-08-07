import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import PrimaryKeyConstraint

Base = declarative_base()

class timelion(Base):
    __tablename__ = 'timelion'

    fid = Column(String(length=50), primary_key=True)
    tpostnum = Column(Integer)
    tid = Column(String(length=50))
    releasetime = Column('timestamp', sa.DateTime(), nullable=True, primary_key=True)
    unum = Column(Integer)

    def __repr__(self):
        return 'fid:{},releasetime:{},unum:{}'.format(self.fid, self.releasetime, self.unum)



engine = create_engine('mysql+pymysql://root:@localhost:3306/hp')
timelion.__table__
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()
session.query(timelion).filter(timelion.fid=='ddd').order_by(sa.desc(timelion.releasetime)).first()