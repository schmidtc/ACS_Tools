""" location quotients (LQs)

    LQ: 

        a metric of spatial concentration in a single area of an ethnic
        group or industry group compared to all other groups, and all other areas. 

    Overview: 
    
        extract census variables, such as counts by race, and transform them into LQs 

TODO:

1. uniform scale centered at zero  -2 -1 -.5 0 +.5 +1 + 2
2. discretization n=null, and transform to null ,, or 0,1,2,3,4,5,6,7,8,9

[Census Variables:](http://www2.census.gov/acs2011_5yr/summaryfile/ACS_2007_2011_SF_Tech_Doc.pdf)

* B01003 Total Population
* B03003 Hispanic Or Latino Origin
* B02009 Black Or African American Alone Or In Combination With One Or More Other Races

TODO: 
- sava data as a pytable
- handle nan better for map classification
- do it by state

"""
import numpy
import pysal
import pyACS
import tables

# stylized facts:
# 689 of 74,001 tracts have zero population 1%
# 5,529 of 74,001 tracts have black zero population 7%
# 42 million black / 310 million total = .13
# texas fips = 48, 5265 blocks, 390 have zero black population

f=tables.open_file("census_variables.h5")
print "pyTable Fields Description: ", f.root.tracts.readout
tract_total=f.root.tracts.readout.cols.tractcount[:] 
tract_black=f.root.tracts.readout.cols.blackcount[:] 
geoids=f.root.tracts.readout.cols.geoid[:] 

N=len(tract_black)
parent = numpy.array([ i[:2] for i in geoids ]) # state parent of each tract
states=list(set(parent))
print len(states), "unique state ids"

parent_state_total=numpy.zeros(N)
parent_state_black=numpy.zeros(N)

for state in states:
    parent_state_total[parent==state] = tract_total[parent==state].sum()
    parent_state_black[parent==state] = tract_black[parent==state].sum()

# array needs to be a float to use nan
tract_black = tract_black.astype(numpy.float)
tract_total = tract_total.astype(numpy.float)

# replace 0 with null values, so no division by zero
Nzeros=len(tract_total[tract_total==0])
print Nzeros, "count zero values"
if Nzeros >0:
    tract_total[tract_total==0] = numpy.nan # convert zeros to nan 
    Nnulls=numpy.sum(numpy.isnan(tract_total)), "count nan values"
    if Nzeros==Nnulls: print "OK now"



# calculate location quotients
numerator=tract_black/tract_total
denomenator=parent_state_black/parent_state_total

LQs = numerator/denomenator
print numpy.isnan(LQs).sum() , "count nan in LQs"
# remove 689 tracts with (zero pop) nans
# so we can use pysal's classification code
LQs = LQs[numpy.logical_not(numpy.isnan(LQs))]


from pysal.esda.mapclassify import *
# source: http://pysal.org/1.3/_modules/pysal/esda/mapclassify.html
#fj=Fisher_Jenks(lqs) # takes too long for real-time map rendering
p=Percentiles(LQs, pct=[1,10,40,60,90,99,100])
print p.bins
print p.counts
print p.k


"""
http://colorbrewer2.org/ PRgn
BIN COUNT COLOR COLORLABEL
0-1% 4840       (27, 120, 55)       GREEN
1-10% 2492      (127, 191, 123)
10-40% 21993    (217, 240, 211)
40-60% 14662    (247, 247, 247)
60-90% 21993    (231, 212, 232)
90-99% 6598     (175, 141, 195)
99-100 734      (118, 42, 131)      PURPLE 0x762A83
Each color should be in HEX RGB format beginning with a '#'.
The first color in the list provided is assigned to class 2, the next to class 3 and so on.

Class 0 and Class 1 are reserved for the background and borders respectivly.
The Background color should NOT be used anywhere else in the color scheme.
Since this color will be made transparent.
"""

fillcolors=[
    "#0x762A83",
    "#0xAF8DC3",
    "#0xE7D4E8",
    "#0xF7F7F7",
    "#0xD9F0D3",
    "#0x7FBF7B",
    "#0x1B7837"
    ]

classes = numpy.zeros(N)

classes


def make_lqs():
    pass



if __name__ == '__main__':
    pass
