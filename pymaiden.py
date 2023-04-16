'''
This module contains a set of eight functions that provide calculations related
to the Maidenhead Grid Locator System used world wide by the Amateur Radio
community. Refer to the readme.md file for information on the Maidenhead Grid
Locator System and the usage of the pymaiden module.

Written by: Kevin Hallquist, WB7BGJ
'''


# ====================================================================
# Module imports:
from pyproj import Geod
import numpy as np
import gridtables # Used for converting between Lat/Lon and grid formats.
import math
import re


# ====================================================================
# Regular expression for matching 2, 4, 6, 8 or 10 digit
# grid ID string. E.g. "AR", "AR09", "AR09ax", "AR09ax09", "AR09ax09AX"
# Persist regular expression patterns to avoid re-compiling on every call
grid_location_pattern_AR = re.compile(r'^[A-R]{2}$')
grid_location_pattern_AR09 = re.compile(r'^[A-R]{2}[0-9]{2}$')
grid_location_pattern_AR09ax = re.compile(r'^[A-R]{2}[0-9]{2}[a-x]{2}$')
grid_location_pattern_AR09ax09 = re.compile(r'^[A-R]{2}[0-9]{2}[a-x]{2}[0-9]{2}$')
grid_location_pattern_AR09ax09AX = re.compile(r'^[A-R]{2}[0-9]{2}[a-x]{2}[0-9]{2}[A-X]{2}$')


# ====================================================================
# Validates correct format of a given grid ID.
# Input parameter: 2, 4, 6, 8 or 10 character grid locator character string
# Returns: True or False
def grid_location_valid_ID(gl_id):

    # Use the regular expression to valid the format of the given grid ID 
    if (len(gl_id)%2 == 0) and (len(gl_id) >= 2) and (len(gl_id) <= 10):
        if (len(gl_id) == 2):
            if grid_location_pattern_AR.match(gl_id):
                return True
            else:
                return False
        elif (len(gl_id) == 4):
            if grid_location_pattern_AR09.match(gl_id):
                return True
            else:
                return False
        elif (len(gl_id) == 6):
            if grid_location_pattern_AR09ax.match(gl_id):
                return True
            else:
                return False
        elif (len(gl_id) == 8):
            if grid_location_pattern_AR09ax09.match(gl_id):
                return True
            else:
                return False
        else:
            if grid_location_pattern_AR09ax09AX.match(gl_id):
                return True
            else:
                return False
    else:
        # Invalid string length
        return False


