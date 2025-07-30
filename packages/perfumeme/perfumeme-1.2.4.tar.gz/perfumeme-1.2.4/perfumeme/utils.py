#!/usr/bin/env python
# coding: utf-8

import requests
import json
from pathlib import Path
import pandas as pd
import os
import urllib.parse


def get_smiles(compound_name): 
    """
    Retrieves the SMILES (Simplified Molecular Input Line Entry System) string for a given compound name 
    using the PubChem PUG REST API.

    This function sends a request to the PubChem database to fetch the canonical SMILES representation
    of a compound, which is essential for computational chemistry applications.

    Args:
        compound_name (str): The name of the compound to search for (e.g., "linalool").

    Returns:
        str: The SMILES string corresponding to the compound name.

    Raises:
        Exception: If the request fails or the SMILES string is not found in the API response.
    """

    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{compound_name}/property/IsomericSMILES/JSON"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to get SMILES for {compound_name}")
    
    data = response.json() 
    try:
        smiles = data["PropertyTable"]["Properties"][0]["IsomericSMILES"]
        return smiles
    except (KeyError, IndexError): 
        raise Exception("SMILES not found in response")


def resolve_input_to_smiles_and_cid(input_str):
    """
    Attempts to resolve the input string to a valid SMILES and CID.
    If the input is a SMILES, it directly gets the CID.
    If the input is a compound name, it first converts it to SMILES.

    Args:
        input_str (str): Compound name or SMILES.

    Returns:
        tuple: (smiles: str, cid: int)

    Raises:
        Exception: If the input cannot be resolved to a valid compound.
    """

    try:
        cid = get_cid_from_smiles(input_str)
        return input_str, cid
    except requests.HTTPError:
        smiles = get_smiles(input_str)
        cid = get_cid_from_smiles(smiles)
        return smiles, cid


def get_odor(compound_name):
    """
    Retrieves the odor description for a given compound name from a CSV dataset.

    The function performs a case-insensitive search for the compound name in the 'Name' column 
    of the loaded DataFrame. If a match is found, it returns the corresponding value in the 'Odor_notes' column.

    Args:
        compound_name (str): The common name of the compound.

    Returns:
        str: A semicolon-separated string of odor notes associated with the compound.

    Raises:
        Exception: If the compound name is not found in the dataset.
    """
    project_root = Path(__file__).resolve().parents[2]
    csv_path = project_root / "data" / "withodors.csv"

    if not csv_path.exists():
        raise FileNotFoundError(
            f"\n❌ File not found: {csv_path}\n"
            "Make sure the 'data/withodors.csv' file is present in the root directory of the project.\n"
            "This file is not included in the PyPI distribution."
        )

    df = pd.read_csv(csv_path)

    row = df[df["Name"].str.lower() == compound_name.lower()]
    if not row.empty:
        return row.iloc[0]["Odor_notes"]
    else:
        raise Exception(f"Odor information not found for '{compound_name}'.")


def get_cid_from_smiles(smiles):
    """
    Retrieves the PubChem Compound ID (CID) corresponding to a given SMILES string.

    This function queries the PubChem PUG REST API to find the CID for the provided
    SMILES representation of a molecule. It raises an exception if no CID is found
    or if the request fails.

    Args:
        smiles (str): A valid SMILES (Simplified Molecular Input Line Entry System) string.

    Returns:
        int: The first matching PubChem Compound ID (CID).

    Raises:
        Exception: If the request fails or if no CID is found for the SMILES input.
    """
    
    url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/cids/JSON"
    data = {"smiles": smiles}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=data, headers=headers, timeout=10)
    response.raise_for_status()

    try:
        cid = response.json()["IdentifierList"]["CID"][0]
        return cid
    except (KeyError, IndexError):
        raise Exception("CID not found in PubChem response")

    
def get_pubchem_description(cid):
    """
    Retrieves the textual description entries for a compound from PubChem using its CID.

    This function queries the PubChem PUG REST API to get the descriptive information
    associated with a compound identified by its Compound ID (CID). These descriptions
    may include general chemical information, properties, and remarks.

    Args:
        cid (int): The PubChem Compound ID (CID) of the molecule.

    Returns:
        list: A list of dictionaries, each containing a description entry under the "Description" key.
              Returns an empty list if no descriptions are available.

    Raises:
        requests.exceptions.RequestException: If the API request fails.
    """

    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/description/JSON"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get("InformationList",{}).get("Information",[])


def get_pubchem_record_sections(cid):
    """
    Retrieves the structured data sections for a compound from PubChem using its CID.

    This function queries the PubChem PUG-View API to obtain detailed, categorized 
    information about a compound identified by its Compound ID (CID). The returned 
    sections may contain physical and chemical properties, safety data, spectral 
    information, and more.

    Args:
        cid (int): The PubChem Compound ID (CID) of the molecule.

    Returns:
        list: A list of nested dictionaries representing the top-level sections of the 
              compound's data record. Returns an empty list if no sections are found.

    Raises:
        requests.exceptions.RequestException: If the API request fails.
    """

    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get("Record", {}).get("Section",[])
