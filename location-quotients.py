""" location quotients (LQs)

    Overview: 
    
        extract census variables, such as counts by race, and transform them into LQs 

    Source of variable names matched to variable codes:

        Census Variables Dict: http://www2.census.gov/acs2011_5yr/summaryfile/ACS_2007_2011_SF_Tech_Doc.pdf

        * B01003 Total Population
        * B03003 Hispanic Or Latino Origin
        * B02009 Black Or African American Alone Or In Combination With One Or More Other Races

    quasiLQs:

        1. uniform scale centered at zero  -2 -1 -.5 0 +.5 +1 + 2


"""
import numpy
import pysal
import pyACS
import tables
from numpy import *
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt
#stats.nanmean

# stylized facts:
# 689 of 74,001 tracts have zero population 1%
# 5,529 of 74,001 tracts have black zero population 7%
# 42 million black / 310 million total = .13
# texas fips = 48, 5265 blocks, 390 have zero black population
# the min(quasiLQs) is in DC 52% of the pop to equal state compos

def simple_stats(myarray):
    idx=where(isnan(LQs)==False)[0]
    print "mean ", mean(myarray[idx])
    print "median ", median(myarray[idx])
    print "min ", min(myarray[idx])
    print "max ", max(myarray[idx])

f=tables.open_file("census_variables.h5")
print "pyTable Fields Description: ", f.root.tracts.readout
tract_total=f.root.tracts.readout.cols.tractcount[:] 
tract_black=f.root.tracts.readout.cols.blackcount[:] 

tract_nonblack = tract_total - tract_black

geoids=f.root.tracts.readout.cols.geoid[:] 

N=len(tract_black)
parent = numpy.array([ i[:2] for i in geoids ]) # state parent of each tract
states=list(set(parent))
print len(states), "unique state ids"

# Initialize the state level values
parent_state_total=numpy.zeros(N)
parent_state_black=numpy.zeros(N)
parent_state_nonblack=numpy.zeros(N)

for state in states:
    parent_state_total[parent==state] = tract_total[parent==state].sum()
    parent_state_black[parent==state] = tract_black[parent==state].sum()
    parent_state_nonblack[parent==state] = tract_nonblack[parent==state].sum()

# array needs to be a float to use nan
tract_black = tract_black.astype(numpy.float)
tract_nonblack = tract_nonblack.astype(numpy.float)
tract_total = tract_total.astype(numpy.float)

validtractidx=where(tract_total!=0)[0] # the indexes of tracts that have population
invalidtractidx=where(tract_total==0)[0] # the indexes of tracts with zero population
tract_total[invalidtractidx] = numpy.nan # replace 0 with null values, so no division by zero


# calculate location quotients
numerator=tract_black/tract_total
denomenator=parent_state_black/parent_state_total
LQs = numerator/denomenator

# Quasi-LQs 

# Interpretation: 

# a positive (negative) measurement is percentage of a tract that would need to
# switch their identification to black (non-black) for that tract's to black
# portion to be inline with it's state


# Significance for redistricting: 

# This metric allows for diverging choropleth color schemes, diverging at 0,
# contrasting areas that should not be split by district lines in order to
# preserve black political power, with areas irrelevant for black power,
# relative to the whole state

#quasiLQs = numerator-denomenator
#OR
qLQ = denomenator-numerator

#quasiLQs[validtractidx]

sum((q>-.10) & (q<.10))


# convert back nulls to zeros
# basically putting nulls in as middle bin with grey fill
qLQ[where(isnan(qLQ)==True)[0]]=0

print "quasiLQs:"
simple_stats(quasiLQs)
print "-----------"
print "LQs:"
simple_stats(LQs)

classes=zeros(len(qLQ)).astype(numpy.int)


classes[where(qLQ>.90)]=9
classes[where((qLQ>.80) & (qLQ<.90))]=19
classes[where((qLQ>.70) & (qLQ<.80))]=18
classes[where((qLQ>.60) & (qLQ<.70))]=17
classes[where((qLQ>.50) & (qLQ<.60))]=16
classes[where((qLQ>.40) & (qLQ<.50))]=15
classes[where((qLQ>.30) & (qLQ<.40))]=14
classes[where((qLQ>.20) & (qLQ<.30))]=13
classes[where((qLQ>.10) & (qLQ<.20))]=12

classes[where((qLQ>-.10) & (qLQ<.10))]=11 # GREY

classes[where((qLQ>-.10) & (qLQ<-.20))]=10
classes[where((qLQ>-.20) & (qLQ<-.30))]=9
classes[where((qLQ>-.30) & (qLQ<-.40))]=8
classes[where((qLQ>-.40) & (qLQ<-.50))]=7
classes[where((qLQ>-.50) & (qLQ<-.60))]=6
classes[where((qLQ>-.60) & (qLQ<-.70))]=5
classes[where((qLQ>-.70) & (qLQ<-.80))]=4
classes[where((qLQ>-.80) & (qLQ<-.90))]=3
classes[where((qLQ<-.90))]=2


# Find Grey + 9 black high + 9 nonblackhigh color
"""
Grey: middle: 
    
0xF0F0F0

BuGr-light to dark
0xF7FCFD
0xE5F5F9
0xCCECE6
0x99D8C9
0x66C2A4
0x41AE76
0x238B45
0x006D2C

OrRd
0xFFF7EC
0xFEE8C8
0xFDD49E
0xFDBB84
0xFC8D59
0xEF6548
0xD7301F
0xB30000
0x7F0000

"""

## BELOW DID NOT WORK OUT
## Dissimilarity Index Local, adjusted
#D=(tract_black / parent_state_black) - (tract_nonblack/parent_state_nonblack)
#Dadj= D*parent_state_total/tract_total


if __name__ == '__main__':
    pass
