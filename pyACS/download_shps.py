"""
Download the "Generalized" boundary files.
Good for display, but not analysis
"""
import os
import pysal
import urllib
import config
DEBUG = config.DEBUG


#base_url = "http://www2.census.gov/geo/tiger/GENZ2010/"
#name_template = "gz_2010_%s_%s_00_500k.zip" #2digit FIPS, 3 digit Summary Level
# gz_2010_ss_lll_vv_rr.zip
#   ss = state fips code or 'us' for a national level file 
#   lll = summary level code
#   vv = 2-digit version code 
#   rr = resolution level
#       *500k = 1:500,000 
#        5m = 1:5,000,000 
#        20m = 1:20,000,000
#base_url = "http://www2.census.gov/geo/tiger/TIGER2010/BG/2010/"
#name_template = "tl_2010_%s_bg10.zip" #2digit FIPS
base_url = "http://www2.census.gov/geo/tiger/TIGER2011/TRACT/"
name_template = "tl_2011_%s_tract.zip" #2digit FIPS

def dl_merge(outname="tracts",sumlevel="140"):
    os.chdir('/tmp')
    outshp = pysal.open(outname+'.shp','w')
    outdbf = pysal.open(outname+'.dbf','w')
    for st in config.STATE_FIPS:
        fname = name_template%(st)#,sumlevel)
        if DEBUG: print fname
        url = urllib.urlopen(base_url+fname)
        dat = url.read()
        if not os.path.exists(fname):
            with open(fname,'wb') as o:
                o.write(dat)
            os.system('unzip '+fname)
        shp = pysal.open(fname.replace('.zip','.shp'),'r')
        for x in shp:
            outshp.write(x)
        dbf = pysal.open(fname.replace('.zip','.dbf'),'r')
        outdbf.header = dbf.header
        outdbf.field_spec = dbf.field_spec
        for row in dbf:
            outdbf.write(row)
        os.remove(fname)
        os.remove(fname.replace('.zip','.shp'))
        os.remove(fname.replace('.zip','.shx'))
        os.remove(fname.replace('.zip','.dbf'))
        os.remove(fname.replace('.zip','.shp.xml'))
        os.remove(fname.replace('.zip','.prj'))
    outshp.close()
    outdbf.close()
if __name__=='__main__':
    dl_merge(outname='/pyacs/tracts11',sumlevel='140')
