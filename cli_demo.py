'''
This file imports the pymaiden module (pymaiden.py file) and sets up a
series of eight demonstration function calls showing the usage of each of
the eight functions provided by the pymaiden module. Each function is
called at the bottom of this file.

Written by: Kevin Hallquist, WB7BGJ
'''


# *********************************************************
# Module import
import pymaiden


# *********************************************************
def run_grid_location_valid_ID():

    gl_id = 'FN31pr21OM' # Valid grid ID for W1AW, ARRL HQ, Newington, CT
    
    print('---------------------------------------------------------')
    print('RUN: grid_location_valid_ID(' + str(gl_id) +')')

    ret = pymaiden.grid_location_valid_ID(gl_id)

    print()
    print(gl_id + ' valid: ' + str(ret))
    print()


# *********************************************************
def run_lat_lon_to_grid_ID():

    # W1AW, American Radio Relay League HQ
    lat = 41.7147450
    lon = -72.728192

    print('---------------------------------------------------------')
    print('RUN: lat_lon_to_grid_ID(' + str(lat) + ',' + str(lon) + ')')

    ret = pymaiden.lat_lon_to_grid_ID(lat, lon)

    print()
    print('Maidenhead Grid Square: ' + ret)
    print()


# *********************************************************
def run_grid_location_ID_bounds():

    gl_id = 'FN31pr21OM' # W1AW ARRL HQ, Newington, CT
        
    ret = pymaiden.grid_location_ID_bounds(gl_id)

    print('---------------------------------------------------------')
    print('RUN: grid_location_ID_bounds(' + gl_id + ')')
    print()

    print('               Lat         Lon')
    print('SW Corner : ', end = "")
    print('{:.6f}'.format(ret['SW']['lat']), end=', ')
    print('{:.6f}'.format(ret['SW']['lon']))

    print('NW Corner : ', end = "")
    print('{:.6f}'.format(ret['NW']['lat']), end=', ')
    print('{:.6f}'.format(ret['NW']['lon']))

    print('NE Corner : ', end = "")
    print('{:.6f}'.format(ret['NE']['lat']), end=', ')
    print('{:.6f}'.format(ret['NE']['lon']))

    print('SE Corner : ', end = "")
    print('{:.6f}'.format(ret['SE']['lat']), end=', ')
    print('{:.6f}'.format(ret['SE']['lon']))

    print('Center    : ', end = "")
    print('{:.6f}'.format(ret['CEN']['lat']), end=', ')
    print('{:.6f}'.format(ret['CEN']['lon']))
    print()


# *********************************************************
def run_lat_lon_distance():

    # Nairobi, Kenya - City center from Wikipedia
    lat1 = -1.286389
    lon1 = 36.817222

    # Seattle, WA  - City center from Wikipedia
    lat2 = 47.609722
    lon2 = -122.333056

    print('---------------------------------------------------------')
    print('RUN: lat_lon_distance(' + str(lat1) + ',' + str(lon1) + ',' + str(lat2) + ',' + str(lon2) +')')

    ret = pymaiden.lat_lon_distance(lat1,lon1,lat2,lon2)
    
    print()
    print('Kilometers     : ' + '{:.6f}'.format(ret['km']))
    print('Statute Miles  : ' + '{:.6f}'.format(ret['smi']))
    print('Nautical Miles : ' + '{:.6f}'.format(ret['nmi']))
    print()


# *********************************************************
def run_grid_location_distance():

    # Nairobi, Kenya - City center from Wikipedia
    gl_id1 = 'KI88jr'

    # Seattle, WA  - City center from Wikipedia
    gl_id2 = 'CN87uo'

    # Check that the grid IDs are valid before call GridLocDistance
    parm_1 = pymaiden.grid_location_valid_ID(gl_id1)
    parm_2 = pymaiden.grid_location_valid_ID(gl_id2)
    
    if parm_1 == True and parm_2 == True:
        ret = pymaiden.grid_location_distance(gl_id1, gl_id2)
        print('---------------------------------------------------------')
        print('RUN: grid_location_distance(' + gl_id1 + ',' + gl_id2 + ')')
        print()
        print('Kilometers     : ' + '{:.6f}'.format(ret['km']))
        print('Statute Miles  : ' + '{:.6f}'.format(ret['smi']))
        print('Nautical Miles : ' + '{:.6f}'.format(ret['nmi']))
        print()
    else:
        print("Invalid ID")


# *********************************************************
def run_angle_from_coordinates():

    # Nairobi, Kenya - City center from Wikipedia
    lat1 = -1.286389
    lon1 = 36.817222

    # Seattle, WA  - City center from Wikipedia
    lat2 = 47.609722
    lon2 = -122.333056

    print('---------------------------------------------------------')
    print('RUN: angle_from_coordinates(' + str(lat1) + ',' + str(lon1) + ',' + str(lat2) + ',' + str(lon2) +')')

    ret = pymaiden.angle_from_coordinates(lat1,lon1,lat2,lon2)

    print()
    print('Start bearing ' + str(ret))
    print()


# *********************************************************
def run_angle_from_grid_location_IDs():

    # Nairobi, Kenya - City center from Wikipedia 
    gl_id1 = 'KI88jr'

    # Seattle, WA  - City center from Wikipedia
    gl_id2 = 'CN87uo'
    
    ret = pymaiden.angle_from_grid_location_IDs(gl_id1, gl_id2)

    print('---------------------------------------------------------')
    print('RUN: angle_from_grid_location_IDs(' + gl_id1 + ',' + gl_id2 + ')')

    print()
    print('Start bearing ' + str(ret))
    print()


# *********************************************************
def run_grid_size():
    
    gl_id = 'FN31pr' # Valid grid ID for W1AW, ARRL HQ, Newington, CT

    print('---------------------------------------------------------')
    print('RUN: grid_location_size(' + gl_id + ')')
    
    ret = pymaiden.grid_location_size(gl_id)
    
    print()
    print('Area:')
    print('  Square Miles      : ' + '{:.6f}'.format(ret['sqmi']))
    print('  Square Kilometers : ' + '{:.6f}'.format(ret['sqkm']))
    print()
    print('Perimeter')
    print('  Miles             : ' + '{:.6f}'.format(ret['permi']))
    print('  Kilometers        : ' + '{:.6f}'.format(ret['perkm']))
    print()
    print('Side Lengths (miles)')
    print('  North             : ' + '{:.6f}'.format(ret['Ndist']))
    print('  South             : ' + '{:.6f}'.format(ret['Sdist']))
    print('  East/West         : ' + '{:.6f}'.format(ret['Mdist']))
    print()


# *********************************************************
if __name__ == '__main__':
    
    print()
    run_grid_location_valid_ID()
    run_lat_lon_to_grid_ID()
    run_grid_location_ID_bounds()
    run_lat_lon_distance()
    run_grid_location_distance()
    run_angle_from_coordinates()
    run_angle_from_grid_location_IDs()
    run_grid_size()
