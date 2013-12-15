'''
Created on 08-10-2012

@author: Jacek Przemieniecki
'''

from math import log as ln, exp, fsum

from . import database 

class Engine(object):
    """
    Executes calculations for the UNIFAC model
    provides activity coefficients for molecules
    inside mix argument
    """
    def __init__(self, mix, db=database.Database()):
        """
        mix is instance of molecule.Molecule
        db i instance of database.Database
        defaults to new Database object if no db is provided
        """
        
        # Determines if values need to be recalculated before
        # access to activity coefficients
        self._calculated = False     
        self._combinatorial_calculated = False                        
        self._moles = mix.get_moles()                       # [mol1, mol2, ...]; mol.get_groups() = {"group_symbol" : amount, ...}
        self._groups = mix.get_groups()                     # {"group_symbol" : amount, ...}
        self._mole_fractions = mix.get_mole_fractions()
        self._database = db
        self._temperature = 273
        
        self._mol_number = len(self._moles)
        self._mol_surface = [0 for _ in range(self._mol_number)]
        self._mol_volume = [0 for _ in range(self._mol_number)]
        
        #{symbol : [frac_of_mol_0, frac_of_mol1, ...]
        self._grp_mol_surface_fraction = [{} 
                                          for _ in range(self._mol_number)]
        
        self._grp_surface_fraction = {symbol : 0 for symbol in self._groups}
        self._sum_surface = 0
        
        self._combinatorial = [0 for _ in range(self._mol_number)]
        
        #Values used to calculate residual part
        
        #{symbol1 : {symbol1 : param, symbol2 : param, ...}, ...}
        self._interaction_parameters = {symbol1 : {} 
                                        for symbol1 in self._groups}
        
        #TOD: rename those values to something with physical sense
        self._grp_interaction_energy = [{} 
                                          for _ in range(self._mol_number)]
        
        self._total_grp_interaction_energies = {}
        self._residual = [0 for _ in range(self._mol_number)]
        
        self._activity_coefficients = [0 for _ in range(self._mol_number)]


    
    def _calc_mol_surface_volume(self):
        ms = self._mol_surface
        mv = self._mol_volume
        moles = self._moles
        db = self._database
        
        for mol_index in range(self._mol_number):
            grps = moles[mol_index].get_groups()
            for symbol in grps:
                q, r = db.get_q_r(symbol)
                amount = grps[symbol]
                ms[mol_index] += q*amount
                mv[mol_index] += r*amount
    
    def _calc_grp_mol_surface_fraction(self):
        db = self._database
        ms = self._mol_surface
        groups = self._groups
        for i in range(self._mol_number):
            grps = self._moles[i].get_groups()
            for symbol in groups:
                q, _ = db.get_q_r(symbol)
                #check if symbol group exists in mol i
                amount = grps.get(symbol, 0)
                self._grp_mol_surface_fraction[i][symbol] = amount*q/ms[i]
    
    def _calc_sum_grp_surface(self):
        frac = self._mole_fractions
        ms = self._mol_surface
        ms_frac = self._grp_mol_surface_fraction
        
        grp_frac = self._grp_surface_fraction
        
        self._sum_surface = fsum(frac[i]*ms[i] for i in range(self._mol_number))
        sum_surface = self._sum_surface
        
        for i in range(self._mol_number):
            for symbol in self._moles[i].get_groups():
                grp_frac[symbol] += frac[i]*ms[i]*ms_frac[i][symbol]/sum_surface
        
    
    def _calc_combinatorial(self):
        self._calc_mol_surface_volume()
        self._calc_grp_mol_surface_fraction()
        self._calc_sum_grp_surface()
        
        frac = self._mole_fractions
        mv = self._mol_volume
        ms = self._mol_surface
        
        sum_volume = fsum(frac[i]*mv[i] for i in range(self._mol_number))
        sum_surface = self._sum_surface
        
        #Volume contribution of mol i
        vc = [mv[i]/sum_volume for i in range(self._mol_number)]
        
        #Surface contribution of mol i
        sc = [ms[i]/sum_surface for i in range(self._mol_number)]
        
        self._combinatorial = [1.0 - vc[i] + ln(vc[i]) - 5*ms[i]*(1.0 - vc[i]/sc[i] + ln(vc[i]/sc[i]))
                               for i in range(self._mol_number)]
        
        self._combinatorial_calculated = True
    
    ### Residual part calculation
    
    def _calc_interaction_parameters(self):
        grps = self._groups
        db = self._database
        temp = self._temperature
        
        for symbol1 in grps:
            for symbol2 in grps:
                self._interaction_parameters[symbol1][symbol2] = exp(-1*db.get_parameter(symbol1, symbol2)/temp)
        
    def _calc_grp_interaction_energies(self):
        gm_frac = self._grp_mol_surface_fraction
        ip = self._interaction_parameters
        ie = self._grp_interaction_energy
        groups = self._groups
        
        for i in range(self._mol_number):
            for symbol1 in groups:
                ie[i][symbol1] = fsum(gm_frac[i][symbol2]*ip[symbol2][symbol1] for symbol2 in groups)        
    
    def _calc_total_grp_interaction_energies(self):
        groups = self._groups
        
        ip = self._interaction_parameters
        grp_frac = self._grp_surface_fraction
        tot_ie = self._total_grp_interaction_energies
        
        for symbol1 in groups:
            tot_ie[symbol1] = fsum(grp_frac[symbol2]*ip[symbol2][symbol1] for symbol2 in groups)
    
    def _calc_residual(self):
        self._calc_interaction_parameters()
        self._calc_grp_interaction_energies()
        self._calc_total_grp_interaction_energies()
        
        groups = self._groups
        ms = self._mol_surface
        grp_frac = self._grp_surface_fraction        
        gm_frac = self._grp_mol_surface_fraction
        ie = self._grp_interaction_energy
        tot_ie = self._total_grp_interaction_energies
        
        for i in range(self._mol_number):
            x = 0
            for symbol in groups:
                x += grp_frac[symbol] * ie[i][symbol]/tot_ie[symbol] - gm_frac[i][symbol]*ln(ie[i][symbol]/tot_ie[symbol])
            self._residual[i] = ms[i]*(1 - x)

    def _calc_activity_coefficients(self):
        for i in range(self._mol_number):
            self._activity_coefficients[i] = exp(self._combinatorial[i] + self._residual[i])
        

    def _calc(self):
        
        #combinatorial part is not temperature dependant
        #and does not need to be recalculated
        if not self._combinatorial_calculated:
            self._calc_combinatorial()
        
        self._calc_residual()
        self._calc_activity_coefficients()       
        self._calculated = True
           
    
    #### Public methods ####
    
    
    def set_temperature(self, temp):
        if temp > 0:
            self.calculated = False
            self._temperature = temp
        else:
            raise ValueError()  #TODO: Exception handling
        
    def get_temperature(self):
        return self._temperature
    

        
 
    def get_activity_coeff(self, mol):
        if not self._calculated:
            self._calc()
        return self._activity_coefficients[self._moles.index(mol)]
        
