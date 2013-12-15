'''
Created on 16-10-2012

@author: Jacek Przemieniecki
'''

class Mixture(object):
    
    def _calc_groups(self):
        self._groups = {}
        groups = self._groups
        
        tot_grps = 0
        for mol in self.moles:
            m_groups = self.moles[mol].get_groups()
            for m_grp in m_groups:
                groups[m_grp] = groups.get(m_grp, 0) + m_groups[m_grp]*self.quantities[mol]
                tot_grps += m_groups[m_grp]*self.quantities[mol]
        
        for grp in groups:
            groups[grp] = groups[grp]/tot_grps
        
    def _calc_ordered(self):
        total_moles = sum(self.quantities.values())
        for mol in self.moles:
            self._ordered_moles.append(self.moles[mol])
            self._ordered_mol_fractions.append(self.quantities[mol]/total_moles)
    
    def _finalize(self):
        self._calc_groups()
        self._calc_ordered()
        self._finalized = True
    
    def __init__(self):
        self.moles = {}
        self.quantities = {}
        self._finalized = False
        self._groups = None
        
        # Those two lists must be ordered so that moles[i] 
        # corresponds to quantities[i]
        self._ordered_moles = []
        self._ordered_mol_fractions = []
    
    def add(self, iden, mol, amount):
        if self._finalized:
            raise Exception()       # TODO: Exception handling
        if iden in self.moles:
            self.quantities[iden] += amount
        else:
            self.moles[iden] = mol
            self.quantities[iden] = amount
    
    def get_moles(self):
        if not self._finalized:
            self._finalize()
        return self._ordered_moles
    
    def get_groups(self):
        if not self._finalized:
            self._finalize()
        
        return self._groups
    
    def get_mole_fractions(self):
        if not self._finalized:
            self._finalize()
        
        return self._ordered_mol_fractions