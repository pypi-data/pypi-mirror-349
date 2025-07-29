"""
@Author: Luo Jiejian
@Date: 2025/1/21
"""
import gzip
import io
import os
import pathlib
import shutil
import subprocess
import time
import uuid
from typing import Union, Optional

import pdbfixer
from openmm import app
from typeguard import typechecked

from gemmi_protools.io.cif_opts import _is_cif
from gemmi_protools.io.pdb_opts import _is_pdb


@typechecked
def _load_by_pbdfixer(path: Union[str, pathlib.Path]) -> pdbfixer.PDBFixer:
    cur_path = pathlib.Path(path)
    if _is_pdb(path) or _is_cif(path):
        s1 = cur_path.suffixes[-1]
        s2 = "".join(cur_path.suffixes[-2:])

        if s1 in [".pdb", ".cif"]:
            # s1 suffix
            fixer = pdbfixer.PDBFixer(filename=path)
        else:
            # s2 suffix
            with gzip.open(path, "rb") as gz_handle:
                with io.TextIOWrapper(gz_handle, encoding="utf-8") as text_io:
                    if s2 == ".pdb.gz":
                        fixer = pdbfixer.PDBFixer(pdbfile=text_io)
                    else:
                        fixer = pdbfixer.PDBFixer(pdbxfile=text_io)
    else:
        raise ValueError("Only support .cif, .cif.gz, .pdb or .pdb.gz file, but got %s" % path)
    return fixer


@typechecked
def clean_structure(input_file: Union[str, pathlib.Path],
                    output_file: Union[str, pathlib.Path],
                    add_missing_residue: bool = False,
                    add_missing_atoms: str = "heavy",
                    keep_heterogens: str = "all",
                    replace_nonstandard: bool = True,
                    ph: Union[float, int] = 7.0
                    ):
    """

    :param input_file: str, Input structure file, support file format .cif, .cif.gz, .pdb or .pdb.gz
    :param output_file: str, Output structure file, support file format .cif, .pdb
    :param add_missing_residue: default False
    :param add_missing_atoms: default heavy, accepted values 'all', 'heavy', 'hydrogen', 'none'
        all: add missing heavy and hydrogen atoms
        heavy: add missing heavy atoms only
        hydrogen: add missing hydrogen atoms only
        none: not add missing atoms

    :param keep_heterogens: default all, accepted values 'all', 'water', 'none'
            all: keep all heterogens
            water: only keep water
            none: remove all heterogens
    :param replace_nonstandard: default True, replace all non-standard residues to standard ones
    :param ph: default 7.0, ph values to add missing hydrogen atoms
    :return:
        str, status message of fixing
        if successful, return Finish, otherwise message of error
    """
    assert add_missing_atoms in ['all', 'heavy', 'hydrogen', 'none']
    assert keep_heterogens in ['all', 'water', 'none']

    try:
        ######################################################
        # load structure
        ######################################################
        fixer = _load_by_pbdfixer(input_file)

        ######################################################
        # replace non-standard residues
        ######################################################
        if replace_nonstandard:
            fixer.findNonstandardResidues()
            fixer.replaceNonstandardResidues()

        ######################################################
        # remove heterogens
        ######################################################
        if keep_heterogens == 'none':
            fixer.removeHeterogens(keepWater=False)
        elif keep_heterogens == 'water':
            fixer.removeHeterogens(keepWater=True)

        ######################################################
        # missing residue
        ######################################################
        if add_missing_residue:
            fixer.findMissingResidues()
        else:
            fixer.missingResidues = {}

        ######################################################
        # missing atoms
        ######################################################
        fixer.findMissingAtoms()
        if add_missing_atoms not in ['all', 'heavy']:
            fixer.missingAtoms = {}
            fixer.missingTerminals = {}
        fixer.addMissingAtoms()
        if add_missing_atoms in ['all', 'hydrogen']:
            fixer.addMissingHydrogens(ph)

        ######################################################
        # output
        ######################################################
        out_dir = os.path.dirname(output_file)
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)

        suffix = pathlib.Path(output_file).suffix
        assert suffix in [".pdb", ".cif"], "output file must be .cif or .pdb"

        with open(output_file, 'w') as out_handle:
            if suffix == ".pdb":
                app.PDBFile.writeFile(fixer.topology, fixer.positions, out_handle, keepIds=True)
            else:
                app.PDBxFile.writeFile(fixer.topology, fixer.positions, out_handle, keepIds=True)

        msg_str = "Finished"
    except Exception as e:
        msg_str = str(e)

    return dict(input=input_file, msg=msg_str)


