'''
Created on 11-10-2012

@author: Jacek Przemieniecki
'''

from . import group_parser
from ..database import Database

def _match_atom_to_node(atom, node):
    """
    Returns True, next if atom matches node, False, next if it does not
    next is ("next", ...) parse if it appears as atom extension, None otherwise
    """
    side_chain = None
    
    if node[0] == "atom":
        return atom.symbol == node[1] and not atom.aromatic, None
    
    elif node[0] == "aromatic-atom":
        return atom.symbol == node[1] and atom.aromatic, None
    
    elif node[0] == "ext-atom":
        symbol_matches, _ = _match_atom_to_node(atom, node[1])
        if not symbol_matches:
            return False, None

        atom_bonded_symbols = [con.symbol for con in atom.connected]
        for extension in node[2]:
            token = extension[0]
            if token == "next":
                side_chain = extension
            elif token == "halogen":
                if not atom_bonded_symbols.count(extension[1]) == extension[2]:
                    return False, None
            elif token == "hydrogen":
                if not atom.hydrogens == extension[1]:
                    return False, None
            else:
                raise Exception()       # TODO: exception handling
            
    else:
        # Unknown node type
        raise Exception()                   # TODO: Excepton handling
    
    return True, side_chain

def _crawl(atom, tree, path_so_far):
    
    if atom in path_so_far:
        return None
    new_path_so_far = path_so_far + [atom]
    atom_matches, side_chain = _match_atom_to_node(atom, tree[1])
    
    if not atom_matches:
        return None

    if tree[0] != "node":
        raise Exception()   # TODO: Exception handling
    
    next_tree = tree[2]
    if next_tree is None:
        return [atom]
    next_bond = next_tree[1]
    node = next_tree[2]
    
    next_pos_atoms = [atom.connected[i] for i in range(len(atom.connected)) if atom.bonds[i] == next_bond]
    
    atoms_to_match = []
    for pos_atom in next_pos_atoms:
        atoms_to_match = _crawl(pos_atom, node, new_path_so_far)
        if atoms_to_match:
            break
    if not atoms_to_match:
        return None
    
    if side_chain:
        side_bond = side_chain[1]
        side_node = side_chain[2]
        atoms_to_match_side = []
        next_pos_side_atoms = [atom.connected[i] for i in range(len(atom.connected)) if atom.bonds[i] == side_bond]
        for pos_atom in next_pos_side_atoms:
            atoms_to_match_side = _crawl(pos_atom, side_node, new_path_so_far + atoms_to_match)
            if atoms_to_match_side:
                break
        
        if atoms_to_match_side:
            atoms_to_match.extend(atoms_to_match_side)
        else:
            return None
    
    return atoms_to_match + [atom]
    

def _look_for_group(group_string, atoms, atom_symbols):
    """Finds starting points for group finding"""
    tree = group_parser.parse(group_string)
    # Each tree starts with ("node", first_atom_touple, next_node
    # first_atom_touple may be ("ext-atom", atom_touple, extension_touple)
    # or ("atom", symbol) or ("aromatic_atom", symbol)
    starting_symbol = tree[1]
    if starting_symbol[0] == "ext-atom":
        starting_symbol = starting_symbol[1]
    
    #get the actual symbol string
    starting_symbol = starting_symbol[1]

    try:
        possible_starting_atoms = atom_symbols[starting_symbol]
    except KeyError:
        return None
    
    
    matches = []
    for pos_atom in possible_starting_atoms:
        atom = atoms[pos_atom]
        match = _crawl(atom, tree, [])
        if match:
            match_ids = sorted([atoms.index(at) for at in match])
            if not match_ids in matches:
                matches.append(match_ids)
    
    return matches
    

def _get_possible_groups(atoms):
    db = Database()
    num_atoms = len(atoms)
    atom_symbols = {}
    for index in range(num_atoms):
        atom_symbols[atoms[index].symbol] = atom_symbols.get(atoms[index].symbol, []) + [index]
    
    possible_groups = {}
    pos_grp_id = 0
    for group_string in db.iterate_strings():
        # list of lists of atoms matching group_string
        possible_atoms_in_group = _look_for_group(group_string, atoms, atom_symbols)
        if not possible_atoms_in_group:
            continue
        
        for poss_grp in possible_atoms_in_group:
            possible_groups[pos_grp_id] = (group_string, poss_grp)
            pos_grp_id +=1
    
    atom_to_pos_grp = _map_atoms_to_groups(possible_groups)
    
    return possible_groups, atom_to_pos_grp

def _map_atoms_to_groups(possible_groups):
    atom_to_pos_grp = {}
    for pos_grp_id in possible_groups:
        for atom_id in possible_groups[pos_grp_id][1]:
            atom_to_pos_grp[atom_id] = atom_to_pos_grp.get(atom_id, []) + [pos_grp_id]
    
    return atom_to_pos_grp

def _remove_group(group_id, possible_groups, atom_to_possible_group):
    atoms_in_removed_group = possible_groups[group_id][1]
    for atom in atoms_in_removed_group:
        for grp in atom_to_possible_group[atom]:
            try:
                del possible_groups[grp]
            except KeyError:
                pass
    return possible_groups, _map_atoms_to_groups(possible_groups)

def _reduce(poss_grp, at_to_grp):
    changed = False
    certain_group = None
    for v in at_to_grp.values():
        if len(v) == 1:
            certain_group_id = v[0]
            certain_group = poss_grp[certain_group_id][0]
            
            poss_grp, at_to_grp = _remove_group(certain_group_id, poss_grp, at_to_grp)
            changed = True
            break
    return changed, certain_group, poss_grp, at_to_grp

def split(molecule):
    """
    Given molecule, returns dict of UNIFAC group string : amount of group in molecule
    """
    atoms = molecule.atoms
    possible_groups, atom_to_possible_group = _get_possible_groups(atoms)
    changed = True
    groups = {}
    while possible_groups:
        while changed:
            changed, certain_group, possible_groups, atom_to_possible_group = _reduce(possible_groups, atom_to_possible_group)
            if certain_group:
                groups[certain_group] = groups.get(certain_group, 0) + 1
        if possible_groups:
            #there are some ambiguous groups, pick one with biggest amount of atoms
            highest_len = 0
            longest_group = None
            for k, v in possible_groups.items():
                c_len = len(v[1])
                if c_len > highest_len:
                    highest_len = c_len
                    longest_group = k
            longest_grp_symbol = possible_groups[longest_group][0]
            groups[longest_grp_symbol] = groups.get(longest_grp_symbol, 0) + 1
            possible_groups, atom_to_possible_group = _remove_group(longest_group, possible_groups, atom_to_possible_group)
    return groups
                
            
    