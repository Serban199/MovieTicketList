
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# url-ul bazei de date va fi preluat dintr-o variabila de mediu
# pentru dezvoltare locala (fara docker momentan), ar putea arata asa:
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:secretpassword@localhost:5432/moviedb")

# cream motorul care comunica cu postgres
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# cream o clasa pentru sesiunile de baza de date
# autocommit=False si autoflush=False sunt setari standard pentru a avea control manual asupra tranzactiilor
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# clasa de baza pe care o vom folosi pentru a crea modelele noastre orm (tabelele)
Base = declarative_base()