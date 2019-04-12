from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime
# models.py is only necessary if you want to add things to the database through python rebel manually (I can use MySQL workbench for that)

class Checkoff_sheet(Base):
   __tablename__ = 'checkoff_sheet'
   chk_name = Column('chk_name', String(45), primary_key = True)
   sname = Column('sname', String(30))
   #can I add an attribute here so that I can update it later with array of positions?

   def __init__(self, checkoff_name, sport_name):
      self.chk_name = checkoff_name
      self.sname = sport_name

class Position:
   __tablename__ = 'position'
   name = Column('name', String(45), primary_key = True)
   abbreviation = Column('abbreviation', String(5))
   
   def __init__(self, name, abbrv):
      self.name=name
      self.abbreviation=abbrv
      

class Staff:
   __tablename__ = 'staff_members'
   member_id = Column('member_id', Integer(11), primary_key = True)
   name = Column('name', String(5))
   position_title = Column('position_title', String(5))
   
   def __init__(self, memberID, name, position):
      self.member_id=memberID
      self.name=name
      self.position_title=position


      