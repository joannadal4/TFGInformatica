from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Boolean, Float, Index, Text, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class R_Protein_ModelVPF(Base):
   __tablename__ = 'r_protein_modelvpf'

   idProtein = Column(Integer, ForeignKey('protein.idProtein'), primary_key = True)
   idModel = Column(Integer, ForeignKey('model.idModel'),primary_key = True)
   score = Column (Float, nullable = True)
   e_value = Column (Float, nullable = True)

   model = relationship('ModelVPF', back_populates= 'proteins')
   protein = relationship('Protein', back_populates= 'models')

class ModelVPF(Base):
   __tablename__ = 'model'
   idModel = Column(Integer, primary_key = True)
   code = Column(String(100), nullable = False, unique = True)
   path = Column(String(500), nullable = False)

   proteins = relationship('R_Protein_ModelVPF', back_populates= 'model')

   def __repr__(self):
        return "<ModelVPF(code='%s')>" % (self.code)

class Species(Base):
   __tablename__ = 'species'
   idSpecies = Column(Integer, primary_key = True)
   name = Column(String(100), nullable = False, unique = True)
   taxonomy = Column(String(100), nullable = False)
   isVirus = Column(Boolean, nullable = False)

   proteins = relationship('Protein')

   def __repr__(self):
        return "<Species(name='%s', taxonomy = '%s', isVirus = '%s')>" % (self.name, self.taxonomy, self.isVirus)


R_Protein_Function = Table('r_protein_function', Base.metadata,
    Column('idProtein', Integer, ForeignKey('protein.idProtein'), nullable = False),
    Column('idFunction', Integer, ForeignKey('function.idFunction'), nullable = False)
)

Interaction = Table('interaction', Base.metadata,
    Column('idProteinV', Integer, ForeignKey('protein.idProtein'), nullable = False),
    Column('idProteinH', Integer, ForeignKey('protein.idProtein'), nullable = False)
)

class Protein(Base):
   __tablename__ = 'protein'
   idProtein = Column(Integer, primary_key = True)
   codeUniprot = Column(String(15), nullable = False, unique = True)
   codeString = Column(String(30), nullable = True, unique = True)
   name = Column(String(500), nullable = False)
   gene = Column(String(50), nullable = True)
   location = Column(Text, nullable = True)
   idSpecies = Column(Integer, ForeignKey('species.idSpecies'))

   functions = relationship("Function",secondary=R_Protein_Function, back_populates='proteins')

   models = relationship('R_Protein_ModelVPF', back_populates='protein')

   proteinsV = relationship("Protein",secondary=Interaction, back_populates='proteinsH')
   proteinsH = relationship("Protein",secondary=Interaction, back_populates='proteinsV')

   def __repr__(self):
        return "<Protein(codeUniprot='%s', codeString='%s', name = '%s', gene = '%s', location = '%s', idSpecies = '%s')>" % (self.codeUniprot, self.codeString, self.name, self.gene, self.location, self.idSpecies)

protein_idSpecies_index = Index('protein_idSpecies_index', Protein.idSpecies)

class Inaccessible_Protein(Base):
    __tablename__ = 'inaccessible_protein'
    idProtein = Column(Integer, primary_key = True)
    codeUniprot = Column(String(15), nullable = False, unique = True)
    codeString = Column(String(30), nullable = True, unique = True)

    def __repr__(self):
        return "<Protein(codeUniprot='%s', codeString='%s')>" % (self.codeUniprot, self.codeString)

class Function(Base):
   __tablename__ = 'function'
   idFunction = Column(Integer, primary_key = True)
   codeGO = Column(String(15), nullable = False, unique = True)
   description = Column(Text, nullable = False)
   aspect = Column(String(100), nullable = True)

   proteins = relationship("Protein",secondary=R_Protein_Function, back_populates= 'functions')

   def __repr__(self):
        return "<Specie(codeGO='%s', description = '%s', aspect = '%s')>" % (self.codeGO, self.description, self.aspect)
