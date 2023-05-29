from datetime import datetime

from sqlalchemy import Column, Integer, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///photoinfo.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class PhotoInfo(Base):
    __tablename__ = 'photo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.now())
    size = Column(Integer)


Base.metadata.create_all(engine)