# ====================================================================
# Find cooresponding grid ID for a given lat/lon location
# Input parameters: Longitude and Latitiude. (Use minus prefix for South and West)
# Returns: A 10 character Grid Locator ID string
def lat_lon_to_grid_ID(lat, lon):
    
    # Check that latitude and longitude values given are within required range
    if not (-90 < lat < 90):
        print('latitude must be -90<=lat<90, given %f\n'%lat)
        return False

    if not (-180 < lon < 180):
        print('longitude must be -180<=lon<180, given %f\n'%lon)
        return False

    # Convert plus/minus 90 deg lat and 180 deg lon format to 180 deg Lat and 360 deg Lon format
    gls_lon = lon + 180.0
    gls_lat = lat + 90.0

    # Created initial empty grid ID string
    grid_ID = ""

    #-----------------------------------------
    # Calculate First Pair (AA-RR)
    # Field, A-R, 18x18, 20 x 10 degrees
    field_lon_index = int(gls_lon/20)
    grid_ID += gridtables.field[field_lon_index]
     
    field_lat_index = int(gls_lat/10)
    grid_ID += gridtables.field[field_lat_index]
        
    #-----------------------------------------
    # Calculate Second Pair (00-99)
    # Square, 0-9, 10x10,  2 x 1 degrees
    lon_square_index_rmdr = (gls_lon - field_lon_index*20)/2
    grid_lon_square = str(int(lon_square_index_rmdr))
    grid_ID += grid_lon_square
    
    lat_square_index_rmdr = (gls_lat - field_lat_index*10)/1
    grid_lat_square = str(int(lat_square_index_rmdr))
    grid_ID += grid_lat_square

    #-----------------------------------------
    # Calculate Third Pair (aa-xx)
    # Subsquare, a-x, 24x24,  5 x 2.5 minutes
    lon_subsquare_rmdr = lon_square_index_rmdr*2 - int(lon_square_index_rmdr)*2
    lon_subsquare_index = int(lon_subsquare_rmdr * 12)
    grid_lon_subsquare = gridtables.subsquare[lon_subsquare_index]
    grid_ID += grid_lon_subsquare

    lat_subsquare_rmdr = lat_square_index_rmdr - int(lat_square_index_rmdr)
    lat_subsquare_index = int(lat_subsquare_rmdr * 24)
    grid_lat_subsquare = gridtables.subsquare[lat_subsquare_index]
    grid_ID += grid_lat_subsquare
    
    #-----------------------------------------
    # Calculate Fourth Pair PAIR (00-99)
    # Extended square, 0-9, 10x10, 30 x 15 seconds
    lon_extsubsquare_rmdr = lon_subsquare_rmdr - (lon_subsquare_index/12)
    lon_extsubsquare_index_rmdr = lon_extsubsquare_rmdr * 120
    grid_ID += str(int(lon_extsubsquare_index_rmdr))

    lat_extsubsquare_rmdr = lat_subsquare_rmdr - (lat_subsquare_index/24)
    lat_extsubsquare_index_rmdr = lat_extsubsquare_rmdr * 240
    grid_ID += str(int(lat_extsubsquare_index_rmdr))

    #-----------------------------------------
    # Calculate Fifth Pair (AA-XX)
    # Super extended square, A-X, 24x24, 1.25 x 0.625 seconds
    lon_supextsquare_rmdr = lon_extsubsquare_rmdr - (int(lon_extsubsquare_index_rmdr)/120)
    lon_supextsquare_index = int(lon_supextsquare_rmdr * 2880)
    grid_ID += gridtables.supsextsubsquare[lon_supextsquare_index]
    
    lat_supextsquare_rmdr = lat_extsubsquare_rmdr - (int(lat_extsubsquare_index_rmdr)/240)
    lat_supextsquare_index = int(lat_supextsquare_rmdr * 5760)
    grid_ID += gridtables.supsextsubsquare[int(lat_supextsquare_index)]

    return grid_ID


