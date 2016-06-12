'''
Created on 11-10-2012

@author: Jacek Przemieniecki
'''
import unittest

from unifac import molecule

from unifac.atom import Atom


class MoleculeTest(unittest.TestCase):
    
    def setUp(self):
        self.mol = molecule.Molecule()
        self.atomC = Atom("C")
        self.atomN = Atom("N")
        self.atomN.add_connected(self.atomC)
        
        self.atomO = Atom("O")

    def test_add(self):
        mol = self.mol
        
        mol.add_atom(self.atomC)
        mol.add_atom(self.atomN)
        
        self.assertTrue(mol.atoms == [self.atomC, self.atomN] or mol.atoms == [self.atomN, self.atomC])
        
        mol.add_atom(self.atomC) #nothing should happen, since this atom is already in the molecule)
        self.assertTrue(mol.atoms == [self.atomC, self.atomN] or mol.atoms == [self.atomN, self.atomC])
    
    # Integrity test, actually testing molecule_splitter
    def test_get_groups(self):
        mol = self.mol
        mol.add_atom(self.atomC)
        mol.add_atom(self.atomN)
        
        result = mol.get_groups()
        expected = {"CH3NH2" : 1}
        self.assertEqual(result, expected)
        


if __name__ == "__main__":
    unittest.main()