import numpy
import pyACS

t = pyACS.ACS()
c = t['B19013001']
c = numpy.nan_to_num(c)