# ====================================================================
# Calculates and returns center and four corner coordinates of a given grid ID square
# Input parameter: 2, 4, 6, 8 or 10 character grid locator character string
# Returns: Structure containing lat/lon of the SW, NW, NE, SE corners and Center of the provide grid ID 
def grid_location_ID_bounds(gl_id):
    if (len(gl_id) == 10):
        # Calculate the longitude and latitude of the square's SW corner
        SW_coord_lon = gridtables.lon_field[gl_id[0]] + gridtables.lon_square[gl_id[2]] + gridtables.lon_subsquare[gl_id[4]]/60 + gridtables.lon_extendedsquare[gl_id[6]]/3600 + gridtables.lon_supextsquare[gl_id[8]]/3600
        SW_coord_lat = gridtables.lat_field[gl_id[1]] + gridtables.lat_square[gl_id[3]] + gridtables.lat_subsquare[gl_id[5]]/60 + gridtables.lat_extendedsquare[gl_id[7]]/3600 + gridtables.lat_supextsquare[gl_id[9]]/3600

        # Calculate lon/lat for the other three corners and center from the SW corner location
        NW_coord_lon = SW_coord_lon
        NW_coord_lat = SW_coord_lat + 0.625/3600

        NE_coord_lon = SW_coord_lon + 1.25/3600
        NE_coord_lat = SW_coord_lat +  0.625/3600

        SE_coord_lon = SW_coord_lon + 1.25/3600
        SE_coord_lat = SW_coord_lat

        CEN_coord_lon = SW_coord_lon + 0.625/3600
        CEN_coord_lat = SW_coord_lat + 0.3125/3600
        
    elif (len(gl_id) == 8):
        # Calculate the longitude and latitude of the square's SW corner
        SW_coord_lon = gridtables.lon_field[gl_id[0]] + gridtables.lon_square[gl_id[2]] + gridtables.lon_subsquare[gl_id[4]]/60 + gridtables.lon_extendedsquare[gl_id[6]]/3600
        SW_coord_lat = gridtables.lat_field[gl_id[1]] + gridtables.lat_square[gl_id[3]] + gridtables.lat_subsquare[gl_id[5]]/60 + gridtables.lat_extendedsquare[gl_id[7]]/3600

        # Calculate lon/lat for the other three corners and center from the SW corner location
        NW_coord_lon = SW_coord_lon
        NW_coord_lat = SW_coord_lat + 15/3600

        NE_coord_lon = SW_coord_lon + 30/3600
        NE_coord_lat = SW_coord_lat + 15/3600

        SE_coord_lon = SW_coord_lon + 30/3600
        SE_coord_lat = SW_coord_lat

        CEN_coord_lon = SW_coord_lon + 15/3600
        CEN_coord_lat = SW_coord_lat + 7.5/3600
    
    elif (len(gl_id) == 6):
        # Calculate the longitude and latitude of the square's SW corner
        SW_coord_lon = gridtables.lon_field[gl_id[0]] + gridtables.lon_square[gl_id[2]] + gridtables.lon_subsquare[gl_id[4]]/60
        SW_coord_lat = gridtables.lat_field[gl_id[1]] + gridtables.lat_square[gl_id[3]] + gridtables.lat_subsquare[gl_id[5]]/60
    
        # Calculate lon/lat for the other three corners and center from the SW corner location
        NW_coord_lon = SW_coord_lon
        NW_coord_lat = SW_coord_lat + 2.5/60

        NE_coord_lon = SW_coord_lon + 5/60
        NE_coord_lat = SW_coord_lat +  2.5/60

        SE_coord_lon = SW_coord_lon + 5/60
        SE_coord_lat = SW_coord_lat

        CEN_coord_lon = SW_coord_lon + 2.5/60
        CEN_coord_lat = SW_coord_lat + 1.25/60
    
    elif  (len(gl_id) == 4):
        # Calculate the longitude and latitude of the square's SW corner
        SW_coord_lon = gridtables.lon_field[gl_id[0]] + gridtables.lon_square[gl_id[2]]
        SW_coord_lat = gridtables.lat_field[gl_id[1]] + gridtables.lat_square[gl_id[3]]
    
        # Calculate lon/lat for the other three corners and center from the SW corner location
        NW_coord_lon = SW_coord_lon
        NW_coord_lat = SW_coord_lat + 1

        NE_coord_lon = SW_coord_lon + 2
        NE_coord_lat = SW_coord_lat +  1

        SE_coord_lon = SW_coord_lon + 2
        SE_coord_lat = SW_coord_lat

        CEN_coord_lon = SW_coord_lon + 1
        CEN_coord_lat = SW_coord_lat + .5
   
    elif  (len(gl_id) == 2):
        # Calculate the longitude and latitude of the square's SW corner
        SW_coord_lon = gridtables.lon_field[gl_id[0]]
        SW_coord_lat = gridtables.lat_field[gl_id[1]]
    
        # Calculate lon/lat for the other three corners and center from the SW corner location
        NW_coord_lon = SW_coord_lon
        NW_coord_lat = SW_coord_lat + 10

        NE_coord_lon = SW_coord_lon + 20
        NE_coord_lat = SW_coord_lat +  10

        SE_coord_lon = SW_coord_lon + 20
        SE_coord_lat = SW_coord_lat

        CEN_coord_lon = SW_coord_lon + 10
        CEN_coord_lat = SW_coord_lat + 5
    else:
        return False
    
    grid_bounds = {'NE':{'lat':NE_coord_lat, 'lon':NE_coord_lon},
                   'SE':{'lat':SE_coord_lat, 'lon':SE_coord_lon},
                   'SW':{'lat':SW_coord_lat, 'lon':SW_coord_lon},
                   'NW':{'lat':NW_coord_lat, 'lon':NW_coord_lon},
                   'CEN':{'lat':CEN_coord_lat, 'lon':CEN_coord_lon}}

    return grid_bounds