@typechecked
def move_with_overwrite(src_folder: str, dst_folder: str, filename: str):
    assert os.path.isdir(src_folder)
    assert os.path.isdir(dst_folder)

    src_path = os.path.join(src_folder, filename)
    dst_path = os.path.join(dst_folder, filename)

    if os.path.exists(dst_path):
        os.remove(dst_path)
    shutil.move(src_path, dst_folder)


@typechecked
def repair_structure(input_file: Union[str, pathlib.Path],
                     out_dir: Union[str, pathlib.Path],
                     temp_dir: Union[str, pathlib.Path],
                     foldx_path: Optional[str] = None,
                     timeout=3600):
    if not os.path.isdir(out_dir):
        raise NotADirectoryError(out_dir)

    if not os.path.isdir(temp_dir):
        raise NotADirectoryError(temp_dir)

    in_path = pathlib.Path(input_file).expanduser().resolve()
    pdb_dir = str(in_path.parent)
    pdb_file = str(in_path.name)
    if not os.path.isfile(input_file):
        raise FileNotFoundError(input_file)

    assert pdb_dir != str(out_dir), "output directory can't be the directory of input_file"

    stem_name = in_path.stem

    # create temp dir
    sub_temp_dir = os.path.join(temp_dir, "%s_%s" % (stem_name, str(uuid.uuid4())))

    if os.path.isdir(sub_temp_dir):
        shutil.rmtree(sub_temp_dir)

    os.makedirs(sub_temp_dir)

    if foldx_path is None:
        foldx_path = shutil.which("foldx")

    if foldx_path is None:
        raise RuntimeError("path of foldx is not set or found in PATH")

    old_dir = os.getcwd()
    command_settings = ["cd %s" % sub_temp_dir,
                        "&&",
                        foldx_path,
                        "-c RepairPDB",
                        "--pdb %s" % pdb_file,
                        "--pdb-dir %s" % pdb_dir,
                        "--output-dir %s" % sub_temp_dir,
                        "&&",
                        "cd %s" % old_dir
                        ]

    start = time.time()

    try:
        result = subprocess.run(" ".join(command_settings), shell=True, check=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=timeout)
        # Return a tuple of the file name and the stdout or stderr if command fails
        if result.returncode == 0:
            msg_str = "Finished"
        else:
            msg_str = result.stderr

        result_file = os.path.join(sub_temp_dir, "%s_Repair.pdb" % stem_name)
        fxout_file = os.path.join(sub_temp_dir, "%s_Repair.fxout" % stem_name)
        if os.path.exists(result_file) and os.path.exists(fxout_file):
            move_with_overwrite(sub_temp_dir, out_dir, "%s_Repair.pdb" % stem_name)
            move_with_overwrite(sub_temp_dir, out_dir, "%s_Repair.fxout" % stem_name)
    except subprocess.CalledProcessError as e:
        # Handle errors in the called executable
        msg_str = e.stderr
    except Exception as e:
        # Handle other exceptions such as file not found or permissions issues
        msg_str = str(e).encode()
    finally:
        # clean sub temp
        if os.path.isdir(sub_temp_dir):
            shutil.rmtree(sub_temp_dir)
    end = time.time()
    return dict(input=input_file, msg=msg_str, use_time=round(end - start, 1))
