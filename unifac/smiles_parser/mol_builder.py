'''
Created on 15-10-2012

@author: Jacek Przemieniecki
'''
from . import parser
from ..atom import Atom
from ..molecule import Molecule

class MolBuilder(object):
    
    def __init__(self):
        pass
    
    def _build_atom(self, atom_data):
        if atom_data[0] == "atom":
            atom = Atom(atom_data[1])
        
        elif atom_data[0] == "atom-hcount":
            atom = Atom(atom_data[1])
            atom.hydrogens = atom_data[2]
        
        elif atom_data[0] == "aromatic":
            atom = Atom(atom.data[1].upper(), aromatic=True)
        
        return atom
    
    def _interpret_chain(self, chain):
        first_atom = self._interpret_branched(chain[0])
        
        curr_atom = first_atom
        for node in chain[1:]:
            next_atom = self._interpret_branched(node)
            if not next_atom:
                continue    # node was a bond
            
            curr_atom.add_connected(next_atom, self.bond_next)
            curr_atom = next_atom
            self.bond_next = 1
        
        return first_atom
    
    def _interpret_branched(self, node):
        """
        returns first atom of a chain
        """

        if node[0] == "branched":
            first_atom = self._build_atom(node[1])
            
            if node[2] != []:
                for ringbond in node[2]:
                    self._add_to_ringbond(ringbond, first_atom)
            
            if node[3] != []:
                for branch in node[3]:  # branch looks like ("branch", ("bond", X), next_node)
                    first_atom.add_connected(self._interpret_chain(branch[2]), branch[1][1])
            
            return first_atom
        
        elif node[0] == "bond":
            self.bond_next = node[1]
        
        else:
            raise Exception()   # TODO: Exception Handling
 
    
    def build_smiles(self, smiles):
        self.ringbonds = {}
        self.bond_next = 1
        
        mol = Molecule()
        tree = parser.parse(smiles)
        
        first_atom = self._interpret_chain(tree)
        
        mol.add_atom(first_atom)
        
        return mol