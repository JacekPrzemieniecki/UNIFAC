import unittest

from unifac import engine #@UnresolvedImport

class stub_mol(object):
    def __init__(self, groups):
        self.groups = groups
    
    def get_groups(self):
        return self.groups

class stub_mix(object):
    def __init__(self):
        mol1 = {"CH3" : 2,
                "CH2": 1, 
                "CH2NH" : 1}
        mol2 = {"CH3" : 2,
                "CH2" : 5}
        
        self.moles = [stub_mol(mol1), stub_mol(mol2)]
        self.quantities = [0.4, 0.6]
        
    def get_moles(self):
        return self.moles
    
    def get_groups(self):
        return {"CH3" : 2/5.8,
                "CH2" : 3.4/5.8,
                "CH2NH" : 0.4/5.8}
    
    def get_mole_fractions(self):
        return self.quantities



class stub_mix1(object):
    def __init__(self, x_et):
        mol1 = {"ACH" : 6}
        mol2 = {"CH3" : 1,
                "CH2" : 1,
                "OH" : 1}
        
        self.moles = [stub_mol(mol1), stub_mol(mol2)]
        self.quantities = [float(x_et), 1.0-x_et]
        
    def get_moles(self):
        return self.moles
    
    def get_groups(self):
        div = 6*self.quantities[0]+3*self.quantities[1]
        return {"ACH" : 6*self.quantities[0]/div,
                "CH3" : self.quantities[1]/div,
                "CH2": self.quantities[1]/div,
                "OH" : self.quantities[1]/div}
    
    def get_mole_fractions(self):
        return self.quantities


class stub_mix2(object):
    def __init__(self, x_et):
        mol1 = {"CH3" : 1,
                "CH2": 1, 
                "OH" : 1}
        mol2 = {"CH3" : 2,
                "CH2" : 1,
                "CH2O" : 1}
        
        self.moles = [stub_mol(mol1), stub_mol(mol2)]
        self.quantities = [float(x_et), 1.0-x_et]
        
    def get_moles(self):
        return self.moles
    
    def get_groups(self):
        div = 3*self.quantities[0]+4*self.quantities[1]
        return {"CH3" : (self.quantities[0]+2*self.quantities[1])/div,
                 "CH2" : 1/div,
                 "OH" : self.quantities[0]/div,
                 "CH2O": self.quantities[1]/div}
    
    def get_mole_fractions(self):
        return self.quantities

class stub_db(object):
    
    params = {"CH3" :{
                      "CH3" : 0.0,
                      "CH2" : 0.0,
                      "CH2NH" : 255.70,
                      "CH3CO" : 476.40,
                      "ACH" : 61.130,
                      "CH2O" : 251.50,
                      "OH" : 986.50},
              
              "CH2" :{
                      "CH3" : 0.0,
                      "CH2" : 0.0,
                      "CH2NH" : 255.70,
                      "CH3CO" : 476.40,
                      "ACH" : 61.130,
                      "CH2O" : 251.50,
                      "OH" : 986.50},
              
              "CH2NH" :{
                        "CH3" : 65.330,
                        "CH2" : 65.330,
                        "CH2NH" : 0.0,
                        "CH3CO" : 394.60,
                        "CH2O" : 222.10,
                        "OH" : -150.00},
              
              "CH3CO" :{
                        "CH3" : 26.76,
                        "CH2" : 26.76,
                        "CH2NH" : -174.20,
                        "CH3CO" : 0.0,
                        "ACH" : 140.100,
                        "CH2O" : -103.60,
                        "OH" : 164.50},
              
              "ACH" :{
                      "CH3" : -11.120,
                      "CH2" : -11.120,
                      "CH3CO" : 25.770,
                      "ACH" : 0.0,
                      "OH" : 636.100},
              
              "OH" :{
                     "CH3" : 156.40,
                     "CH2" : 156.40,
                     "CH2NH" : 42.700,
                     "CH3CO" : 84.000,
                     "ACH" : 89.600,
                     "CH2O" : 28.060,
                     "OH" : 0.0},
              
              "CH2O" : {
                        "CH3" : 83.360,
                        "CH2" : 83.360,
                        "CH2O" : 0.0,
                        "OH" : 237.700}
              }
    
    q_r_table = {"CH3" : (0.848, 0.9011),
                 "CH2" : (0.540, 0.6744),
                 "CH2NH" : (0.936, 1.2070),
                 "CH3CO" : (1.448, 1.6724),
                 "ACH" : (0.400, 0.5313),
                 "CH2CO" : (1.180, 1.4457),
                 "CH2O" : (0.780, 0.9183),
                 "OH" : (1.2, 1.0)}
    def get_q_r(self, symbol):
        return self.q_r_table[symbol]
    
    def get_parameter(self, symbol1, symbol2):
        return self.params[symbol1][symbol2]

