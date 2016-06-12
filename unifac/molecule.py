'''
Created on 11-10-2012

@author: Jacek Przemieniecki
'''

from .mol_splitter import molecule_splitter

class Molecule(object):
    '''
    Represents chemical molecules as graphs of atom.Atom instances
    '''


    def __init__(self):
        self.atoms = []
        self.groups = {}
        self.finalized = False
    
    def add_atom(self, atom):
        if self.finalized:
            raise Exception()       # TODO: Exception handling
        if not atom in self.atoms:
            self.atoms.append(atom)
            for to_con in atom.connected:
                self.add_atom(to_con)
    
    def get_groups(self):
        if not self.finalized:
            self.groups = molecule_splitter.split(self)
            self.finalized = True

        return self.groups