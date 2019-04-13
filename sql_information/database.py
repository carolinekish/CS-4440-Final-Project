from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://orgt4440:finalproject4440@orgt4440.ccfdnjnpnqku.us-east-2.rds.amazonaws.com:3306/orgt_chechoffs', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)