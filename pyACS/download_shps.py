"""
Download the "Generalized" boundary files.
Good for display, but not analysis
"""
import os
import pysal
import urllib
import config
import glob
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

def CODE_LOOKUP():
    """ 
    Conveniently avoid manually looking-up a census fips and summary level codes

        >>> code("tx") 
        >>> code("TEXAS")
        >>> code("north carolina")
        >>> code("block")
        >>> code("tract")
        >>> code("block group")
    """
    # Source: http://factfinder2.census.gov/help/en/glossary/s/summary_level_code_list.htm
    GEO_CODES = {}
    GEO_CODES['County'] = '050'
    GEO_CODES['Tract'] = '140'
    GEO_CODES['Block Group'] = '150'
    GEO_CODES['Block'] = '750'
    GEO_CODES['Place'] = '160'
    GEO_CODES['City'] = '170'
    GEO_CODES['State-Congressional'] = '500'
    GEO_CODES['State-Legislative--Upper'] = '610'
    GEO_CODES['State-Legislative-Lower'] = '620'
    GEO_CODES['zipcode'] = '860'
    GEO_CODES['Elementary'] = '950'
    GEO_CODES['Secondary'] = '960'
    GEO_CODES['Unified'] = '970'

    state2code={}
    stateab2code=zip(config.STATE_AB,config.STATE_FIPS)
    statename2code=zip([name.lower()for name in config.STATE_NAME],config.STATE_FIPS)
    state2code.update(dict(stateab2code))
    state2code.update(dict(statename2code))
    code=state2code
    code.update(dict(GEO_CODES))
    return code

CODE_LOOKUP=CODE_LOOKUP()

CENSUS_URL = "http://www2.census.gov/geo/tiger/GENZ2010/"
SHAPEFILE_TEMPLATE = "gz_2010_{state}_{geo}_00_500k.zip" #2digit FIPS, 3 digit Summary Level

def fetch_shapefile(state,geolevel):
    """
        >>> fetch_shapefile("texas","Block Group")
        saves these file to the current dir:
            texas_Block_Group.shp
            texas_Block_Group.dbf
            texas_Block_Group.shx
            texas_Block_Group.prj
    """    
    fname=SHAPEFILE_TEMPLATE.format(state=CODE_LOOKUP[state],geo=CODE_LOOKUP[geolevel])
    print fname
    url = urllib.urlopen(CENSUS_URL+fname)
    dat = url.read()
    with open(fname,'wb') as o:
        o.write(dat)
    r=os.system('unzip '+fname)
    print "unzip result", r
    fname.replace('.zip','.shp')
    fname.replace('.zip','.dbf')
    # rename to a easier to understand filename:
    prefix=fname.split(".")[0]
    for filename in glob.glob(prefix+'*.*'):
        suffix=filename.split(".")[1]
        print filename
        os.rename(filename,state+"_"+geolevel.replace(" ","_")+"."+suffix)

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
    #dl_merge(outname='/pyacs/tracts11',sumlevel='140')
    fetch_shapefile("texas","Block Group")
