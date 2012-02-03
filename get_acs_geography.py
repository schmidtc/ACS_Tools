__author__ = "Charles R. Schmidt <schmidtc@gmail.com>"

import urllib
import re
import os

DEBUG = True

OUT_DIR = "ACS_GEO"
if not os.path.isdir(OUT_DIR):
    os.mkdir(OUT_DIR)
# extracted from http://www2.census.gov/acs2010_5yr/summaryfile/2006-2010_ACSSF_By_State_By_Sequence_Table_Subset/ using vim and python
STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "DistrictOfColumbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "NewHampshire", "NewJersey", "NewMexico", "NewYork", "NorthCarolina", "NorthDakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "PuertoRico", "RhodeIsland", "SouthCarolina", "SouthDakota", "Tennessee", "Texas", "UnitedStates", "Utah", "Vermont", "Virginia", "Washington", "WestVirginia", "Wisconsin", "Wyoming"]

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
