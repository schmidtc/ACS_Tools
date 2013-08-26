"""Get Data for a Map of Location Quotients by Race

1. calculate LQs
2. calculate where to break bins
3. associated each bin of areas to a color

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


### IN THE FUTURE I WILL REPLACE THIS WITH pyTABLES

# Extract tract ids from the shapefile
dbf = pysal.open('/pyacs/tracts11.dbf')
geoids = dbf.by_col('GEOID') # get the geoids, in same geoids as .shp
# Question: why is GEOID != STATE + COUNTY + TRACT ?

# The Magic
datasetObj = pyACS.ACS()
# arrays of total pop and black pop values ordered by shapefile's tract ids
tract_total = numpy.array(datasetObj.get_ordered(geoids, 'B01003001'))
tract_black = numpy.array(datasetObj.get_ordered(geoids, 'B02009001'))
N=len(tract_black)

# demoninator: parent state's black population / total population
parent = numpy.array([ i[:2] for i in geoids ]) # state parent of each tract
states=list(set(parent))
print len(states), "unique state ids"

parent_state_total=numpy.zeros(N)
parent_state_black=numpy.zeros(N)

for state in states:
    parent_state_total[parent==state] = tract_total[parent==state].sum()
    parent_state_black[parent==state] = tract_black[parent==state].sum()


# replace 0 with null values, so no division by zero
#Nzeros=len(myarray[myarray==0]), "count zero values"
#print Nzeros, "count zero values"
#if Nzeros >0:
#    myarray[myarray==0] = numpy.nan # convert zeros to nan 
#    Nnulls=numpy.sum(numpy.isnan(myarray)), "count nan values"
#    if Nzeros==Nnulls:
#        return myarray
#    else:
#        print "ERROR: bug in function"



# calculate location quotients
numerator=tract_black/tract_total
denomenator=parent_state_black/parent_state_total

LQs = numerator/denomenator
print numpy.isnan(lqs).sum() , "count nan in LQs"
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
99-100 734      (118, 42, 131)      PURPLE

(27, 120, 55)     
(127, 191, 123)
(217, 240, 211)
(247, 247, 247)
(231, 212, 232)
(175, 141, 195)
(118, 42, 131)    

Each color should be in HEX RGB format beginning with a '#'.
The first color in the list provided is assigned to class 2, the next to class 3 and so on.

Class 0 and Class 1 are reserved for the background and borders respectivly.
The Background color should NOT be used anywhere else in the color scheme.
Since this color will be made transparent.
"""


def make_lqs():
    ## The old way was to use national level demoninator instead of statelevel:
    #grandtotal=total.sum() # 310,346,358
    #blacktotal=black.sum() # 41,917,507
    #blackportionusa=blacktotal/grandtotal # 0.135

    """
    Examples
    --------

    >>> cal=load_example()
    >>> fj=Fisher_Jenks(cal)
    >>> fj.adcm
    832.8900000000001
    >>> fj.bins
    [110.73999999999999, 192.05000000000001, 370.5, 722.85000000000002, 4111.4499999999998]
    >>> fj.counts
    array([50,  2,  4,  1,  1])


    ### PERCENTILES
    >>> p=Percentiles(dataarray, pct=[1,10,50,90,99,100])
    >>> p.bins
    array([  1.35700000e-01,   5.53000000e-01,   9.36500000e+00,
             2.13914000e+02,   2.17994800e+03,   4.11145000e+03])
    >>> p.counts
    array([ 1,  5, 23, 23,  5,  1])
    >>> p2=Percentiles(cal,pct=[50,100])
    >>> p2.bins
    array([    9.365,  4111.45 ])
    >>> p2.counts
    array([29, 29])
    >>> p2.k
    """
    pass


def _test():
    import doctest
    doctest.testmod(verbose=True)

if __name__ == '__main__':
    _test()

