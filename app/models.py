from sqlalchemy import Column, Integer, String
from .database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    size=Column(Integer)
    type=Column(String)
    filepath = Column(String)
  
  
    def __str__(self):
      return self.filename
