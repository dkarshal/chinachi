from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean

from database import Base


class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    director = Column(String)

class Student(Base):
    __tablename__ = "student"

    ID = Column(Integer, primary_key=True)
    DisplayNameAll = Column(String, nullable=False)
    PostName = Column(String, nullable=False)
    DivisionName = Column(String, nullable=False)
    # MinIn = Column(DateTime)
    # MaxIn = Column(DateTime)
    # MaxOut = Column(DateTime)
    Status = Column(Boolean, default=False, nullable=False)
    # DayOut = Column(DateTime)
    DaysNoInScool = Column(Integer)
    DaysNoOutScool = Column(Integer)
    Manager = Column(String, nullable=False)

    def __repr__(self):
        return " ".join({"DisplayNameAll: " + self.DisplayNameAll + ", DivisionName: " + self.DivisionName + ", Status " + str(self.Status)})
