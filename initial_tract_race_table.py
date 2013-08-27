"""Extract and store census tract data as a pyTable 

    As a pyTable it will be faster to load census variables into memory and start working with in
    numpy
"""
import numpy
import pysal
import pyACS
from tables import *

# Extract using Charlie's ACH 
dbf = pysal.open('/pyacs/tracts11.dbf')
geoids = dbf.by_col('GEOID') # shapefile geoid, 11chars=2state+3county+6tract
datasetObj = pyACS.ACS()
tract_total = numpy.array(datasetObj.get_ordered(geoids, 'B01003001'))
tract_black = numpy.array(datasetObj.get_ordered(geoids, 'B02009001'))
N=len(tract_black)

# Define a pyTable's record that describes a census tract
class TractModel(IsDescription):
    geoid           = StringCol(11)   # geoid
    blackcount        = UInt16Col()     # Unsigned short integer
    tractcount        = UInt16Col()     # Unsigned short integer

filename = "tracts_race.h5"
h5file = open_file(filename, mode = "w", title = "Test file")
group = h5file.create_group("/", 'tracts', 'Tract Attributes')# new group under "/" (root)
table = h5file.create_table(group, 'readout', TractModel, "Race counts")# new table of group
# Fill the table with 10 particles
tract = table.row
for i in xrange(N):
    tract['geoid']  = geoids[i]
    tract['blackcount'] = black[i]
    tract['totalcount'] = total[i]
    tract.append()
# Close (and flush) the file
h5file.close()
