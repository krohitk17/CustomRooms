from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///database/guilds.sqlite', echo=False)
localsession = sessionmaker(bind=engine)
base = declarative_base()
