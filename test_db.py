from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///demo.db')

Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

Base.metadata.create_all(engine)

maria = User(name="Maria", age=19)
oleg = User(name="Олег", age=22)
session.add_all([maria, oleg])
session.commit()

users = session.query(User).all()
print(users)