# ====================================================================
# Calculate the area and perimeter information for a given grid 
# Input parameter: 2, 4, 6, 8 or 10 character grid locator character string
# Returns: Structure containing grid area and perimeter in miles and kilometers
def grid_location_size(gl_id):

    # Define WGS84 as Coordinate Reference Systems (CRS)
    geod = Geod('+a=6378137 +f=0.0033528106647475126')
    
    # Get corner coordinates of grid square
    Grid_Bounds = grid_location_ID_bounds(gl_id)
    
    # Create arrary of lat/lon corner boundary data for requested grid ID
    coordinates = np.array([
    [Grid_Bounds['NE']['lon'], Grid_Bounds['NE']['lat']], 
    [Grid_Bounds['SE']['lon'], Grid_Bounds['SE']['lat']], 
    [Grid_Bounds['SW']['lon'], Grid_Bounds['SW']['lat']], 
    [Grid_Bounds['NW']['lon'], Grid_Bounds['NW']['lat']]])
    lats = coordinates[:,1]
    lons = coordinates[:,0]

    # Retrieve grid square area and perimeter in square meters
    area, perim = geod.polygon_area_perimeter(lons, lats)

    # Convert sqare meters into square miles
    sq_mi = abs(area) * 0.00000038610215854245

    # Convert sqare meters into square miles
    sq_km = abs(area) * 0.000001

    # Convert meters into miles
    perim_mi = perim * 0.00062137119

    # Convert meters into kilometers
    perim_km = perim * 0.001

    # Calculate distance of north and south grid lines and the meridian line                       
    n_dist = lat_lon_distance(Grid_Bounds['NE']['lat'],Grid_Bounds['NE']['lon'],Grid_Bounds['NW']['lat'],Grid_Bounds['NW']['lon'])
    s_dist = lat_lon_distance(Grid_Bounds['SE']['lat'],Grid_Bounds['SE']['lon'],Grid_Bounds['SW']['lat'],Grid_Bounds['SW']['lon'])
    m_dist = lat_lon_distance(Grid_Bounds['NE']['lat'],Grid_Bounds['NE']['lon'],Grid_Bounds['SE']['lat'],Grid_Bounds['SE']['lon'])
    
    return {'sqmi':sq_mi, 'sqkm':sq_km,'permi': perim_mi, 'perkm':perim_km,'Ndist': n_dist['smi'], 'Sdist': s_dist['smi'], 'Mdist': m_dist['smi']}


# ====================================================================
# Calculates the distance between two lat/lon coordinates
# Input parameters: lat/lon of a start point and end point
# Returns: Structure containing the distance between the two point in kilometers, statue miles and nautical miles
def lat_lon_distance(slat,slon,elat,elon):

    # Check that latitude and longitude values given are within required range
    if not (-90 <= slat <= 90):
        print('latitude must be -90<=lat<90, given %f\n'%slat)
        return False

    if not (-180 <= slon <= 180):
        print('longitude must be -180<=lon<180, given %f\n'%slon)
        return False
    
    if not (-90 <= elat <= 90):
        print('latitude must be -90<=lat<90, given %f\n'%elat)
        return False

    if not (-180 <= elon <= 180):
        print('longitude must be -180<=lon<180, given %f\n'%elon)
        return False

    # Scale multipliers for different units of distance
    kilometers = 6371.0210
    statute_miles = 3958.7613
    nautical_miles = 3437.8675

    # Convert lats and lons to radians
    r_start_lat = math.radians(slat)
    r_start_lon = math.radians(slon)
    r_end_lat = math.radians(elat)
    r_end_lon = math.radians(elon)

    # The formula, "acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))"
    # provides the arc in Radians of the great circle path between two points on the Earth.
    arc_in_radians = math.acos(math.sin(r_start_lat)*math.sin(r_end_lat) + math.cos(r_start_lat)*math.cos(r_end_lat)*math.cos(r_start_lon - r_end_lon))

    # Converter arc_in_radians to kilometers, statute miles and nautical miles
    km = kilometers * arc_in_radians
    smi = statute_miles * arc_in_radians
    nmi = nautical_miles * arc_in_radians

    return {'km':km, 'smi':smi, 'nmi': nmi}


