'''
Created on 16-10-2012

@author: Jacek Przemieniecki
'''

from unifac.facade import Facade    #@UnresolvedImport

class UI(object):
    
    def __init__(self):
        self.facade = Facade()
    
    def parse_file(self, f):
        """ Opens the file from patch f and executes commands inside"""
        with open(f) as raw_file:
            line_number = 1
            commands = raw_file.readlines()
            try:
                for line in commands:
                    self.run_command(line)
                    line_number += 1
            except Exception:   # TODO: Exception handling 
                raise
    
    def run_command(self, line):
        """Available commands:
        ADD <smiles> <quantity>
            <smiles> - SMILES notation of compound added
            <quantity> - amount (in moles) of compound
        REMOVE <smiles> <quantity>
            <smiles> - SMILES notation of compound removed
            <quantity> - amount (in moles) of compound
        PRINT
            prints calculation results for current solution
        RESET
            resets the solution"""
        
        command = line.split()[0]
        parameters = line.split()[1:3]
        
        if command == "ADD":
            self.facade.add_molecule_smiles(parameters[0], float(parameters[1]))
        elif command == "REMOVE":
            self.facade.add_molecule(parameters[0], float(-parameters[1]))
        elif command == "PRINT":
            self.print_result(parameters[0])
        elif command == "RESET":
            self.facade.reset_solution()
        elif command == "TEMPERATURE":
            self.facade.set_temperature(float(parameters[0]))
        else:
            raise Exception() # TODO: Exception handling CommandError("Unknown command: %s" % command)
    
    def print_result(self, iden):
        print("Activity coefficient for: ", iden, " ", self.facade.get_coeff(iden))

ui = UI()

while 1:
    ui.run_command(input())