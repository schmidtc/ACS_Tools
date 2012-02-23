"""
pyACS -- Python Library for Extracting Data from the American Community Survey.
"""

__author__ = "Charles R Schmidt <schmidtc [on] gmail>"

import os
import config
import sumlevel
from geo import GEO

def COL_LOOKUP():
    d = {}
    with open(os.path.join(config.PYACS_DATAPATH,'column_lookup.csv'),'r') as f:
        header = f.next()
        for line in f:
            cid,seq,idx = line.strip().split(',')
            seq = seq.rjust(4,'0')
            idx = int(idx)
            d[cid] = (seq,idx)
    return d
COL_LOOKUP = COL_LOOKUP()

def ffloat(x):
    """
    ffloat -- Forced float -- will make anything a float or NaN
    """
    try:
        return float(x)
    except:
        return float('nan')

class StSeq:
    def __init__(self,st,seq):
        fname = "e20105%s%s000.txt"%(st,seq)
        self.path = os.path.join(config.ACS_PATH,fname)
    def get_col_by_lrn(self,colidx,lrns):
        LOGRECNO_IDX = 5
        d = {}
        with open(self.path,'r') as f:
            for line in f:
                line = line.split(',')
                d[line[LOGRECNO_IDX]] = line[colidx]
        return [d[lrn] for lrn in lrns]
        
class ACS:
    """
    Main entry point

    Allows you to open the ACS at a particular summary level.
    Default summary level is TRACT

    Examples:
    >>> tracts = ACS(sumlevel.TRACT)
    >>> len(tracts)
    74002
    >>> blkgrps = ACS(sumlevel.BLOCKS_GRP)
    >>> len(blkgrps)
    220334
    """
    def __init__(self, sumlevel=sumlevel.TRACT):
        self.level = sumlevel
        self.GEOID = []
        self.LOGRECNO = {}
        for st in config.STATE_AB:
            geo = GEO(st)
            self.GEOID.extend(geo.get('GEOID',sumlevel))
            self.LOGRECNO[st] = geo.get('LOGRECNO',sumlevel)
    def __len__(self):
        """ returns the number of regions at the current sumlevel """
        return len(self.GEOID)
    def __getitem__(self,key):
        if key not in COL_LOOKUP:
            raise KeyError
        seq,idx = COL_LOOKUP[key]
        col = []
        for st in config.STATE_AB:
            lrn = self.LOGRECNO[st]
            col.extend(StSeq(st,seq).get_col_by_lrn(idx,lrn))
        return map(ffloat,col)

