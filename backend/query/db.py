from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_session():
    engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/hp')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session
