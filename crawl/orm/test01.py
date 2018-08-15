import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://itoffice:itoffice@localhost:3306/hp')

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50))
    fullname = Column(String(length=50))
    password = Column(String(length=50))
    
    # def __repr__(self):
    #     return "<User(name='%s', fullname='%s', password='%s')>" % (
    #                             self.name, self.fullname, self.password)


User.__table__
Base.metadata.create_all(engine)

# DBSession = sessionmaker(bind=engine)
# session = DBSession()
# new_user = User(id='5', name='Bob')
# session.query(User).filter(User.name.in_(['jingqi','jingqi1'])).all()