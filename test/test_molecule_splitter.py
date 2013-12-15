'''
Created on 12-10-2012

@author: Jacek Przemieniecki
'''
import unittest
import itertools

from Unifac.unifac import database
from Unifac.unifac.mol_splitter import group_parser
from Unifac.unifac.mol_splitter import molecule_splitter

from Unifac.unifac.atom import Atom

class stub_mol(object):
    
    def __init__(self, atoms):
        self.atoms = atoms

class ParserTest(unittest.TestCase):
    def test_parser1(self):
        result = group_parser.parse("CH3NH2")
        expected = ("node",
                    ("ext-atom",
                     ("atom", "C"),
                     [("hydrogen", 3)]),
                    ("next",
                     1,
                     ("node",
                      ("ext-atom",
                       ("atom", "N"),
                       [("hydrogen", 2)]),
                      None)))
        self.assertEqual(result, expected)
        
    def test_parser2(self):
        result = group_parser.parse("CHN(=O)=O")
        expected = ("node",
                    ("ext-atom",
                     ("atom", "C"),
                     [("hydrogen", 1)]),
                    ("next",
                     1,
                     ("node",
                      ("ext-atom",
                       ("atom", "N"),
                       [("next", 
                        2,
                        ("node",
                         ("atom", "O"),
                         None))]),
                      ("next",
                       2,
                       ("node",
                        ("atom", "O"),
                        None)))))
        self.assertEqual(result, expected)
    
    def test_parser_on_database(self):
        db = database.Database()
        for group_string in db.iterate_strings():
            group_parser.parse(group_string)

class AuxiliaryFuncTest(unittest.TestCase):
    
    def setUp(self):
        self.atomC1 = Atom("C")
        self.atomC2 = Atom("C")
        self.atomC3 = Atom("C")
        self.atomO = Atom("O")
        self.atomN = Atom("N")
    
    def test_match_atom_to_node(self):
        result = (molecule_splitter._match_atom_to_node(self.atomC1, ("ext-atom", ("atom", "C"), [("hydrogen", 4)])))
        expected = (True, None)
        self.assertEqual(result, expected)
        self.atomC1.add_connected(Atom("Cl"))
        self.atomC1.add_connected(Atom("Cl"))
        result = (molecule_splitter._match_atom_to_node(self.atomC1, ("ext-atom", ("atom", "C"), [("hydrogen", 2), ("halogen", "Cl", 2)])))
        expected = (True, None)
        self.assertEqual(result, expected)
    
    def test_crawl(self):
        self.atomC1.add_connected(self.atomC2, 2)
        result = molecule_splitter._crawl(self.atomC1,("node", ("ext-atom", ("atom", "C"), [("hydrogen", 2)]), ("next", 2, ("node", ("ext-atom", ("atom", "C"), [("hydrogen", 2)]), None))), [])
        expected = [self.atomC1, self.atomC2]
        expected_alt = [self.atomC2, self.atomC1]
        self.assertTrue(result == expected or result == expected_alt)
       
    def test_crawl_2(self):
        self.atomC1.add_connected(self.atomO, 2)
        self.atomC1.add_connected(self.atomN)
        result = molecule_splitter._crawl(self.atomC1, ("node", 
                                                        ("ext-atom", 
                                                         ("atom", "C"),
                                                         [("next", 
                                                           2, 
                                                           ("node",
                                                            ("atom", "O"), 
                                                            None))]), 
                                                        ("next", 
                                                         1, 
                                                         ("node", 
                                                          ("ext-atom", 
                                                           ("atom", "N"), 
                                                           [("hydrogen", 2)]), 
                                                          None)), 
                                                        None),
                                          [])
        expected = list(itertools.permutations([self.atomC1, self.atomN, self.atomO]))
        self.assertIn(tuple(result), expected)
        
    def test_look_for_group(self):
        self.atomN.add_connected(self.atomC3)
        self.atomC3.add_connected(self.atomC2)
        self.atomC2.add_connected(self.atomC1, 2)
        
        result = molecule_splitter._look_for_group("CH2=CH", [self.atomC1, self.atomC2, self.atomC3, self.atomN], {"C" : [0, 1, 2], "N" : 3})
        expected = [[0, 1]]
        self.assertEqual(result, expected)
        
        result = molecule_splitter._look_for_group("CH2NH2", [self.atomC1, self.atomC2, self.atomC3, self.atomN], {"C" : [0, 1, 2], "N" : 3})
        expected = [[2, 3]]
        self.assertEqual(result, expected)
    
    def test_look_for_group1(self):
        self.atomC1.add_connected(self.atomC2)
        self.atomC1.add_connected(self.atomC3)
        self.atomC1.add_connected(self.atomN)
        self.atomC1.add_connected(self.atomO)
        
        result = molecule_splitter._look_for_group("CH0", [self.atomC1, self.atomC2, self.atomC3, self.atomN], {"C" : [0, 1, 2], "N" : 3})
        expected = [[0]]
        
        self.assertEqual(result, expected)

class SplitterTest(unittest.TestCase):
    
    def setUp(self):
        # construct propenamine
        self.atomC1 = Atom("C")
        self.atomC2 = Atom("C")
        self.atomC3 = Atom("C")
        self.atomN = Atom("N")
        self.atomO = Atom("O")
        
    def test_split(self):
        self.atomN.add_connected(self.atomC3)
        self.atomC3.add_connected(self.atomC2)
        self.atomC2.add_connected(self.atomC1, 2)
        mol = stub_mol([self.atomC1, self.atomC2, self.atomC3, self.atomN])
        result = molecule_splitter.split(mol)
        expected = {"CH2=CH" : 1,
                    "CH2NH2" : 1}
        self.assertEqual(result, expected)
    
    def test_split1(self):
        # construct propan-2-ole
        self.atomC1.add_connected(self.atomO)
        self.atomC1.add_connected(self.atomC2)
        self.atomC1.add_connected(self.atomC3)
        mol = stub_mol([self.atomC1, self.atomC2, self.atomC3, self.atomO])
        
        result = molecule_splitter.split(mol)
        expected = {"CH3" : 2,
                    "CH" : 1,
                    "OH" : 1}
        self.assertEqual(result, expected)
    
    def test_split2(self):
        # construct cyclobutane
        atomC = Atom("C")
        atomC.add_connected(self.atomC1)
        self.atomC1.add_connected(self.atomC2)
        self.atomC2.add_connected(self.atomC3)
        self.atomC3.add_connected(atomC)
        mol = stub_mol([self.atomC1,atomC, self.atomC2, self.atomC3])
        
        result = molecule_splitter.split(mol)
        expected = {"CH2" : 4}
        self.assertEqual(result, expected)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
