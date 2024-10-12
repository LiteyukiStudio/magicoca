from multiprocessing import set_start_method

from magicoca.chan import Chan, T

set_start_method("spawn", force=True)