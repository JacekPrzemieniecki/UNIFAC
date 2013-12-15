'''
Created on 11-10-2012

@author: Jacek Przemieniecki
'''
import unittest

from Unifac.unifac import atom

class AtomTest(unittest.TestCase):

    def setUp(self):
        self.atom = atom.Atom("C")
        
    def test_create(self):
        self.assertEqual(self.atom.symbol, "C")
    
    def test_add_connected(self):
        new_atom = atom.Atom("O")
        self.atom.add_connected(new_atom)
        self.assertEqual(self.atom.connected, [new_atom])
        self.assertEqual(new_atom.connected, [self.atom])
    
    def test_hydrogens(self):
        self.assertEqual(self.atom.hydrogens, 4)
        
        new_atom = atom.Atom("O")
        self.atom.add_connected(new_atom)
        self.assertEqual(self.atom.hydrogens, 3)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()