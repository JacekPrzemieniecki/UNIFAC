'''
Created on 11-10-2012

@author: Jacek Przemieniecki
'''

from . import database

class Atom(object):
    """
    Atom class to be used as molecule.Molecule graph nodes
    Instance created with Atom(symbol)
    """
    
    def __init__(self, symbol, aromatic=False):
        self.symbol = symbol
        self.connected = []
        self.bonds = []
        self.aromatic = aromatic
        db = database.Database()
        self.valency = db.get_atom_valency(symbol)
        
        self._exp_hydrogens = None
        self._has_exp_hydrogens = False
        
        
    def add_connected(self, atom, bond_order=1):
        if not atom in self.connected:
            self.connected.append(atom)
            self.bonds.append(bond_order)
            atom.add_connected(self, bond_order)
    
    @property
    def hydrogens(self):
        if self._has_exp_hydrogens:
            return self._exp_hydrogens
        else:
            return self.valency - sum(self.bonds)
    
    @hydrogens.setter
    def hydrogens(self, value):
        self._exp_hydrogens = value
        self._has_exp_hydrogens = True
        