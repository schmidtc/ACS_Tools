import numpy
import pysal
import pyACS
db = pysal.open('/pyacs/tracts11.dbf')
order = db.by_col('GEOID')

t = pyACS.ACS()
#c = t['B19013001']

c = t.get_ordered(order, 'B19013001')
c = numpy.nan_to_num(c)
