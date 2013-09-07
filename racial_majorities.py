""" percent of each race in an area

Census Variables: http://www2.census.gov/acs2011_5yr/summaryfile/ACS_2007_2011_SF_Tech_Doc.pdf

    * B01003 Total Population
    * B03003 Hispanic Or Latino Origin
    * B02009 Black Or African American Alone Or In Combination With One Or More Other Races
"""
import numpy
import pysal
import pyACS
import tables
import simplejson
from numpy import *
import matplotlib.pyplot as plt

#a = array([[1,2,3],[0,3,NaN]]);
#whereAreNaNs = isnan(a);
#a[whereAreNaNs] = 0;

f=tables.open_file("census_variables.h5")
print "pyTable Fields Description: ", f.root.tracts.readout
tract_total=f.root.tracts.readout.cols.tractcount[:] 
tract_black=f.root.tracts.readout.cols.blackcount[:] 

# array needs to be a float to use nan
# remember 689 tracts with (zero pop) nans
tract_black = tract_black.astype(numpy.float)
tract_total = tract_total.astype(numpy.float)

# replace zeros to null values, so no division by zero
tract_total[tract_total==0] = numpy.nan # convert zeros to nan 

# the main calculation
percent=tract_black/tract_total

# convert back nulls to zeros
percent[where(isnan(percent)==True)[0]]=0
classes=zeros(len(percent)).astype(numpy.int)
classes[where(percent<.50)]=0
classes[where((percent>.50) & (percent<.60))]=3
classes[where((percent>.60) & (percent<.70))]=4
classes[where((percent>.70) & (percent<.80))]=5
classes[where((percent>.80) & (percent<.90))]=6
classes[where(percent>.90)]=7

mapclassesjson=simplejson.dumps(classes.tolist())
with open('blacktractmajorities.json', 'w') as outfile:
  outfile.write(mapclassesjson)

print "percent of black living .90+ areas", sum(tract_black[where(classes==7)])/sum(tract_black)

colors=["#EDF8FB", "#B3CDE3", "#8C96C6", "#8856A7", "#810F7C"]

"""
http://colorbrewer2.org/ 5 colors BuPu sequential
race  percent class color
none   all<50  0     no color
black  50-60   3     #EDF8FB
black  60-70   4     #B3CDE3
black  70-80   5     #8C96C6
black  80-90   6     #8856A7
black  90-100  7     #810F7C

HEX format begins with '#'.
Assign colors to class 2, the next to class 3 and so on.
class 0 and class 1 are reserved for the background and borders respectivly.
"""

if __name__ == '__main__':
    pass
