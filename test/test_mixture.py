'''
Created on 16-10-2012

@author: Jacek Przemieniecki
'''
import unittest

from unifac.mixture import Mixture

class stub_mol(object):
    def __init__(self, groups):
        self.groups = groups
    
    def get_groups(self):
        return self.groups

class MixtureTest(unittest.TestCase):
    
    def setUp(self):
        self.mix = Mixture()
        
        self.mol1 = stub_mol({"CH3" : 2,
                              "CH2": 1,
                              "CH2NH" : 1})
        self.mol2 = stub_mol({"CH3" : 2,
                              "CH2" : 5})
        self.mix.add("Diethyloamine", self.mol1, 0.4)
        self.mix.add("Heptane", self.mol2, 0.6)
    
    def test_get_moles(self):
        result = self.mix.get_moles()
        expected = [self.mol1, self.mol2]
        
        for mol in result:
            self.assertIn(mol, expected)
    
    def test_get_groups(self):
        result = self.mix.get_groups()
        expected = {"CH3" : 2/5.8,
                    "CH2" : 3.4/5.8,
                    "CH2NH" : 0.4/5.8}
        for grp in result:
            self.assertAlmostEqual(result[grp], expected[grp])
    
    def test_get_mole_fractions(self):
        result = self.mix.get_mole_fractions()
        expected = [0.4, 0.6]
        for frac in result:
            self.assertIn(frac, expected)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_mix']
    unittest.main()