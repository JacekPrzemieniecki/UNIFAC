Usage
-------
Run text_mode.py

Available commands:

ADD <smiles> <quantity>
  <smiles> - SMILES notation of compound added
  <quantity> - amount (in moles) of compound
  
REMOVE <smiles> <quantity>
  <smiles> - SMILES notation of compound removed
  <quantity> - amount (in moles) of compound

PRINT <smiles>
  prints activity coefficient of <smiles>
TEMPERATURE <temp>
  <temp> - temperature of the solution in K
RESET
  resets the solution

Example
-------
For equimolar mixture of water and pentanamine do::

  ADD CCCCCN 1
  ADD O 1
  PRINT CCCCCN
  > Activity coefficient for:  CCCCCN   1.0009635890593225
  PRINT O
  > Activity coefficient for:  O   1.4522017025416403

API
-------
Text mode commands map directly to the methods of unifac.facade.

facade.add_molecule_smiles(smiles, quantity)
  Adds the specified amount od compound into the mixture.
  Use negative quantities to remove.

facade.getcoeff(smiles)
  Returns the activity coefficient of the compound in current mixture.

facade.set_temperature(temp)
  Sets the temperature of current mixture

facade.reset_solution()
  Resets the mixture to empty state, and the temperature to 273K

Example
-------
::

  from unifac.facade import Facade

    f = Facade()
    print(f.__dict__)

    f.add_molecule_smiles("CCCCCN", 1.0)
    f.add_molecule_smiles("O", 1.0)
    print("Pentanamine activity coefficient: ")
    print(f.get_coeff("CCCCCN"))
    print("Water activity coefficient: ")
    print(f.get_coeff("O"))



Credits
-------
- 'PLY' : http://www.dabeaz.com/ply/
- `modern-package-template`: http://pypi.python.org/pypi/modern-package-template
