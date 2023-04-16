# This setup is needed to access pymaiden imports while working from the \test directory
import os
import sys
test_path = os.path.dirname(__file__)
pymaiden_path = test_path.removesuffix('\\test')
sys.path.insert(0, pymaiden_path)

import pymaiden 
import pytest

# Location data used:
# Tokyo, Japan, NE : 35.6815740250241, 139.76715986657285, PM95vq23BN
# New York City, USA, NW : 40.75065390774735, -73.99349806969549, FN30as00SD
# Perth, Australia, SE : -31.949433295017, 115.8602175557753, OF78wb32FD
# Santiago, Chile, SW : -33.45302146354265, -70.67975036211871, FF46pn81KG
# ARRL Headquarters, Newington, CT : 41.71484375000001, -72.72829861111111, FN31pr21ON

# -------------------------------------------------------------------
# Grid ID tests
grid_loc_ID_valid_testlist = [("DN",True),("dn",False),("Dn",False),("dN",False), # First pair group must be all capitals
                              ("AR",True),("AS",False),("TR",False),("_7",False), # First pair group with capital letter range between A to R (18 Ranges)
                              ("DN55",True),("DN09",True),("DN0A",False),("DNA9",False),("DNab",False), # Second pair group must numbers 0 through 9
                              ("DN55ic",True),("DN55Ic",False),("DN55iC",False),("DN55IC",False), # Thrid pair group must be all lower case
                              ("DN55ax",True),("DN55ay",False),("DN55az",False), # Thrid pair group with lower case letter between a to x (24 Ranges)
                              ("DN55ax55",True),("DN55ax09",True),("DN55az0A",False), ("DN55azA9",False), ("DN55axAz",False), # Fourth pair group must numbers 0 through 9
                              ("DN55ax55",True),("DN55ax09",True),("DN55az0A",False), ("DN55azA9",False), ("DN55axAz",False)] # Fifth pair group with capital letter range between A to X (24 Ranges)
@pytest.mark.parametrize("gridID, result", grid_loc_ID_valid_testlist)
def test_grid_loc_ID_valid(gridID, result):
    assert result == pymaiden.grid_location_valid_ID(gridID)


# -------------------------------------------------------------------
# Lat/Lat to Grid ID tests
lat_lon_to_grid_loc_testlist = [(35.6815740250241, 139.76715986657285,"PM95vq23BN"), # Tokyo, Japan, NE
                                (40.75065390774735, -73.99349806969549,"FN30as00SD"), # New York City, USA, NW
                                (-31.949433295017, 115.8602175557753,"OF78wb32FD"), # Perth, Australia, SE
                                (-33.45302146354265, -70.67975036211871,"FF46pn81KG"), # Santiago, Chile, SW
                                (0,0,"JJ00aa00AA"), 
                                (0,180,False),
                                (90,0,False),
                                (90, 180,False)]
@pytest.mark.parametrize("lat, lon, result", lat_lon_to_grid_loc_testlist)
def test_lat_lon_to_grid_loc(lat, lon, result):
    assert result == pymaiden.lat_lon_to_grid_ID(lat,lon)


# -------------------------------------------------------------------
# Grid ID location boaurdaries tests
arrl_grid_ID_location_testlist = [("FN",{'NE': {'lat': 50, 'lon': -60}, 'SE': {'lat': 40, 'lon': -60}, 'SW': {'lat': 40, 'lon': -80}, 'NW': {'lat': 50, 'lon': -80}, 'CEN': {'lat': 45, 'lon': -70}}),
                         ("FN31",{'NE': {'lat': 42, 'lon': -72}, 'SE': {'lat': 41, 'lon': -72}, 'SW': {'lat': 41, 'lon': -74}, 'NW': {'lat': 42, 'lon': -74}, 'CEN': {'lat': 41.5, 'lon': -73}}),
                         ("FN31pr",{'NE': {'lat': 41.75, 'lon': -72.66666666666667}, 'SE': {'lat': 41.708333333333336, 'lon': -72.66666666666667}, 'SW': {'lat': 41.708333333333336, 'lon': -72.75}, 'NW': {'lat': 41.75, 'lon': -72.75}, 'CEN': {'lat': 41.72916666666667, 'lon': -72.70833333333333}}),
                         ("FN31pr21",{'NE': {'lat': 41.716666666666676, 'lon': -72.725}, 'SE': {'lat': 41.712500000000006, 'lon': -72.725}, 'SW': {'lat': 41.712500000000006, 'lon': -72.73333333333333}, 'NW': {'lat': 41.716666666666676, 'lon': -72.73333333333333}, 'CEN': {'lat': 41.71458333333334, 'lon': -72.72916666666667}}),
                         ("FN31pr21ON",{'NE': {'lat': 41.71493055555556, 'lon': -72.728125}, 'SE': {'lat': 41.71475694444445, 'lon': -72.728125}, 'SW': {'lat': 41.71475694444445, 'lon': -72.72847222222222}, 'NW': {'lat': 41.71493055555556, 'lon': -72.72847222222222}, 'CEN': {'lat': 41.71484375000001, 'lon': -72.72829861111111}})]
