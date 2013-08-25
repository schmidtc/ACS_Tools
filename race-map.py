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

"""
import numpy
import pysal
import pyACS

# get a list of census tract ids from the shapefile
dbf = pysal.open('/pyacs/tracts11.dbf') 
order = dbf.by_col('GEOID') # get the geoids, in same order as .shp
t = pyACS.ACS()

# get arrays of total pop and black pop values in the same order as the census tract ids
total = t.get_ordered(order, 'B01003001')
total = numpy.array(total) 
black = t.get_ordered(order, 'B02009001')
black = numpy.array(black) 

# replace null values with 0, so no division by zero
print len(total[total==0]), "zero values"
total[total==0] = np.nan # convert zeros to nan 
print numpy.sum(numpy.isnan(total)), "nan values"

# calculate location quotients
grandtotal=total.sum() # 310,346,358
blacktotal=black.sum() # 41,917,507
blackportionusa=blacktotal/grandtotal # 0.135
lqs=black/total/blackportionusa

from pysal.esda.mapclassify import *
# source: http://pysal.org/1.3/_modules/pysal/esda/mapclassify.html
#fj=Fisher_Jenks(lqs) # takes too long for real-time map rendering
p=Percentiles(lqs, pct=[1,10,40,60,90,99,100])
print p.bins
print p.counts
print p.k

def make_lqs():
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

