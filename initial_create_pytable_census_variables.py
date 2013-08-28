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

filename = "census_variables.h5"
h5file = open_file(filename, mode = "w", title = "Census Variables")
group = h5file.create_group("/", 'tracts', 'Tract Level')# new group under "/" (root)
tract_race_table = h5file.create_table(group, 'readout', TractModel, "Race Counts")# new table of group
# Fill the table with 10 particles
tract = tract_race_table.row
for i in xrange(N):
    tract_race_table.row['geoid']  = geoids[i]
    tract_race_table.row['blackcount'] = tract_black[i]
    tract_race_table.row['tractcount'] = tract_total[i]
    tract.append()
# Close (and flush) the file
h5file.close()
