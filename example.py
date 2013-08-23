"""make a numpy.array of census tract income values ordered as the tract shapefile

        Requirement 1.  Follow the README instructions on how you need to fetch the census datasets

        Requirement 2.  Run $python /pyACS/download_shps.py to fetch each state's shapefile of
            tracts and then merge them all into 1 large shapefile written to /pyacs

        Warning: over 20 minutes to run since its pulls down many shapefiles

"""
import numpy
import pysal
import pyACS

dbf = pysal.open('/pyacs/tracts11.dbf') 
order = dbf.by_col('GEOID') # get the geoids, in same order as .shp
t = pyACS.ACS()
c = t.get_ordered(order, 'B19013001') # tract income values, matching order as .shp
c = numpy.nan_to_num(c) # replace null values with 0
