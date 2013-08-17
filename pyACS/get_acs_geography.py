"""
See http://gwikis.blogspot.com/2012/02/geography-tables.html

This was fixed in the 2011 release and this script is no longer needed.
"""
__author__ = "Charles R. Schmidt <schmidtc@gmail.com>"

from config import STATE_NAME as STATES
from config import ACSGEO as OUT_DIR
from config import DEBUG
import urllib
import re
import os

if not os.path.isdir(OUT_DIR):
    os.mkdir(OUT_DIR)
# extracted from http://www2.census.gov/acs2010_5yr/summaryfile/2006-2010_ACSSF_By_State_By_Sequence_Table_Subset/ using vim and python

BASE_URL = "http://www2.census.gov/acs2010_5yr/summaryfile/2006-2010_ACSSF_By_State_By_Sequence_Table_Subset/"
DATA_URL = "/Tracts_Block_Groups_Only/"


geog_file = re.compile("g20105..\.csv") # .. will match the state's abreviation

for state in STATES:
    if DEBUG: print "Working on",state
    directory = urllib.urlopen(BASE_URL+state+DATA_URL).read()
    geo = geog_file.findall(directory)[0]
    if DEBUG: print "Found geofile: ",geo
    csv = urllib.urlopen(BASE_URL+state+DATA_URL+geo).read()
    if DEBUG: print "writing ",geo,"\n"
    out = open(os.path.join(OUT_DIR,geo),'w')
    out.write(csv)
    out.close()
