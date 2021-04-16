import db

from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship


class ModelVPF(db.Base):
   __tablename__ = 'model'
   idModel = Column(Integer, primary_key = True)
   code = Column(String(100), nullable = False)

   proteins = relationship("Protein")

   def __repr__(self):
        return "<ModelVPF(code='%s')>" % (self.code)

class Specie(db.Base):
   __tablename__ = 'specie'
   idSpecie = Column(Integer, primary_key = True)
   name = Column(String(50), nullable = False)
   taxonomy = Column(String(20), nullable = False)
   isVirus = Column(String(3), nullable = False)

   proteins = relationship('Protein')

   __table_args__ = (
        CheckConstraint(isVirus.in_(['Yes', 'No'])),
    )

   def __repr__(self):
        return "<Specie(name='%s', taxonomy = '%s', isVirus = '%s')>" % (self.name, self.taxonomy, self.isVirus)

class Protein(db.Base):
   __tablename__ = 'protein'
   idProtein = Column(Integer, primary_key = True)
   code = Column(String(15), nullable = False)
   name = Column(String(50), nullable = False)
   gene = Column(String(15), nullable = False)
   location = Column(String(100), nullable = False)
   idSpecie = Column(Integer, ForeignKey('specie.idSpecie'))

   functions = relationship('Function', secondary = 'r_protein_function')

   proteinsV = relationship('Function', secondary = 'r_protein_protein')
   proteinsH = relationship('Function', secondary = 'r_protein_protein')

   def __repr__(self):
        return "<Protein(code='%s', name = '%s', gene = '%s', location = '%s', idSpecie = '%s')>" % (self.code, self.name, self.gene, self.location, self.idSpecie)


class Function(db.Base):
   __tablename__ = 'function'
   idFunction = Column(Integer, primary_key = True)
   codeGO = Column(String(15), nullable = False)
   description = Column(String(200), nullable = False)
   aspect = Column(String(30), nullable = False)

   proteins = relationship('Protein', secondary = 'r_protein_function')

   def __repr__(self):
        return "<Specie(codeGO='%s', description = '%s', aspect = '%s')>" % (self.codeGO, self.description, self.aspect)


class R_Protein_Function(db.Base):
   __tablename__ = 'r_protein_function'

   idProtein = Column(
      Integer,
      ForeignKey('protein.idProtein'),
      primary_key = True)

   idFunction = Column(
      Integer,
      ForeignKey('function.idFunction'),
      primary_key = True)


class R_Protein_Protein(db.Base):
   __tablename__ = 'r_protein_protein'

   idProteinV = Column(
      Integer,
      ForeignKey('protein.idProtein'),
      primary_key = True)

   idProteinH = Column(
      Integer,
      ForeignKey('protein.idProtein'),
      primary_key = True)


class R_Protein_ModelVPF(db.Base):
   __tablename__ = 'r_protein_modelVPF'

   idProtein = Column(
      Integer,
      ForeignKey('protein.idProtein'),
      primary_key = True)

   idModel = Column(
      Integer,
      ForeignKey('model.idModel'),
      primary_key = True)

   score = Column(Integer, nullable = False)

   models = relationship("ModelVPF")