@pytest.mark.parametrize("gl_id, result", arrl_grid_ID_location_testlist)
def test_GridLocIDbounds(gl_id, result):
    assert result == pymaiden.grid_location_ID_bounds(gl_id)


# -------------------------------------------------------------------
# Distance between two Lat/Lon locations tests
lat_lon_distance_testlist  = [(35.6815740250241, 139.76715986657285, 40.75065390774735, -73.99349806969549, {'km': 10843.479991978073, 'smi': 6737.813130668869, 'nmi': 5851.2516991109715}), # Tokyo, Japan, NE to New York City, USA, NW
                              (40.75065390774735, -73.99349806969549, 35.6815740250241, 139.76715986657285, {'km': 10843.479991978073, 'smi': 6737.813130668869, 'nmi': 5851.2516991109715}), # New York City, USA, NW to Tokyo, Japan, NE
                              (40.75065390774735, -73.99349806969549, -31.949433295017, 115.8602175557753, {'km': 18699.162405078125, 'smi': 11619.09848855281, 'nmi': 10090.257544220922}), # New York City, USA, NW to Perth, Australia, SE
                              (-31.949433295017, 115.8602175557753, 40.75065390774735, -73.99349806969549, {'km': 18699.162405078125, 'smi': 11619.09848855281, 'nmi': 10090.257544220922}), # Perth, Australia, SE to New York City, USA, NW
                              (-31.949433295017, 115.8602175557753, -33.45302146354265, -70.67975036211871, {'km': 12710.465107686226, 'smi': 7897.901666516021, 'nmi': 6858.69578888509}), # Perth, Australia, SE to Santiago, Chile, SW
                              (-33.45302146354265, -70.67975036211871, -31.949433295017, 115.8602175557753,  {'km': 12710.465107686226, 'smi': 7897.901666516021, 'nmi': 6858.69578888509}), # Santiago, Chile, SW to Perth, Australia, SE
                              (-33.45302146354265, -70.67975036211871, 35.6815740250241, 139.76715986657285,{'km': 17227.42978017496, 'smi': 10704.607991752679, 'nmi': 9296.09570425143}), # Santiago, Chile, SW to Tokyo, Japan, NE
                              (35.6815740250241, 139.76715986657285, -33.45302146354265, -70.67975036211871, {'km': 17227.42978017496, 'smi': 10704.607991752679, 'nmi': 9296.09570425143}), # Tokyo, Japan, NE to Santiago, Chile, SW
                              (40.75065390774735, -73.99349806969549, -33.45302146354265, -70.67975036211871, {'km': 8258.09561013491, 'smi': 5131.332844939919, 'nmi': 4456.152084567839}), # New York City, USA, NW to Santiago, Chile, SW
                              (-33.45302146354265, -70.67975036211871, 40.75065390774735, -73.99349806969549, {'km': 8258.09561013491, 'smi': 5131.332844939919, 'nmi': 4456.152084567839}), # Santiago, Chile, SW to New York City, USA, NW
                              (35.6815740250241, 139.76715986657285, -31.949433295017, 115.8602175557753, {'km': 7922.675494560599, 'smi': 4922.912848713709, 'nmi': 4275.1559908209865}), # Tokyo, Japan, NE to Santiago, Chile, SW
                              (-31.949433295017, 115.8602175557753, 35.6815740250241, 139.76715986657285, {'km': 7922.675494560599, 'smi': 4922.912848713709, 'nmi': 4275.1559908209865}), # Santiago, Chile, SW to Tokyo, Japan, NE
                              (90.01, 0, 0, 0, False),
                              (-90.01, 0, 0, 0, False),
                              (0, 180.01, 0, 0, False),
                              (0, -180.010, 0, 0, False),
                              (0, 0, 90.01, 0, False),
                              (0, 0, -90.01, 0, False),
                              (0, 0, 0, 180.01, False),
                              (0, 0, 0, -180.01, False)]
@pytest.mark.parametrize("slat1, slon1, elat2, elon2, distance", lat_lon_distance_testlist)
def test_LatLonDistance(slat1, slon1, elat2, elon2, distance):
    assert distance == pymaiden.lat_lon_distance(slat1, slon1, elat2, elon2)


