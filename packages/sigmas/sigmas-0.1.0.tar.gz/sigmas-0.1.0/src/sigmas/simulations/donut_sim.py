from astrodonut.donut import Donut
from astrodonut.donut_List import DonutList
from astrodonut.donut_exporter import DonutExporter

import tempfile, os
from pathlib import Path

def create_one_nut(values: dict):
    temp_dir = tempfile.gettempdir()
    fits_path = os.path.join(temp_dir, "simulation_result")
    fits_dir = Path(fits_path)
    donut_path = Path.joinpath(fits_dir, "donut.fits")

    try:
        # Create donut with parameter validation
        donut = Donut(
            a1=float(values["semi-maj"]),
            b1=float(values["semi-min"]),
            ecc=float(values["ecc"]),
            inc=float(values["inc"]),
            ring_ratio=float(values["ring_ratio"]),
            width=int(values["width"]),
            height=int(values["height"])
        )

        export_ring1 = DonutExporter(donut)
        export_ring1.save_to_fits(str(donut_path), overwrite=True)

        return str(donut_path)
    
    except (ValueError, KeyError) as e:
        raise ValueError(f"Simulation failed: {str(e)}")