class EngineTest(unittest.TestCase):
    
    
    
    def setUp(self):
        self.test_mix = stub_mix()
        db = stub_db()
        self.engine = engine.Engine(self.test_mix, db)
    
    def test_init(self):
        self.assertEqual(len(self.engine._moles), 2)
        self.assertEqual(len(self.engine._groups), 3)
        
    def test_temperature(self):
        self.assertEqual(self.engine.get_temperature(), 273)
        self.engine.set_temperature(300.53)
        self.assertEqual(self.engine.get_temperature(), 300.53)
        self.assertRaises(ValueError, self.engine.set_temperature, -5)
        self.assertRaises(ValueError, self.engine.set_temperature, 0)
        
    def test_calc_combinatorial(self):
        self.engine.set_temperature(308.15)
        self.engine._calc()
        self.assertAlmostEqual(self.engine._combinatorial[0]*1000, -21.347, places=2)
        self.assertAlmostEqual(self.engine._combinatorial[1]*1000, -7.6016, places=3)
    
    def test_calc_residual(self):
        self.engine.set_temperature(308.15)
        self.engine._calc()
        self.assertAlmostEqual(self.engine._residual[0]*10, 1.4630, places=2)
        self.assertAlmostEqual(self.engine._residual[1]*10, 0.53583, places=3)
    
    def test_calc(self):
        self.engine.set_temperature(308.15)
        val = self.engine.get_activity_coeff(self.test_mix.get_moles()[0])
        val1 = self.engine.get_activity_coeff(self.test_mix.get_moles()[1])
        self.assertAlmostEqual(val, 1.133, places=3)
        self.assertAlmostEqual(val1, 1.047, places=3)
        
        
    def test_calc1(self):
        res = {0.05 : 4.3403, # x_benzene : activity_coeff_benzene
               0.10 : 3.8329,
               0.15 : 3.4022,
               0.20 : 3.0352,
               0.25 : 2.7210,
               0.30 : 2.4512,
               0.35 : 2.2186
               }
        db = stub_db()
        for x_et in res:
            test_mix = stub_mix1(x_et)
            eng = engine.Engine(test_mix, db)
            eng.set_temperature(300)
            coef = eng.get_activity_coeff(test_mix.get_moles()[0])
            self.assertAlmostEqual(coef, res[x_et], places=2)
     
    def test_calc2(self):
        res = {0.05 : 3.5090, # x_ethanol : activity_coeff_ethanol
               0.10 : 2.9066,
               0.15 : 2.4744,
               0.20 : 2.1543,
               0.25 : 1.9108,
               0.30 : 1.7218,
               0.35 : 1.5726
               }
        db = stub_db()
        for x_et in res:
            test_mix = stub_mix2(x_et)
            eng = engine.Engine(test_mix, db)
            eng.set_temperature(300)
            coef = eng.get_activity_coeff(test_mix.get_moles()[0])
            self.assertAlmostEqual(coef, res[x_et], places=4)


   


if __name__ == '__main__':
    unittest.main()
