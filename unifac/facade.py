'''
Created on 16-10-2012

@author: Jacek Przemieniecki
'''

from .mixture import Mixture
from .smiles_parser.mol_builder import MolBuilder
from .engine import Engine

class Facade(object):
    '''
    Privides API for UNIFAC model
    '''
    
    def __init__(self):
        self.mixture = Mixture()
        self._calculated = False
        self._temp = 273.0
        
    
    def add_molecule_smiles(self, smiles, amount):
        builder = MolBuilder()
        mol = builder.build_smiles(smiles)
        
        self.mixture.add(smiles, mol, amount)
    
    def get_coeff(self, iden):
        if not self._calculated:
            self.engine = Engine(self.mixture)
            self.engine.set_temperature(self._temp)
        
        mol = self.mixture.moles[iden]
        return self.engine.get_activity_coeff(mol)
    
    def reset_solution(self):
        self.mixture = Mixture()
        self.engine = None
        self._calculated = False
        self._temp = 273.0
        
    def set_temperature(self, temp):
        self._temp = temp