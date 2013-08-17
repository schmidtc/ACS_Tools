from config import PYACS_DATAPATH

import os
import pysal

db = pysal.open(os.path.join(PYACS_DATAPATH,'table_restrictions.csv'),'r')
header = db[0][0]
tid = db[1:,0]
nonblks = db[1:,1]
blks = db[1:,2]

aval4blks = dict([x for x in zip(tid,blks) if x[1]])
avalnonblks = dict([x for x in zip(tid,nonblks) if x[1]])



