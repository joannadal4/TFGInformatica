from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class ModelVPF(Base):
   __tablename__ = 'model'
   idModel = Column(Integer, primary_key = True)
   code = Column(String(100), nullable = False)
   path = Column(String(500), nullable = False)

   proteins = relationship("Protein")

   def __repr__(self):
        return "<ModelVPF(code='%s')>" % (self.code)

class Species(Base):
   __tablename__ = 'species'
   idSpecies = Column(Integer, primary_key = True)
   name = Column(String(50), nullable = False)
   taxonomy = Column(String(20), nullable = False)
   isVirus = Column(Boolean, nullable = False)

   proteins = relationship('Protein')

   def __repr__(self):
        return "<Species(name='%s', taxonomy = '%s', isVirus = '%s')>" % (self.name, self.taxonomy, self.isVirus)

class Protein(Base):
   __tablename__ = 'protein'
   idProtein = Column(Integer, primary_key = True)
   code = Column(String(15), nullable = False)
   name = Column(String(50), nullable = False)
   gene = Column(String(15), nullable = False)
   location = Column(String(100), nullable = False)
   idSpecies = Column(Integer, ForeignKey('species.idSpecies'))

   functions = relationship('Function', secondary = 'r_protein_function')

   proteinsV = relationship('Function', secondary = 'interaction')
   proteinsH = relationship('Function', secondary = 'interaction')

   def __repr__(self):
        return "<Protein(code='%s', name = '%s', gene = '%s', location = '%s', idSpecies = '%s')>" % (self.code, self.name, self.gene, self.location, self.idSpecies)


class Function(Base):
   __tablename__ = 'function'
   idFunction = Column(Integer, primary_key = True)
   codeGO = Column(String(15), nullable = False)
   description = Column(String(200), nullable = False)
   aspect = Column(String(30), nullable = False)

   proteins = relationship('Protein', secondary = 'r_protein_function')

   def __repr__(self):
        return "<Specie(codeGO='%s', description = '%s', aspect = '%s')>" % (self.codeGO, self.description, self.aspect)


class R_Protein_Function(Base):
   __tablename__ = 'r_protein_function'

   idProtein = Column(
      Integer,
      ForeignKey('protein.idProtein'),
      primary_key = True)

   idFunction = Column(
      Integer,
      ForeignKey('function.idFunction'),
      primary_key = True)


class Interaction(Base):
   __tablename__ = 'interaction'

   idProteinV = Column(
      Integer,
      ForeignKey('protein.idProtein'),
      primary_key = True)

   idProteinH = Column(
      Integer,
      ForeignKey('protein.idProtein'),
      primary_key = True)


class R_Protein_ModelVPF(Base):
   __tablename__ = 'r_protein_modelVPF'

   idProtein = Column(
      Integer,
      ForeignKey('protein.idProtein'),
      primary_key = True)

   idModel = Column(
      Integer,
      ForeignKey('model.idModel'),
      primary_key = True)

   score = Column(Float, nullable = False)

   models = relationship("ModelVPF")
