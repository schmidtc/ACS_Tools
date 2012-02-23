__author__ = "Charles R. Schmidt <schmidtc@gmail.com>"

import config
import os
DEBUG = config.DEBUG

#extracted from XLS template: http://www2.census.gov/acs2010_5yr/summaryfile/UserTools/2010_SummaryFileTemplates.zip
GEOHEADER = ['FILEID', 'STUSAB', 'SUMLEVEL', 'COMPONENT', 'LOGRECNO', 'US', 'REGION', 'DIVISION', 'STATECE', 'STATE', 'COUNTY', 'COUSUB', 'PLACE', 'TRACT', 'BLKGRP', 'CONCIT', 'AIANHH', 'AIANHHFP', 'AIHHTLI', 'AITSCE', 'AITS', 'ANRC', 'CBSA', 'CSA', 'METDIV', 'MACC', 'MEMI', 'NECTA', 'CNECTA', 'NECTADIV', 'UA', 'BLANK', 'CDCURR', 'SLDU', 'SLDL', 'BLANK', 'BLANK', 'BLANK', 'SUBMCD', 'SDELM', 'SDSEC', 'SDUNI', 'UR', 'PCI', 'BLANK', 'BLANK', 'PUMA5', 'BLANK', 'GEOID', 'NAME', 'BTTR', 'BTBG', 'BLANK']
GEODESCRIPTIONS = ['Always equal to ACS Summary File identification', 'State Postal Abbreviation', 'Summary Level', 'Geographic Component', 'Logical Record Number', 'US ', 'Census Region', 'Census Division', 'State (Census Code)', 'State (FIPS Code)', 'County of current residence', 'County Subdivision (FIPS)', 'Place (FIPS Code)', 'Census Tract', 'Block Group', 'Consolidated City', 'American Indian Area/Alaska Native Area/ Hawaiian Home Land (Census)', 'American Indian Area/Alaska Native Area/ Hawaiian Home Land (FIPS)', 'American Indian Trust Land/ Hawaiian Home Land Indicator', 'American Indian Tribal Subdivision (Census) ', 'American Indian Tribal Subdivision (FIPS)', 'Alaska Native Regional Corporation (FIPS)', 'Metropolitan and Micropolitan Statistical Area', 'Combined Statistical Area', 'Metropolitan Statistical Area-Metropolitan Division', 'Metropolitan Area Central City', 'Metropolitan/Micropolitan Indicator Flag ', 'New England City and Town Area', 'New England City and Town Combined Statistical Area', 'New England City and Town Area Division', 'Urban Area', 'Reserved Future Use', 'Current Congressional District ***', 'State Legislative District Upper', 'State Legislative District Lower', 'Reserved Future Use', 'Reserved Future Use', 'Reserved Future Use', 'Subminor Civil Division (FIPS)', 'State-School District (Elementary)', 'State-School District (Secondary)', 'State-School District (Unified)', 'Urban/Rural', 'Principal City Indicator', 'Reserved Future Use', 'Reserved Future Use', 'Public Use Microdata Area 5% File', 'Reserved Future Use', 'Geographic Identifier', 'Area Name', 'Tribal Tract', 'Tribal Block Group', 'Reserved Future Use']

class GEO(object):
    # Field descriptions:
    # >>> for a,b in zip(GEOHEADER,GEODESCRIPTIONS): print a.rjust(10),'  --  ',b
    """
    Fields in GEO File:
        FILEID   --   Always equal to ACS Summary File identification
        STUSAB   --   State Postal Abbreviation
      SUMLEVEL   --   Summary Level
     COMPONENT   --   Geographic Component
      LOGRECNO   --   Logical Record Number
            US   --   US 
        REGION   --   Census Region
      DIVISION   --   Census Division
       STATECE   --   State (Census Code)
         STATE   --   State (FIPS Code)
        COUNTY   --   County of current residence
        COUSUB   --   County Subdivision (FIPS)
         PLACE   --   Place (FIPS Code)
         TRACT   --   Census Tract
        BLKGRP   --   Block Group
        CONCIT   --   Consolidated City
        AIANHH   --   American Indian Area/Alaska Native Area/ Hawaiian Home Land (Census)
      AIANHHFP   --   American Indian Area/Alaska Native Area/ Hawaiian Home Land (FIPS)
       AIHHTLI   --   American Indian Trust Land/ Hawaiian Home Land Indicator
        AITSCE   --   American Indian Tribal Subdivision (Census) 
          AITS   --   American Indian Tribal Subdivision (FIPS)
          ANRC   --   Alaska Native Regional Corporation (FIPS)
          CBSA   --   Metropolitan and Micropolitan Statistical Area
           CSA   --   Combined Statistical Area
        METDIV   --   Metropolitan Statistical Area-Metropolitan Division
          MACC   --   Metropolitan Area Central City
          MEMI   --   Metropolitan/Micropolitan Indicator Flag 
         NECTA   --   New England City and Town Area
        CNECTA   --   New England City and Town Combined Statistical Area
      NECTADIV   --   New England City and Town Area Division
            UA   --   Urban Area
         BLANK   --   Reserved Future Use
        CDCURR   --   Current Congressional District ***
          SLDU   --   State Legislative District Upper
          SLDL   --   State Legislative District Lower
         BLANK   --   Reserved Future Use
         BLANK   --   Reserved Future Use
         BLANK   --   Reserved Future Use
        SUBMCD   --   Subminor Civil Division (FIPS)
         SDELM   --   State-School District (Elementary)
         SDSEC   --   State-School District (Secondary)
         SDUNI   --   State-School District (Unified)
            UR   --   Urban/Rural
           PCI   --   Principal City Indicator
         BLANK   --   Reserved Future Use
         BLANK   --   Reserved Future Use
         PUMA5   --   Public Use Microdata Area ? 5% File
         BLANK   --   Reserved Future Use
         GEOID   --   Geographic Identifier
          NAME   --   Area Name
          BTTR   --   Tribal Tract
          BTBG   --   Tribal Block Group
         BLANK   --   Reserved Future Use
    """
    def __init__(self,state):
        path = os.path.join(config.ACSGEO, "g20105%s.csv"%state)
        data = open(path,'r').readlines()
        self.data = [line.split(',') for line in data]
    def get(self,fieldName,sumlevel_filter=None):
        """
        Get the specified field at the specified summary level.
        """
        if fieldName not in GEOHEADER:
            raise KeyError,"%s is not a valid field"%fieldName
        idx = GEOHEADER.index(fieldName)
        if sumlevel_filter:
            idxsum = GEOHEADER.index('SUMLEVEL')
            return [x[idx] for x in self.data if x[idxsum]==sumlevel_filter]
        else:
            return [x[idx] for x in self.data]
        
