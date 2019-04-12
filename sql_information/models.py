class Checkoff_sheet(db.Model):
        __tablename__ = 'checkoff_sheet'
        chk_name = Column('chk_name', String(45), primary_key = True)
        sname = Column('sname', String(45))
        #can I add an attribute here so that I can update it later with array of positions?


class Position:
   def __init__(self, categories):
      self.categories = categories #array of categories

class Category:
   def __init__(self, checkoffs):
      self.checkoffs = checkoffs #array of checkoffs

class Checkoff:
   def __init__(self, requirements):
      self.requirements = requirements #array of requirements

class Requirement:
   def __init__(self,attr):
          self.attr = attr;