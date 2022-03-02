"""
Functions for interfacing between PEST and FracMan
PEST: https://pesthomepage.org/
FracMan: https://www.golder.com/fracman/
"""
import json
from pathlib import Path
import warnings

class PestGenerator:
    """Class to generate a basic pest file from a config json
    Provides numerous input checks
    """
    def __init__(self, config_path: Path) -> None:
            self.config_path = Path(config_path)
            assert self.config_path.exists()
            assert self.config_path.is_file()
            assert self.config_path.suffix.lower() == '.json'

    def parse_config(self):
        "Load the json file, check for basic sections"
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)
        
        # check for mandatory sections
        assert 'control data' in self.config.keys()
        assert 'parameter groups' in self.config.keys()
        assert 'parameter data' in self.config.keys()
        assert 'observation groups' in self.config.keys()
        assert 'model command line' in self.config.keys()
        assert 'model input/output' in self.config.keys()

        # check and parse control data
        self.check_control_data()

    def check_control_data(self):
        "Check control data section of json"
        cdata = self.config['control data']
        
        ## FIRST LINE ##
        # RSTFLE: should PEST leave tracks to restart upon failure?
        assert cdata.get('restart') is not None
        assert isinstance(cdata.get('restart'), bool)
        if cdata.get('restart'):
            self.RSTFLE = 'restart'
        else:
            self.RSTFLE = 'norestart'

        # PESTMODE: what mode is pest running in?
        self.PESTMODE = cdata.get('mode')
        assert self.PESTMODE is not None
        assert isinstance(self.PESTMODE, str)
        assert self.PESTMODE in ['estimation', 'prediction', 'regularization', 'pareto']
        
        ## SECOND LINE ##
        # npar: number of parameters
        self.npar = cdata.get('parameters')
        assert self.npar is not None
        assert isinstance(self.npar, int)
        assert self.npar > 0
        
        # nobs: number of parameters
        self.nobs = cdata.get('observations')
        assert self.nobs is not None
        assert isinstance(self.nobs, int)
        assert self.nobs > 0

        # npargp: number of parameter groups
        self.npargp = cdata.get('parameter groups')
        assert self.npargp is not None
        assert isinstance(self.npargp, int)
        assert self.nobs > 0
    
    def check_pest_viability(self):
        "Some checks built off the pest manual"
        if self.npar > self.nobs:
            warnings.warn("Number of parameters exceeds observations, risk of non-unique solution")

    def write_pst_file(self, filename='case.pst'):
        "Write out .pst file"
        with open(self.config_path.parent / filename, 'w') as f:
            f.writelines("pcf \n")
            f.writelines("* control data \n")
            f.writelines(self.RSTFLE + "  " + self.PESTMODE)

