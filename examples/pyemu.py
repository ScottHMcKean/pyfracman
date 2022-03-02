import pyemu
import os
os.chdir("C:\\Users\\scott.mckean\\Desktop\\exp1_onep32_seismiclength")

pst = pyemu.Pst("test1.pst")
pst.add_parameters("test1.ptf")
pst.write("test1.pst")

# this does an okay job, but lacks some functionality
psthelp = pyemu.helpers.pst_from_io_files(
    tpl_files=['test1.ptf'],
    in_files=['test1.fmf'],
    ins_files=['output.pin'],
    out_files=['output.sts'],
    pst_filename='out.pst'
    )

# make new pst file
par_names = pyemu.pst_utils.parse_tpl_file('test1.ptf')
obs_names = pyemu.pst_utils.parse_ins_file('output.pin')
new_pst = pyemu.pst_utils.generic_pst(par_names,obs_names)
new_pst.control_data.get_dataframe().to_csv('control_data.csv')
new_pst.control_data.
pyemu.helpers.pst_from_io_files()
import pyfracman
import pyfracman.pest
from importlib import reload
reload(pyfracman.pest)
from pyfracman.pest import PestGenerator

self = PestGenerator("examples/pest_config.json")
self.parse_config()
self.write_pst_file()

control_data = pyemu.pst.ControlData()
CONTROL_VARIABLE_LINES = """RSTFLE PESTMODE
NPAR NOBS NPARGP NPRIOR NOBSGP [MAXCOMPDIM]
NTPLFLE NINSFLE PRECIS DPOINT [NUMCOM] [JACFILE] [MESSFILE] [OBSREREF]
RLAMBDA1 RLAMFAC PHIRATSUF PHIREDLAM NUMLAM [JACUPDATE] [LAMFORGIVE] [DERFORGIVE]
RELPARMAX FACPARMAX FACORIG [IBOUNDSTICK] [UPVECBEND]
PHIREDSWH [NOPTSWITCH] [SPLITSWH] [DOAUI] [DOSENREUSE] [BOUNDSCALE]
NOPTMAX PHIREDSTP NPHISTP NPHINORED RELPARSTP NRELPAR [PHISTOPTHRESH] [LASTRUN] [PHIABANDON]
ICOV ICOR IEIG [IRES] [JCOSAVE] [VERBOSEREC] [JCOSAVEITN] [REISAVEITN] [PARSAVEITN] [PARSAVERUN]""".lower().split(
    "\n"
)