# -------------------------------------------------------------------
# Distance between two Grid locations tests
grid_ID_loc_distance_testlist = [("PM95vq23BN", "FN30as00SD", {'km': 10843.486912467022, 'smi': 6737.817430853067, 'nmi': 5851.255433476945}), # Tokyo, Japan, NE to New York City, USA, NW
                                 ("FN30as00SD", "PM95vq23BN", {'km': 10843.486912467022, 'smi': 6737.817430853067, 'nmi': 5851.255433476945}), # New York City, USA, NW to Tokyo, Japan, NE
                                 ("FN30as00SD", "OF78wb32FD", {'km': 18699.156319526875, 'smi': 11619.094707173846, 'nmi': 10090.254260395792}), # New York City, USA, NW to Perth, Australia, SE
                                 ("OF78wb32FD", "FN30as00SD", {'km': 18699.156319526875, 'smi': 11619.094707173846, 'nmi': 10090.254260395792}), # Perth, Australia, SE to New York City, USA, NW
                                 ("OF78wb32FD", "FF46pn81KG", {'km': 12710.468152199568, 'smi': 7897.9035582852675, 'nmi': 6858.697431735344}), # Perth, Australia, SE to Santiago, Chile, SW
                                 ("FF46pn81KG", "OF78wb32FD", {'km': 12710.468152199568, 'smi': 7897.9035582852675, 'nmi': 6858.697431735344}), # Santiago, Chile, SW to Perth, Australia, SE
                                 ("FF46pn81KG", "PM95vq23BN", {'km': 17227.4329256914, 'smi': 10704.609946282219, 'nmi': 9296.097401603976}), # Santiago, Chile, SW to Tokyo, Japan, NE
                                 ("PM95vq23BN", "FF46pn81KG", {'km': 17227.4329256914, 'smi': 10704.609946282219, 'nmi': 9296.097401603976}), # # Tokyo, Japan, NE to Santiago, Chile, SW
                                 ("FN30as00SD", "FF46pn81KG", {'km': 8258.092926083775, 'smi': 5131.331177151074, 'nmi': 4456.150636226645}), # New York City, USA, NW to Santiago, Chile, SW
                                 ("FF46pn81KG", "FN30as00SD", {'km': 8258.092926083775, 'smi': 5131.331177151074, 'nmi': 4456.150636226645}), # Santiago, Chile, SW to New York City, USA, NW
                                 ("PM95vq23BN", "FF46pn81KG", {'km': 17227.4329256914, 'smi': 10704.609946282219, 'nmi': 9296.097401603976}), # Tokyo, Japan, NE to Santiago, Chile, SW
                                 ("FF46pn81KG", "PM95vq23BN", {'km': 17227.4329256914, 'smi': 10704.609946282219, 'nmi': 9296.097401603976})] # Santiago, Chile, SW to Tokyo, Japan, NE                                                     
@pytest.mark.parametrize("gl_id1, gl_id2, distance", grid_ID_loc_distance_testlist)
def test_GridLocDistance(gl_id1, gl_id2, distance):
    assert distance == pymaiden.grid_location_distance(gl_id1, gl_id2)


# -------------------------------------------------------------------
# Initial angle at start Lat/Lon heading towards end Lat/lon tests
angle_from_lat_lon_coordinates_testlist = [(35.6815740250241, 139.76715986657285, 40.75065390774735, -73.99349806969549, 25), # Tokyo, Japan, NE to New York City, USA, NW
                                           (40.75065390774735, -73.99349806969549, 35.6815740250241, 139.76715986657285, 333), # New York City, USA, NW to Tokyo, Japan, NE
                                           (40.75065390774735, -73.99349806969549, -31.949433295017, 115.8602175557753, 315), # New York City, USA, NW to Perth, Australia, SE
                                           (-31.949433295017, 115.8602175557753, 40.75065390774735, -73.99349806969549, 39), # Perth, Australia, SE to New York City, USA, NW
                                           (-31.949433295017, 115.8602175557753, -33.45302146354265, -70.67975036211871, 174), # Perth, Australia, SE to Santiago, Chile, SW
                                           (-33.45302146354265, -70.67975036211871, -31.949433295017, 115.8602175557753,  186), # Santiago, Chile, SW to Perth, Australia, SE
                                           (-33.45302146354265, -70.67975036211871, 35.6815740250241, 139.76715986657285, 284), # Santiago, Chile, SW to Tokyo, Japan, NE
                                           (35.6815740250241, 139.76715986657285, -33.45302146354265, -70.67975036211871, 94), # Tokyo, Japan, NE to Santiago, Chile, SW
                                           (40.75065390774735, -73.99349806969549, -33.45302146354265, -70.67975036211871, 177), # New York City, USA, NW to Santiago, Chile, SW
                                           (-33.45302146354265, -70.67975036211871, 40.75065390774735, -73.99349806969549, 357), # Santiago, Chile, SW to New York City, USA, NW
                                           (35.6815740250241, 139.76715986657285, -33.45302146354265, -70.67975036211871, 94), # Tokyo, Japan, NE to Santiago, Chile, SW
                                           (-33.45302146354265, -70.67975036211871, 35.6815740250241, 139.76715986657285, 284), # Santiago, Chile, SW to Tokyo, Japan, NE                               
                                           (90.01, 0, 0, 0, False),
                                           (-90.01, 0, 0, 0, False),
                                           (0, 180.01, 0, 0, False),
                                           (0, -180.010, 0, 0, False),
                                           (0, 0, 90.01, 0, False),
                                           (0, 0, -90.01, 0, False),
                                           (0, 0, 0, 180.01, False),
                                           (0, 0, 0, -180.01, False)]
