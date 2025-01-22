from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pytz

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.utc))

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)
    game_id = Column(Integer, unique=True, index=True)
    season = Column(String(10), index=True)
    game_type = Column(Integer, index=True)
    venue = Column(String(100))
    neutral_site = Column(String(10))
    start_time = Column(DateTime)
    home_team = Column(String(50))
    home_team_score = Column(Integer)
    away_team = Column(String(50))
    away_team_score = Column(Integer)
    game_state = Column(String(20))
    game_center_link = Column(String(120))



