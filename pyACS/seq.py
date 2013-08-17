"""
seq.py -- Do something useful with Sequence_Number_and_Table_Number_Lookup.txt
"""

__author__ = "Charles R. Schmidt <schmidtc@gmail.com>"

import os
import urllib,hashlib
import pysal
import json
import config
DEBUG = config.DEBUG

from restrictions import aval4blks, avalnonblks

def isint(x):
    """
    isint(x) -- Test if value of x is an int.

    x -- str or int -- value to be tested

    >>> isint('0.05')
    False
    >>> isint('501')
    True
    >> isint(5)
    True
    """
    try:
        int(x)
        return True
    except:
        return False

class ACS_Table(object):
    """
    ACS_Table -- A class to model ACS table meta data.
    """
    def __init__(self, table_id):
        """
        table_id -- str -- ID of Table
        """
        self._data = {}
        self._data['Table ID'] = table_id
        self._data['Sequences'] = {}
        self._data['Columns'] = []
        if DEBUG: print "\nNew Table:", table_id
        self._cur_prefix = ""
        self._rows_processed = 0
        self._seq = -1
        self._column = 0
    @property
    def json(self):
        num_sequences = len(self._data['Sequences'])
        assert num_sequences >= 1
        if num_sequences > 1:
            values = self._data['Sequences'].values()
            # Get Universe
            universe = [x['Universe'] for x in values]
            assert len(set(universe)) == 1
            universe = universe[0]
            # Get Title
            title = [x['Table Title'] for x in values]
            assert len(set(title)) == 1
            title = title[0]
            # Get Subject
            subject = [x['Subject Area'] for x in values]
            assert len(set(subject)) == 1
            subject = subject[0]
        else:
            value = self._data['Sequences'].values()[0]
            universe = value['Universe']
            title = value['Table Title']
            subject = value['Subject Area']
        doc = {}
        doc["title"] = title.title()
        doc["universe"] = universe
        doc["subject"] = subject
        doc["tid"] = self._data['Table ID']
        if doc["tid"] in aval4blks:
            doc["blockgrps"] = aval4blks[doc["tid"]]
        else:
            doc["blockgrps"] = False
        if doc["tid"] in avalnonblks:
            doc["restrictions"] = avalnonblks[doc["tid"]]
        else:
            doc["restrictions"] = False
        doc["columns"] = [dict(zip(("cid","ColumnTitle"),map(str,col[-2:]))) for col in self._data['Columns']]
        try:
            return json.dumps(doc)
        except:
            print "HERE",
            print doc["tid"]
            return ""
    def process_row(self, row):
        assert row['File ID'] == 'ACSSF'
        assert row['Table ID'] == self._data['Table ID']
        sq = row['Sequence Number']
        if row['Line Number'] == '' and row['Start Position'] != '':
            self._data['Sequences'][sq] = {}
            self._data['Sequences'][sq]['Start Position'] = int(row['Start Position'])
            self._data['Sequences'][sq]['Cells'] = int(row['Total Cells in Table'].split()[0])
            self._data['Sequences'][sq]['Table Title'] = row['Table Title']
            self._data['Sequences'][sq]['Subject Area'] = row['Subject Area']
            self._seq = row['Sequence Number']
            self._column = int(row['Start Position']) - 1 #Make zero-offset
        elif row['Line Number'] == '' and row['Start Position'] == '':
            assert row['Table Title'].startswith('Universe:')
            self._data['Sequences'][sq]['Universe'] = row['Table Title'].lstrip('Universe: ')
        else:
            ln = row['Line Number'].strip()
            if isint(ln):
                if DEBUG: print "\t\t"+self._cur_prefix+row['Table Title']
                title = self._cur_prefix+row['Table Title']
                col = self._column
                id = row['Table ID'] +'%0.3d'%(int(row['Line Number']))
                self._data['Columns'].append((int(sq),col,id,title))
                self._column += 1
            else:
                if DEBUG: print "\tSetting Prefix",row['Table Title']
                self._cur_prefix = row['Table Title']+" "
        self._rows_processed += 1



fname = "Sequence_Number_and_Table_Number_Lookup.txt"
fmd5 = {} #of original.
fmd5['2010'] = '09f40017cda448a96cb24cdc62a4857b'
fmd5['2011'] = '575e59883e8515a271c17f1946810a28'
baseurl = 'http://www2.census.gov/acs'+config.ACSYEAR+'_5yr/summaryfile/'
if not os.path.exists(fname):
    url = urllib.urlopen(baseurl+fname)
    dat = url.read()
    url.close()
    if hashlib.md5(dat).hexdigest() != fmd5[config.ACSYEAR]:
        print 10*"*"+" WARNING! "+10*"*"
        print "Downloaded file seems to be corrupt!"
        print "Please download:",baseurl+fname
    else:
        o = open(fname,'w')
        ### The "ascii" file contains non-ascii chars.
        ### Are these people using word?
        o.write(dat.replace('\x93','').replace('\x94',''))
        o.close()
input = pysal.open(fname,'r','csv')
input.cast('Sequence Number',str)
header = input.header

if DEBUG: print header

tables = {}

for line in input:
    row = dict(zip(header,line))
    if row['File ID'] != 'ACSSF':
        raise ValueError, "Bad input"
    #########################################################
    # Sequences 109 through 118 are specific to Puerto Rico #
    #########################################################
    sq = int(row['Sequence Number'])
    if sq >= 109 and sq <= 118:
        if not row['Table ID'].endswith('PR'):
          row['Table ID'] = row['Table ID']+'PR'
    #########################################################
    tid = row['Table ID']
    if tid not in tables:
        tables[tid] = ACS_Table(tid)
    table = tables[tid]
    table.process_row(row)


o = open('tables.json','w')
idx = '{"index": {"_type": "acsTable", "_id": "%d", "_index": "demos"}}'
for i,doc in enumerate(tables.values()):
    c = i+1
    o.write(idx%c)
    o.write('\n')
    o.write(doc.json)
    o.write('\n')
o.close()

o = open(os.path.join(config.PYACS_DATAPATH,'column_lookup.csv'),'w')
o.write('CID,SEQ,IDX\n')
for table in tables:
    for col in tables[table]._data['Columns']:
        seq,idx,cid,name = col
        o.write(','.join(map(str,[cid,seq,idx])) +'\n')
o.close()
