from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    # relatia cu biletele rezervate de acest user
    tickets = relationship("Ticket", back_populates="owner")

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    external_id = Column(String, unique=True) # id-ul de la omdb
    
    # relatia cu biletele pentru acest film
    tickets = relationship("Ticket", back_populates="movie")

class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    reservation_date = Column(DateTime)
    
    # legaturile inverse catre user si movie
    owner = relationship("User", back_populates="tickets")
    movie = relationship("Movie", back_populates="tickets")