# ====================================================================
# Calculates distance between center points of two grid ID values
# Input parameters: Grid ID of a start point and end point
# Returns: Structure containing the distance between the two point in kilometer, statue miles and nautical miles
def grid_location_distance(gl_id1, gl_id2):

    # Get conter lat/lon coordinate for gl_id1
    coords_1 = grid_location_ID_bounds(gl_id1)
    cen_lat_coord_1 = coords_1['CEN']['lat']
    cen_lon_coord_1 = coords_1['CEN']['lon']

    # Get conter lat/lon coordinate for gl_id2
    coords_2 = grid_location_ID_bounds(gl_id2)
    cen_lat_coord_2 = coords_2['CEN']['lat']
    cen_lon_coord_2 = coords_2['CEN']['lon']

    return lat_lon_distance(cen_lat_coord_1, cen_lon_coord_1, cen_lat_coord_2, cen_lon_coord_2)


# ====================================================================
# Calculate bearing from start location to end location using lat/lon values
# Input parameters: Lat/Lon of a start point and end point
# Returns: Integer value between 0 and 360 degrees of initial bearing angle at start point
def angle_from_coordinates(slat,slon,elat,elon):
    
    # Check that latitude and longitude values given are within required range
    if not (-90 <= slat <= 90):
        print('latitude must be -90<=lat<90, given %f\n'%slat)
        return False

    if not (-180 <= slon <= 180):
        print('longitude must be -180<=lon<180, given %f\n'%slon)
        return False
    
    if not (-90 <= elat <= 90):
        print('latitude must be -90<=lat<90, given %f\n'%elat)
        return False

    if not (-180 <= elon <= 180):
        print('longitude must be -180<=lon<180, given %f\n'%elon)
        return False
        
    # Convert Lat/lon values from degreees to radians
    slat_r = math.radians(slat)
    slon_r = math.radians(slon)
    elat_r = math.radians(elat)
    elon_r = math.radians(elon)

    # Calculate bearing with result in radians
    dlon_r = elon_r - slon_r
    X = math.sin(dlon_r)*math.cos(elat_r)
    Y = math.cos(slat_r)*math.sin(elat_r) - math.sin(slat_r)*math.cos(elat_r)*math.cos(dlon_r)
    bearingRad = math.atan2(X,Y)

    # Covert bearing into degrees and covert from 180/-180 deg format to 360 format 
    start_bearing_deg = round(math.degrees(bearingRad+180*math.pi) % 360)

    return start_bearing_deg


# ====================================================================
# Calculate bearing from start location to end location using either grid ID values
# Input parameters: Grid IDs for the start point and end point 
# Returns: Float value between 0 and 360 degrees of initial bearing angle at start point
def angle_from_grid_location_IDs(gl_id1, gl_id2):
    
    # Get gl_id1 lat/lon center
    coords_1 = grid_location_ID_bounds(gl_id1)
    cen_lat_coord_1 = coords_1['CEN']['lat']
    cen_lon_coord_1 = coords_1['CEN']['lon']
    
    # Get gl_id2 lat/lon center
    coords_2 = grid_location_ID_bounds(gl_id2)
    cen_lat_coord_2 = coords_2['CEN']['lat']
    cen_lon_coord_2 = coords_2['CEN']['lon']
    
    # Get distance between centers of gl_id1 and gl_id2 
    return angle_from_coordinates(cen_lat_coord_1, cen_lon_coord_1, cen_lat_coord_2, cen_lon_coord_2)
