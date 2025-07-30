import json
from pathlib import Path
import os

def match_molecule_to_perfumes(mol):
    """
    Retrieves a list of perfumes that contain a specified molecule from a local JSON database.

    The function loads perfume data from a local JSON file and searches for perfumes that include
    the given molecule in their list of components. The search is case-insensitive.

    Args:
        mol (str): The name of the molecule to search for in the perfume data.

    Returns:
        list[str] or str: A list of perfumes (with brand names) that contain the molecule.
        Returns a message string if no matches are found.
        Returns an empty list if the data file does not exist.

    Notes:
        The perfume data must be stored in a file located at 'data/perfumes.json'.
        Each perfume entry in the JSON file is expected to be a dictionary containing the keys:
        'name' (str), 'brand' (str), and 'molecules' (list of str).
        The molecule matching is performed in uppercase for consistency.
    """
   
    path_perf = Path.home() / ".perfumeme" / "perfumes.json"

    if not path_perf.exists():
        return []

    with open(path_perf, "r", encoding="utf-8") as f:
        perfumes = json.load(f)

    
    mol_upper = mol.upper()
    matched_perfumes = []
    for perfume in perfumes:
        if mol_upper in perfume.get("molecules", []):
            matched_perfumes.append(f"{perfume['name']} by {perfume['brand']}")

    if matched_perfumes == []:
        return f"No perfumes found containg this molecule."
    else:
        return matched_perfumes


def match_mol_to_odor(mol):
    """
    Retrieves the list of odor descriptors associated with a specified molecule from a local JSON database.

    The function loads molecular data from a local JSON file and searches for the odor characteristics
    linked to the specified molecule. The search is case-insensitive.

    Args:
        mol (str): The name of the molecule to search for in the molecular data.

    Returns:
        list[str]: A list of odor descriptors associated with the molecule.
        Returns an empty list if the molecule is not found or if the data file does not exist.

    Notes:
        The molecule data must be stored in a file located at 'data/molecules.json'.
        Each entry in the JSON file should be a dictionary containing at least the keys:
        'name' (str) and 'odors' (list of str).
        The molecule name comparison is performed in lowercase for consistency.
    """

    path = Path.home() / ".perfumeme" / "molecules.json"

    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        molecules = json.load(f)
   
    mol_lower = mol.lower()
    
    for molecule in molecules:
        if mol_lower == molecule.get("name", []).lower():
            if "odor" not in molecule:
                return f"No odors found for this molecule."
            else:
                return molecule.get("odor")  
    if mol not in molecule.get("name", []):
        return f"Molecule not found."
              

def odor_molecule_perfume(mol):
    """
    Retrieves perfumes that contain a given molecule along with the associated odor descriptors.

    This function combines the outputs of `match_molecule_to_perfumes` and `match_mol_to_odor` 
    to return a dictionary with two keys:
    - "perfumes": a list of perfume names and brands containing the molecule.
    - "odors": a list of odor descriptors linked to the molecule.

    If the molecule is not found in any perfume or has no associated odor data, a message is returned.

    Args:
        mol (str): The name of the molecule to search for.

    Returns:
        dict[str, list[str]] or str: A dictionary containing the perfumes and odors associated
        with the molecule, or a message string if no data is found.

    Notes:
        This function depends on the availability of valid data in 'data/perfumes.json' 
        and 'data/molecules.json'. It assumes the functions `match_molecule_to_perfumes` 
        and `match_mol_to_odor` are defined and return expected values.
    """

    dict_mol = {}
    if match_molecule_to_perfumes(mol) == f"No perfumes found containg this molecule." or match_mol_to_odor(mol) == f"Molecule not found.":
        return f"No perfumes found containg this molecule."
    else:
        dict_mol["perfumes"]= match_molecule_to_perfumes(mol)
        dict_mol["odors"]= match_mol_to_odor(mol)
        return dict_mol
    
def what_notes(perfume: str, note_type: str):
    """
    Retrieves the notes of a specified perfume from a JSON database.

    The function loads perfume data from a local JSON file and searches for the notes
    associated with the given perfume name. The search is case-insensitive.

    Args:
        perfume (str): The name of the perfume to search for in the perfume data.
        type (str): The type of notes to retrieve ("top", "heart", "base").

    Returns:
        list[str] or str: A list of notes associated with the perfume.
        Returns a message string if no matches are found.
        Returns an empty list if the data file does not exist.

    Notes:
        The note matching is performed in uppercase for consistency.
    """
    
    path_perf = Path.home() / ".perfumeme" / "perfumes.json"

    if not path_perf.exists():
        return []

    with open(path_perf, "r", encoding="utf-8") as f:
        perfumes = json.load(f)
    
        
    perfume_upper = perfume.upper()
    note_type_upper = note_type.upper()
    perf_list = []
    for perf in perfumes:
        if perfume_upper == perf.get("name", []).upper():
            perf_list.append(perf.get("name", []))
    if perf_list == []:
        return f"Perfume not found."

    for perf in perfumes:
        if perfume_upper == perf.get("name", []).upper():
            print(f"{note_type} notes for {perfume}:")
            if note_type_upper == "TOP":
                return perf.get("notes", {}).get("top")
            elif note_type_upper == "HEART":
                return perf.get("notes", {}).get("heart")
            elif note_type_upper == "BASE":
                return perf.get("notes", {}).get("base")
        if note_type_upper not in ["TOP", "HEART", "BASE"]:
                return f"Invalid note type. Please use 'top', 'heart', or 'base'."
        
def get_mol_from_odor(odor: str):
    """
    Retrieve a list of molecule names associated with a given odor from a local JSON database.

    This function searches a locally stored JSON file (`~/.perfumeme/molecules.json`) for molecules 
    that have an "odor" attribute matching the specified odor string (case-insensitive). 

    Parameters:
        odor (str): The name of the odor to search for (e.g., "woody", "citrus", "floral").

    Returns:
        list[str]: A list of molecule names associated with the specified odor.
        If no matching odor is found, a message string is returned indicating that no molecules were found.

    Notes:
        - The JSON file is expected to contain a list of dictionaries, each representing a molecule
          with keys such as "name" and "odor".
        - If the JSON file does not exist, the function returns an empty list.
    """
    
    path_mol = Path.home() / ".perfumeme" / "molecules.json"
    
    if not path_mol.exists():
        return []
    with open(path_mol, "r", encoding="utf-8") as f:
        molecules = json.load(f)
    
    odor_upper = odor.upper()

    matched_molecules = []

    for molecule in molecules:
        for scent in molecule.get("odor", []):
            if odor_upper == scent.upper():
                matched_molecules.append(molecule.get("name",[]))
    
    if matched_molecules == []:
        return f"No molecules found that have this odor."
    else:
        return matched_molecules        

