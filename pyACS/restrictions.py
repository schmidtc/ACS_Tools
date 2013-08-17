from config import PYACS_DATAPATH

import os
import pysal

pth = os.path.join(PYACS_DATAPATH,'table_restrictions.csv')

#### Self Install...
if not os.path.exists(pth):
    from _restrictions import txt
    with open(pth,'w') as o:
        o.write(txt)
#### ... End Self Install

db = pysal.open(pth, 'r')
header = db[0][0]
tid = db[1:,0]
nonblks = db[1:,1]
blks = db[1:,2]

aval4blks = dict([x for x in zip(tid,blks) if x[1]])
avalnonblks = dict([x for x in zip(tid,nonblks) if x[1]])