@pytest.mark.parametrize("slat1, slon1, elat2, elon2, angle", angle_from_lat_lon_coordinates_testlist)
def test_AngleFromCoordinates(slat1, slon1, elat2, elon2, angle):
    assert angle == pymaiden.angle_from_coordinates(slat1, slon1, elat2, elon2)


# -------------------------------------------------------------------
# Initial angle at start grid ID heading towards end grid ID tests
AngleFromGridLocIDs_testlist = [("PM95vq23BN", "FN30as00SD", 25), # Tokyo, Japan, NE to New York City, USA, NW
                                ("FN30as00SD", "PM95vq23BN", 333), # New York City, USA, NW to Tokyo, Japan, NE
                                ("FN30as00SD", "OF78wb32FD", 315), # New York City, USA, NW to Perth, Australia, SE
                                ("OF78wb32FD", "FN30as00SD", 39), # Perth, Australia, SE to New York City, USA, NW
                                ("OF78wb32FD", "FF46pn81KG", 174), # Perth, Australia, SE to Santiago, Chile, SW
                                ("FF46pn81KG", "OF78wb32FD", 186), # Santiago, Chile, SW to Perth, Australia, SE
                                ("FF46pn81KG", "PM95vq23BN", 284), # Santiago, Chile, SW to Tokyo, Japan, NE
                                ("PM95vq23BN", "FF46pn81KG", 94), # Tokyo, Japan, NE to Santiago, Chile, SW
                                ("FN30as00SD", "FF46pn81KG", 177), # New York City, USA, NW to Santiago, Chile, SW
                                ("FF46pn81KG", "FN30as00SD", 357), # Santiago, Chile, SW to New York City, USA, NW
                                ("PM95vq23BN", "FF46pn81KG", 94), # Tokyo, Japan, NE to Santiago, Chile, SW
                                ("FF46pn81KG", "PM95vq23BN", 284)] # Santiago, Chile, SW to Tokyo, Japan, NE
@pytest.mark.parametrize("gl_id1, gl_id2, angle", AngleFromGridLocIDs_testlist)
def test_AngleFromGridLocIDs(gl_id1, gl_id2, angle):
    assert angle == pymaiden.angle_from_grid_location_IDs(gl_id1, gl_id2)


# -------------------------------------------------------------------
# Size of Grid location tests
test_GridLocSize_testlist = [("FN31pr21ON", {'sqmi': 0.0002151300054755712, 'sqkm': 0.000557184156358242, 'permi': 0.059873213635150815, 'perkm': 0.09635659747139358, 'Ndist': 0.017908147460374557, 'Sdist': 0.017908341775156496, 'Mdist': 0.01199546770188496}),
                             ("FN31pr21", {'sqmi': 0.12391537762031467, 'sqkm': 0.32093935472440716, 'permi': 1.4369605790381637, 'perkm': 2.3125638944383047, 'Ndist': 0.42978677066814014, 'Sdist': 0.4298146303666335, 'Mdist': 0.28788924257938864}),
                             ("FN31pr", {'sqmi': 12.388766907947984, 'sqkm': 32.08675899330902, 'permi': 14.367671126038843, 'perkm': 23.122525403919745, 'Ndist': 4.295637732346551, 'Sdist': 4.298424762144943, 'Mdist': 2.878892457169789}),
                             ("FN31", {'sqmi': 7160.625162612897, 'sqkm': 18545.934033739988, 'permi': 345.53931537967895, 'perkm': 556.0916259726798, 'Ndist': 102.69049909910854, 'Sdist': 104.28865137864236, 'Mdist': 69.09341898552411}),
                             ("FN", {'sqmi': 672314.1612674901, 'sqkm': 1741285.6840933007, 'permi': 3328.3948504767563, 'perkm': 5356.532301532609, 'Ndist': 885.5905692280469, 'Sdist': 1056.3375076762015, 'Mdist': 690.9341898553108})]
@pytest.mark.parametrize("gl_id, size", test_GridLocSize_testlist)
def test_GridLocSize(gl_id, size):
    assert size == pymaiden.grid_location_size(gl_id)
