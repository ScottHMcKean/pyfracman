"""
Module to read .fab files and return properties
"""
import pandas as pd
import numpy as np


def read_tesselated_fractures(f):
    # Read the fracture
    frac_nodes = []
    frac_faces = []
    frac_properties = []
    frac_ids = []
    sets = []
    for line in f:
        # exit upon end keyword
        if line.strip() == "END TESSFRACTURE":
            return (
                np.asarray(frac_ids),
                np.asarray(sets),
                frac_nodes,
                frac_faces,
                frac_properties,
            )

        # first line is the properties
        fracid, num_nodes, num_faces, set_no = line.split()
        frac_ids.append(int(fracid))
        sets.append(float(set_no))

        # now we read all the nodes (must be 3D xyz)
        num_nodes = int(num_nodes)
        nodes = np.zeros((num_nodes, 3))
        for i in range(num_nodes):
            data = f.readline().split()
            nodes[i] = np.asarray(data[1:])

        frac_nodes.append(nodes.T)

        # now we read all the faces with properties
        num_faces = int(num_faces)

        # read first face to declare an array
        first_face = f.readline().split()
        face_info = np.zeros((num_faces, 5))
        properties = np.zeros((num_faces, len(first_face) - 5))
        face_info[0] = np.asarray(first_face[:5])
        properties[0] = np.asarray(first_face[5:])
        for i in range(1, num_faces):
            data = f.readline().split()
            face_info[i] = np.asarray(data[:5])
            properties[i] = np.asarray(data[5:])

        frac_faces.append(face_info.T)
        frac_properties.append(properties.T)


def read_fractures(f):
    # Read the fracture
    vertices = []
    frac_ids = []
    sets = []
    normals = []
    properties = []
    for line in f:
        # exit upon end keyword
        if line.strip() == "END FRACTURE":
            return (
                np.asarray(frac_ids),
                np.asarray(sets),
                np.asarray(normals),
                vertices,
                properties,
            )

        # first line is the properties
        fracid, num_vert, set_no, *props = line.split()
        sets.append(float(set_no))
        frac_ids.append(int(fracid))
        properties.append(props)

        # now we read each one of the vertices  (must be 3D xyz)
        num_vert = int(num_vert)
        vert = np.zeros((num_vert, 3))
        for i in range(num_vert):
            data = f.readline().split()
            vert[i] = np.asarray(data[1:])

        # transpose to nd x n_pt format and add to frac list
        vertices.append(vert.T)

        # now we read the normal vector
        normal_vector = f.readline().split()
        normals.append(normal_vector)


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
                    output["fid"],
                    output["sets"],
                    output["normals"],
                    output["vertices"],
                    output["properties"],
                ) = read_fractures(f)
            elif line.strip() == "BEGIN TESSFRACTURE":
                # Read tessellated fractures
                (
                    output["t_fid"],
                    output["t_sets"],
                    output["t_nodes"],
                    output["t_faces"],
                    output["t_properties"],
                ) = read_tesselated_fractures(f)
            elif line.strip() == "BEGIN ROCKBLOCK":
                raise NotImplementedError("Rock Block Not Implemented, Sorry!")
            elif line.strip()[:5] == "BEGIN":
                # Check for keywords not yet implemented
                raise ValueError("Unknown section type " + line)

    output["property_df"] = make_properties_df(
        output["fid"], output["prop_dict"], output["properties"]
    )
    return output
