from tables import *
# Define a record that describes a census tract
class Tract(IsDescription):
    geoid           = StringCol(11)   # geoid
    blackcount        = UInt16Col()     # Unsigned short integer
    tractcount        = UInt16Col()     # Unsigned short integer


filename = "tracts_race.h5"
# Open a file in "w"rite mode
h5file = open_file(filename, mode = "w", title = "Test file")
# Create a new group under "/" (root)
group = h5file.create_group("/", 'tracts_race', 'Tracts Race Attributes')
# Create one table on it
table = h5file.create_table(group, 'readout', Tract, "Tract black total example")
# Fill the table with 10 particles
tract = table.row
for i in xrange(N):
    tract['geoid']  = geoids[i]
    tract['blackcount'] = black[i]
    tract['totalcount'] = total[i]
    tract.append()
# Close (and flush) the file
h5file.close()
