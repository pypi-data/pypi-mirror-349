import tempfile
import os
from .utils import update_yaml, yaml_lss_updates, get_scopesim_inst_pkgs_path, ensure_packages_installed
import re
import subprocess
import sys
import scopesim as sim
from pathlib import Path

def Simulate(variables: dict):
    """
    Simulate images for differnt combinations of source, mode and exposure time.

    :param variables: A dictionary containing values for the mode, source and exposure time.
    :type variables: dict
    :rtype: None
    """
    ensure_packages_installed()
    
    sim.rc.__config__["!SIM.file.local_packages_path"] = get_scopesim_inst_pkgs_path()

    temp_dir = tempfile.gettempdir()
    fits_file_path = os.path.join(temp_dir, "simulation_result")
    mode, source, exp = variables["mode"], variables["source"], variables["exposure_time"] 
    lss_pattern = re.compile("lss_[lnm]")
    img_pattern = re.compile("img_[lnm]")
    ifu_pattern = re.compile("lms")
    this_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(this_dir, "sim.yaml")

    if not os.path.exists(yaml_path):
        with open(yaml_path, 'w') as f:
            f.write('''simulation:
                        source:
                            kwargs: {}
                        properties:
                            ndit: 4
                            nObs: 1
                    ''')

    if lss_pattern.match(mode) or img_pattern.match(mode) or ifu_pattern.match(mode):
        key = (mode, source)
        if key in yaml_lss_updates(mode=mode, source=source, exp=exp):
            yaml_changes = {f"simulation:{k}": v for k, v in yaml_lss_updates(mode=mode, source=source, exp=float(exp)/4)[key].items()}
            update_yaml(yaml_path, yaml_changes)
        else:
            raise ValueError(f"Unsupported mode/source combination: {key}")
    else:
        raise ValueError("Unsupported mode(How did you even select that?)")
    cmd = [
        sys.executable,
        f"{this_dir}/python/run_recipes.py",
        f"--inputYAML={yaml_path}",
        "--outputDir", f"{fits_file_path}",
        "--doCalib=0",
        "--sequence=1",
        "--nCores=4"
    ]

    result = subprocess.run(cmd, stderr=sys.stderr, stdout=sys.stdout,check=True, text=True)
    return None