"""
pyACS -- config -- Settings for data paths and GLOBAL values
"""
DEBUG = True

PYACS_DATAPATH = "/pyacs/"
ACS_PATH = "/pyacs/SUMFILE/"
ACSFILE = "20115" #2011 5-year
ACSGEO = "/pyacs/GEO/"
ACSSHPS = "/pyacs/shps"
# The follow series are in no particular order and should not be assumed comparable.
STATE_AB = ['ak', 'al', 'ar', 'az', 'ca', 'co', 'ct', 'dc', 'de', 'fl', 'ga', 'hi', 'ia', 'id', 'il', 'in', 'ks', 'ky', 'la', 'ma', 'md', 'me', 'mi', 'mn', 'mo', 'ms', 'mt', 'nc', 'nd', 'ne', 'nh', 'nj', 'nm', 'nv', 'ny', 'oh', 'ok', 'or', 'pa', 'pr', 'ri', 'sc', 'sd', 'tn', 'tx', 'us', 'ut', 'va', 'vt', 'wa', 'wi', 'wv', 'wy']
# extracted from http://www2.census.gov/acs2010_5yr/summaryfile/2006-2010_ACSSF_By_State_By_Sequence_Table_Subset/ using vim and python
STATE_NAME = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "DistrictOfColumbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "NewHampshire", "NewJersey", "NewMexico", "NewYork", "NorthCarolina", "NorthDakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "PuertoRico", "RhodeIsland", "SouthCarolina", "SouthDakota", "Tennessee", "Texas", "UnitedStates", "Utah", "Vermont", "Virginia", "Washington", "WestVirginia", "Wisconsin", "Wyoming"]
STATE_FIPS = ['01', '02', '04', '05', '06', '08', '09', '10', '11', '12', '13', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '44', '45', '46', '47', '48', '49', '50', '51', '53', '54', '55', '56', '72']
SUMLEVEL = {}
SUMLEVEL['Region'] = '020'
SUMLEVEL['Division'] = '030'
SUMLEVEL['State'] = '040'
SUMLEVEL['State-County'] = '050'
SUMLEVEL['State-County-County Subdivision'] = '060'
SUMLEVEL['State-County-County Subdivision-Subminor Civil Division'] = '067'
SUMLEVEL['State-County-Census Tract'] = '140'
SUMLEVEL['State-County-Census Tract-Block Group'] = '150'
SUMLEVEL['State-Place'] = '160'
SUMLEVEL['State-Consolidated City'] = '170'
SUMLEVEL['State-Alaska Native Regional Corporation'] = '230'
SUMLEVEL['American Indian Area/Alaska Native Area/Hawaiian Home Land'] = '250'
SUMLEVEL['American Indian Area-Tribal Subdivision/Remainder'] = '251'
SUMLEVEL['American Indian Area/Alaska Native Area (Reservation or Statistical Entity Only)'] = '252'
SUMLEVEL['American Indian Area (Off-Reservation Trust Land Only)/Hawaiian Home Land'] = '254'
SUMLEVEL['American Indian Area-Tribal Census Tract'] = '256'
SUMLEVEL['American Indian Area-Tribal Census Tract-Tribal Block Group'] = '258'
SUMLEVEL['Metropolitan Statistical Area/Micropolitan Statistical Area'] = '310'
SUMLEVEL['Metropolitan Statistical Area-Metropolitan Division'] = '314'
SUMLEVEL['Combined Statistical Area'] = '330'
SUMLEVEL['Combined Statistical Area-Metropolitan Statistical Area/Micropolitan Statistical Area '] = '332'
SUMLEVEL['Combined New England City and Town Area'] = '335'
SUMLEVEL['Combined New England City and Town Area-New England City and Town Area'] = '337'
SUMLEVEL['New England City and Town Area'] = '350'
SUMLEVEL['New England City and Town Area-State-Principal City'] = '352'
SUMLEVEL['New England City and Town Area (NECTA)-NECTA Division'] = '355'
SUMLEVEL['State-New England City and Town Area-Principal City'] = '361'
SUMLEVEL['State-Congressional District (111th)'] = '500'
SUMLEVEL['State-State Legislative District (Upper Chamber)'] = '610'
SUMLEVEL['State-State Legislative District (Lower Chamber)'] = '620'
SUMLEVEL['State-County-Voting District/Remainder'] = '700'
SUMLEVEL['5-Digit ZIP code Tabulation Area'] = '860'
SUMLEVEL['State-School District (Elementary)/Remainder'] = '950'
SUMLEVEL['State-School District (Secondary)/Remainder'] = '960'
SUMLEVEL['State-School District (Unified)/Remainder'] = '970'
