'''
Created on 13-10-2012

@author: Jacek Przemieniecki
'''
import unittest

from unifac.molecule import Molecule
from unifac.smiles_parser import parser
from unifac.smiles_parser.mol_builder import MolBuilder

class ParserTest(unittest.TestCase):
    
    def test_parser1(self):
        result = parser.parse("CCCO")
        expected = [("branched", ("atom", "C"), [], []), ("branched", ("atom", "C"), [], []), ("branched", ("atom", "C"), [], []), ("branched", ("atom", "O"), [], [])]
        self.assertEqual(result, expected)
        
    def test_parser2(self):
        result = parser.parse("C=C")
        expected = [("branched", ("atom", "C"), [], []), ("bond", 2), ("branched", ("atom", "C"), [], [])]
        self.assertEqual(result, expected)
    
    def test_parser3(self):
        result = parser.parse("CC(=O)C")
        expected = [("branched", ("atom", "C"), [], []), ("branched", ("atom", "C"), [], [("branch", ("bond", 2), [("branched", ("atom", "O"), [], [])])]), ("branched", ("atom", "C"), [], [])]
        self.assertEqual(result, expected)


class BuilderTest(unittest.TestCase):
    
    def setUp(self):
        self.builder = MolBuilder()

    def test_builder1(self):
        
        result = self.builder.build_smiles("CCCO")
        self.assertIsInstance(result, Molecule)
        self.assertNotEqual(result.atoms, [])
        
        atomO = [atom for atom in result.atoms if atom.symbol == "O"][0]
        atomC1 = atomO.connected[0]
        self.assertEqual(atomC1.symbol, "C")
        self.assertEqual(len(atomC1.connected), 2)
        
        atomC2 = [atom for atom in atomC1.connected if atom != atomO][0]
        self.assertEqual(atomC2.symbol, "C")
        self.assertEqual(len(atomC2.connected), 2)
        
        atomC3 = [atom for atom in atomC2.connected if atom != atomC1][0]
        self.assertEqual(atomC3.symbol, "C")
        self.assertEqual(len(atomC3.connected), 1)
    
    def test_builder2(self):
        
        result = self.builder.build_smiles("CC(=O)C")
        
        self.assertIsInstance(result, Molecule)
        self.assertNotEqual(result.atoms, [])
        
        atomO = [atom for atom in result.atoms if atom.symbol == "O"][0]
        atomC1 = atomO.connected[0]
        self.assertEqual(atomC1.symbol, "C")
        self.assertEqual(len(atomC1.connected), 3)
        
        other_C_atoms = [atom for atom in atomC1.connected if atom.symbol != "O"]
        
        for atomC in other_C_atoms:
            self.assertEqual(atomC.symbol, "C")
            self.assertEqual(len(atomC.connected), 1)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()