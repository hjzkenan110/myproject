from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_session():
    engine = create_engine('mysql+pymysql://itoffice:itoffice@192.168.127.132:3306/hp')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session
