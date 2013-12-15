'''
Created on 10-10-2012

@author: jacek
'''
import unittest

from Unifac.unifac import database
from Unifac.unifac import errors

class DatabaseTest(unittest.TestCase):

    def setUp(self):
        self.db = database.Database()
    
    def test_get_q_r(self):
        db = self.db
        
        self.assertEqual(db.get_q_r("CH3"), (0.848, 0.9011))
        self.assertEqual(db.get_q_r("OH"), (1.2, 1.0))
        self.assertRaises(KeyError, db.get_q_r, "No Such Thing")
    
    def test_get_parameter(self):
        db = self.db
        
        self.assertEqual(db.get_parameter("CH3", "CH3"), 0.0)
        self.assertEqual(db.get_parameter("CH2", "OH"), 986.50)
        self.assertEqual(db.get_parameter("OH", "CH2"), 156.40)
        self.assertRaises(errors.ValueNotFound, db.get_parameter, "CH0OCH0", "ACCl")



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()