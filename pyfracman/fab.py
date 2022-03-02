"""
Module to read .fab files and return properties
"""
import pandas as pd
import numpy as np

def read_fractures(f, is_tess=False):
    # Read the fracture
    fracs = []
    frac_ids = []
    trans = []
    normals = []
    properties_list = []
    nd = 3
    for line in f:
        # exit upon end keyword
        if line.strip() in ["END FRACTURE", "END TESSFRACTURE"]:
            return (
                fracs,
                np.asarray(frac_ids),
                np.asarray(trans),
                np.asarray(normals),
                properties_list,
            )

        # first line is the properties
        if is_tess:
            fracid, num_vert, *properties = line.split()
        else:
            fracid, num_vert, t, *properties = line.split()
            trans.append(float(t))

        frac_ids.append(int(fracid))
        properties_list.append(properties)

        # now we read each one of the vertices
        num_vert = int(num_vert)
        vert = np.zeros((num_vert, nd))
        for i in range(num_vert):
            data = f.readline().split()
            vert[i] = np.asarray(data[1:])

        # Transpose to nd x n_pt format
        vert = vert.T
        fracs.append(vert)

        # Now we read the normal vector
        normal_vector = f.readline().split()
        normals.append(normal_vector)

        if is_tess:
            trans.append(int(normal_vector[1]))


def read_keyword(line):
    # Read a single keyword, on the form  key = val
    words = line.split("=")
    key = words[0].strip()
    val = words[1].strip()
    return key, val


def read_section(f, section_name):
    # Read a section of the file, surrounded by a BEGIN / END wrapping
    d = {}
    for line in f:
        if line.strip() == "END " + section_name.upper().strip():
            return d
        k, v = read_keyword(line)
        d[k] = v


def make_properties_dict(properties):
    "clean up properties and return"
    return {k: v.split('"')[1] for k, v in properties.items()}


def clean_dict_values(section_dict):
    return {k: v.replace('"', "") for k, v in section_dict.items()}


def make_properties_df(fid, prop_dict, prop_list):
    "Make a property dataframe for the fractures"
    prop_df = pd.DataFrame(prop_list, columns=prop_dict.values(), index=fid)
    prop_df = prop_df.astype(float)
    # rule based fixes
    int_cols = ["Fracture Geometry", "Set Name"]
    for col in int_cols:
        if col in prop_df.columns:
            prop_df[col] = prop_df[col].astype(int)

    return prop_df


def parse_fab_file(f_name):
    output = {}
    with open(f_name, "r") as f:
        for line in f:
            if line.strip() == "BEGIN FORMAT":
                # Read the format section
                output["format"] = clean_dict_values(read_section(f, "FORMAT"))
            elif line.strip() == "BEGIN PROPERTIES":
                # Read in properties section
                output["prop_dict"] = make_properties_dict(
                    read_section(f, "PROPERTIES")
                )
            elif line.strip() == "BEGIN SETS":
                # Read set section
                output["sets"] = clean_dict_values(read_section(f, "SETS"))
            elif line.strip() == "BEGIN FRACTURE":
                # Read fractures
                (
                    output["fracs"],
                    output["fid"],
                    output["trans"],
                    output["normals"],
                    output["prop_list"],
                ) = read_fractures(f, is_tess=False)
            elif line.strip() == "BEGIN TESSFRACTURE":
                # Read tess_fractures
                (
                    output["tess_fracs"],
                    output["tess_fid"],
                    output["tess_sgn"],
                    output["tess_normals"],
                    output["tess_prop_list"],
                ) = read_fractures(f, is_tess=True)
            elif line.strip() == "BEGIN ROCKBLOCK":
                # Not considered block
                pass
            elif line.strip()[:5] == "BEGIN":
                # Check for keywords not yet implemented.
                raise ValueError("Unknown section type " + line)

    output["property_df"] = make_properties_df(output["fid"], output["prop_dict"], output["prop_list"])
    return output
