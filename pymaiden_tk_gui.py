'''
Maidenhead Grid Utility GUI

This GUI utility provides the ability to calculate... 
    1. A 10 digit maidenhead grid identifier calculated from a given Lat/Lon.
    2. The distance and initial bearing between two given lat/lon positions.
    3. The distance and initial bearing between two given grid square ID centers.
    4. The area, perimeter and side lengths of a given grid square ID.
    5. The lat/lat of the four corners and center of a given grid square ID.  
'''


# =========================================================
# Modules required for this utility GUI
import tkinter as tk
from tkinter import ttk
import pymaiden


# =========================================================
# Calculate the 10 digit Maidenhead grid square from a given
# latitude and longitude position. Also provides input validation
# and warnings for invalid inputs. 
def calc_grid_id(*args):
    
    # Retrieve lat and lon string values from input fields
    lat = f1_latitude_entry.get()
    lon = f1_longitude_entry.get()

    # Variables used to flag the validity of the lat and lon values provided. 
    lat_valid = True
    lon_valid = True 

    # Test if the lat string provided is an actual floating point value.
    try:
        f_lat = float(lat)
    except Exception as e:
        f1_latitude_entry.configure({"background": 'red'})
        f1_grid_id_value.set("------------------")
        lat_valid = False   

    # Test if the lon string provided is an actual floating point value.
    try:
        f_lon = float(lon)
    except Exception as e:
        f1_longitude_entry.configure({"background": 'red'})
        f1_grid_id_value.set("------------------")
        lon_valid = False
    
    # When either entry is valid, ensure that its background is set to white
    if (lat_valid):
        f1_latitude_entry.configure({"background": 'white'})
    if (lon_valid):
        f1_longitude_entry.configure({"background": 'white'})
    
    # Set display value with calculated grid square ID string value
    if (lat_valid and lon_valid):
        grid_id = pymaiden.lat_lon_to_grid_ID(f_lat,f_lon)
        f1_grid_id_value.set(grid_id)


# =========================================================
# Calculate the distance between two lat/lon positions and
# the bearing from lat/lon #1 to lat/lon #2. Also provides
# input validation and warnings for invalid inputs.
def calc_dist_brg_lat_lon(*args):
    
    # Retrieve Start and End lat/lon string values from input fields
    lat1 = f2_start_latitude_entry.get()
    lon1 = f2_start_longitude_entry.get()
    lat2 = f2_end_latitude_entry.get()
    lon2 = f2_end_longitude_entry.get()

    # Variables used to flag the validity of the lat and lon values provided.
    lat1_valid = True
    lon1_valid = True
    lat2_valid = True
    lon2_valid = True

    # Test if the Start lat string provided is an actual floating point value.
    try:
        f_lat1 = float(lat1)
        f2_start_latitude_entry.configure({"background": 'white'})
    except Exception as e:
        lat1_valid = False
        f2_start_latitude_entry.configure({"background": 'red'})
    
    # Test if the Start lon string provided is an actual floating point value.
    try:
        f_lon1 = float(lon1)
        f2_start_longitude_entry.configure({"background": 'white'})
    except Exception as e:
        lon1_valid = False
        f2_start_longitude_entry.configure({"background": 'red'})
        
    # Test if the End lat string provided is an actual floating point value.
    try:
        f_lat2 = float(lat2)
        f2_end_latitude_entry.configure({"background": 'white'})
    except Exception as e:
        lat2_valid = False
        f2_end_latitude_entry.configure({"background": 'red'})
    
    # Test if the End lon string provided is an actual floating point value.
    try:
        f_lon2 = float(lon2)
        f2_end_longitude_entry.configure({"background": 'white'})
    except Exception as e:
        lon2_valid = False
        f2_end_longitude_entry.configure({"background": 'red'})   

    # When all user provided input values are valid, calculate the distance and bearing data
    # and the set display values with retrieved data. If any one of the inputs is invalid,
    # then reset all value fields.   
    if (lat1_valid == True and lon1_valid == True and lat2_valid == True and lon2_valid == True):
        distance = pymaiden.lat_lon_distance(f_lat1,f_lon1,f_lat2,f_lon2)
        azimuth = pymaiden.angle_from_coordinates(f_lat1,f_lon1,f_lat2,f_lon2)
        f2_distance_value_miles.set(int(distance['smi']))
        f2_distance_value_kilometers.set(int(distance['km']))
        f2_azimuth_value_degrees.set(azimuth)
    else:
        f2_distance_value_miles.set("---------")
        f2_distance_value_kilometers.set("---------")
        f2_azimuth_value_degrees.set("-----")    


# =========================================================
# Calculate the distance between the centers of two grid locators
# and the bearing from grid ID #1 to grid ID #2. Also provides
# input validation and warnings for invalid inputs.
def calc_dist_brg_grid_id(*args):
    
    # Retrieve Start and End grid ID string values from input fields
    grid_id_start = f3_start_grid_id_value.get()
    grid_id_end = f3_end_grid_id_value.get()
    
    # Test Start and End input strings for validity 
    start_id_test = pymaiden.grid_location_valid_ID(grid_id_start)
    end_id_test = pymaiden.grid_location_valid_ID(grid_id_end)

    # When both user provided Start and End input values are valid,
    # calculate the distance and bearing data and the set display values
    # with retrieved data. If either of the inputs is invalid, then
    # reset all value fields.
    if (start_id_test == True and end_id_test == True):
        distance = pymaiden.grid_location_distance(grid_id_start,grid_id_end)
        azimuth = pymaiden.angle_from_grid_location_IDs(grid_id_start,grid_id_end)
        f3_distance_value_miles.set(int(distance['smi']))
        f3_distance_value_kilometers.set(int(distance['km']))
        f3_azimuth_value_degrees.set(azimuth)
    else:
        f3_distance_value_miles.set("---------")
        f3_distance_value_kilometers.set("---------")
        f3_azimuth_value_degrees.set("-----")

    # Set background color of Start entry field based on its validity
    if (start_id_test == False):
        f3_start_grid_id_entry.configure({"background": 'red'})
    else:
        f3_start_grid_id_entry.configure({"background": 'white'})

    # Set background color of End entry field based on its validity
    if (end_id_test == False):
        f3_end_grid_id_entry.configure({"background": 'red'})
    else:
        f3_end_grid_id_entry.configure({"background": 'white'})


# =========================================================
# Calculate the area, perimeter and side lengths of a given
# grid locator.
def calc_grid_size(*args):
    
    # Retrieve grid ID string value from input field
    grid_id = f4_grid_id_value.get()

    # Test grid id input strings for validity
    id_test = pymaiden.grid_location_valid_ID(grid_id)

    if (id_test == True):
        # Alway reset background color to white on True return
        f4_grid_id_entry.configure({"background": 'white'})
        
        # Retrieve grid square size information
        grid_loc_size = pymaiden.grid_location_size(grid_id)

        # Set displayed values with data contained in grid_loc_size  
        f4_area_value_sq_miles.set(str(grid_loc_size['sqmi'])[0:10])
        f4_area_value_sq_kilometers.set(str(grid_loc_size['sqkm'])[0:10])
        f4_perimeter_value_miles.set(str(grid_loc_size['permi'])[0:10])
        f4_perimeter_value_kilometers.set(str(grid_loc_size['perkm'])[0:10])
        f4_north_value_miles.set(str(grid_loc_size['Ndist'])[0:10])
        f4_north_value_kilometers.set(str(grid_loc_size['Ndist']*1.609344)[0:10])
        f4_south_value_miles.set(str(grid_loc_size['Sdist'])[0:10])
        f4_south_value_kilometers.set(str(grid_loc_size['Sdist']*1.609344)[0:10])
        f4_east_value_miles.set(str(grid_loc_size['Mdist'])[0:10])
        f4_east_value_kilometers.set(str(grid_loc_size['Mdist']*1.609344)[0:10])
        f4_west_value_miles.set(str(grid_loc_size['Mdist'])[0:10])
        f4_west_value_kilometers.set(str(grid_loc_size['Mdist']*1.609344)[0:10])
    else:
        # Grid ID test failed. Reset all value fields.
        f4_grid_id_entry.configure({"background": 'red'})
        f4_area_value_sq_miles.set("--------------------")
        f4_area_value_sq_kilometers.set("--------------------")
        f4_perimeter_value_miles.set("--------------------")
        f4_perimeter_value_kilometers.set("--------------------")
        f4_north_value_miles.set("--------------------")
        f4_north_value_kilometers.set("--------------------")
        f4_south_value_miles.set("--------------------")
        f4_south_value_kilometers.set("--------------------")
        f4_east_value_miles.set("--------------------")
        f4_east_value_kilometers.set("--------------------")
        f4_west_value_miles.set("--------------------")
        f4_west_value_kilometers.set("--------------------")


# =========================================================
# Calculate the lat/lat for the four corners and center of
# a given grid locator.        
def calc_grid_boundary(*args):
    
    # Retrieve grid ID string value from input field
    grid_id = f5_grid_id_value.get()
    
    # Test grid id input strings for validity
    id_test = pymaiden.grid_location_valid_ID(grid_id)

    if (id_test == True):
        # Alway reset background color to white on True grid ID test return.
        f5_grid_id_entry.configure({"background": 'white'})

        # Retrieve grid square boundary lat/lon coordinates
        grid_loc_bounds = pymaiden.grid_location_ID_bounds(grid_id)
        
        # Set displayed values with data contained in grid_loc_bounds 
        f5_NE_lat_value.set(str(float(grid_loc_bounds['NE']['lat'])).ljust(10,'0')[0:10])
        f5_NE_lon_value.set(str(float(grid_loc_bounds['NE']['lon'])).ljust(10,'0')[0:10])
        f5_SE_lat_value.set(str(float(grid_loc_bounds['SE']['lat'])).ljust(10,'0')[0:10])
        f5_SE_lon_value.set(str(float(grid_loc_bounds['SE']['lon'])).ljust(10,'0')[0:10])
        f5_SW_lat_value.set(str(float(grid_loc_bounds['SW']['lat'])).ljust(10,'0')[0:10])
        f5_SW_lon_value.set(str(float(grid_loc_bounds['SW']['lon'])).ljust(10,'0')[0:10])
        f5_NW_lat_value.set(str(float(grid_loc_bounds['NW']['lat'])).ljust(10,'0')[0:10])
        f5_NW_lon_value.set(str(float(grid_loc_bounds['NW']['lon'])).ljust(10,'0')[0:10])
        f5_grid_center_lat_value.set(str(float(grid_loc_bounds['CEN']['lat'])).ljust(10,'0')[0:10])
        f5_grid_center_lon_value.set(str(float(grid_loc_bounds['CEN']['lon'])).ljust(10,'0')[0:10])
    else:
        # Grid ID test failed. Reset all value fields.
        f5_grid_id_entry.configure({"background": 'red'})
        f5_NE_lat_value.set('-----------------')
        f5_NE_lon_value.set('-----------------')
        f5_SE_lat_value.set('-----------------')
        f5_SE_lon_value.set('-----------------')
        f5_SW_lat_value.set('-----------------')
        f5_SW_lon_value.set('-----------------')
        f5_NW_lat_value.set('-----------------')
        f5_NW_lon_value.set('-----------------')
        f5_grid_center_lat_value.set("-----------------")
        f5_grid_center_lon_value.set("-----------------")


# =========================================================
# Create a Tk root window widget
# Set window to a static size and provide application name  
root = tk.Tk()
root.geometry('650x300')
root.title("Maidenhead Grid Locator Utility")


# =========================================================
# Create a large font application name Label to be shown
# above notebook Frames/Tabs
mylabel = ttk.Label(root, text='Maidenhead Grid Locator Utility', font=('Arial', 22), background="#f0f0f0", foreground='black', padding=0)
mylabel.pack()


# =========================================================
# Style notebook tabs background colors
style = ttk.Style(root)
style.theme_use('default')
style.configure('TNotebook.Tab', background="#A0A0A0" )
style.map("TNotebook.Tab", background = [("selected", "#D9D9D9")])


# =========================================================
# Create a notebook to hold a series of frame with tabs.
notebook = ttk.Notebook(root, style='lefttab.TNotebook')
notebook.pack(expand=True)


# ***********************************
# Create Frame #1 - Grid ID from Lat/Lon
frame1 = ttk.Frame(notebook, height=245)
frame1.pack(fill='both', expand=True)
notebook.add(frame1, text='Grid ID from Lat/Lon')

# Latitude text label
f1_latitude_text = tk.Label(frame1, text="Latitute", bg="#D9D9D9", font=("Arial 12"))
f1_latitude_text.pack()
f1_latitude_text.place(x=36,y=20)

# Latitude entry field
f1_latitude_value = tk.StringVar()
f1_latitude_entry = tk.Entry(frame1, width=20, textvariable=f1_latitude_value, font=("Arial 10"))
f1_latitude_entry.pack()
f1_latitude_entry.place(x=40,y=45)

# Longitude text label
f1_longitude_text = tk.Label(frame1, text="Longitude", bg="#D9D9D9", font=("Arial 12"))
f1_longitude_text.pack()
f1_longitude_text.place(x=36,y=70)

# Longitude entry field
f1_longitude_value = tk.StringVar()
f1_longitude_entry = tk.Entry(frame1, width=20, textvariable=f1_longitude_value, font=("Arial 10"))
f1_longitude_entry.pack()
f1_longitude_entry.place(x=40,y=95)

# "Find Grid ID" button to activate calulation by calling function calc_grid_id
f1_cmd_button1 = tk.Button(frame1, text="    Find Grid ID    ", command=calc_grid_id)
f1_cmd_button1.pack()
f1_cmd_button1.place(x=40,y=140)

# Grid ID text label
f1_latitude_text = tk.Label(frame1, text="Grid ID", bg="#D9D9D9", font=("Arial 12"))
f1_latitude_text.pack()
f1_latitude_text.place(x=260,y=60)

# Grid ID Label field
f1_grid_id_value = tk.StringVar()
f1_grid_id_value.set("------------------")
f1_grid_id_label = tk.Label(frame1, textvariable=f1_grid_id_value, fg="#0603ff", bg="#D9D9D9", font=("Arial", 32))
f1_grid_id_label.pack()
f1_grid_id_label.place(x=260,y=80)


# ***********************************
# Create Frame #2 - Distance and Azimuth (Lat/Lon)
frame2 = ttk.Frame(notebook, height=245)
frame2.pack(fill='both', expand=True)
notebook.add(frame2, text='Distance and Azimuth (Lat/Lon)')

# Start Latitude label
f2_start_latitude_text = tk.Label(frame2, text="Latitute (Start)", bg="#D9D9D9", font=("Arial 12"))
f2_start_latitude_text.pack()
f2_start_latitude_text.place(x=36,y=20)

# Start Latitude Entry
f2_start_latitude_value = tk.StringVar()
f2_start_latitude_entry = tk.Entry(frame2, width=20, textvariable=f2_start_latitude_value, font=("Arial 10"))
f2_start_latitude_entry.pack()
f2_start_latitude_entry.place(x=40,y=45)

# Start Longitude label
f2_start_longitude_text = tk.Label(frame2, text="Longitude (Start)", bg="#D9D9D9", font=("Arial 12"))
f2_start_longitude_text.pack()
f2_start_longitude_text.place(x=225,y=20)

# Start Longitude Entry
f2_start_longitude_value = tk.StringVar()
f2_start_longitude_entry = tk.Entry(frame2, width=20, textvariable=f2_start_longitude_value, font=("Arial 10"))
f2_start_longitude_entry.pack()
f2_start_longitude_entry.place(x=225,y=45)

# End Latitude label
f2_end_latitude_text = tk.Label(frame2, text="Latitute (End)", bg="#D9D9D9", font=("Arial 12"))
f2_end_latitude_text.pack()
f2_end_latitude_text.place(x=36,y=70)

# End Latitude Entry
f2_end_latitude_value = tk.StringVar()
f2_end_latitude_entry = tk.Entry(frame2, width=20, textvariable=f2_end_latitude_value, font=("Arial 10"))
f2_end_latitude_entry.pack()
f2_end_latitude_entry.place(x=40,y=95)

# End Longitude label
f2_end_longitude_text = tk.Label(frame2, text="Longitude (End)", bg="#D9D9D9", font=("Arial 12"))
f2_end_longitude_text.pack()
f2_end_longitude_text.place(x=225,y=70)

# End Longitude Entry
f2_end_longitude_value = tk.StringVar()
f2_end_longitude_entry = tk.Entry(frame2, width=20, textvariable=f2_end_longitude_value, font=("Arial 10"))
f2_end_longitude_entry.pack()
f2_end_longitude_entry.place(x=225,y=95)

# "Calculate" button to activate calulation
f2_cmd_button1 = tk.Button(frame2, text="     Calculate     ", command=calc_dist_brg_lat_lon)
f2_cmd_button1.pack()
f2_cmd_button1.place(x=40,y=140)

# Distance label
f2_distance_latitude_text = tk.Label(frame2, text="Distance:", bg="#D9D9D9", font=("Arial 12"))
f2_distance_latitude_text.pack()
f2_distance_latitude_text.place(x=225,y=135)

# Distance in miles to be displayed
f2_distance_value_miles = tk.StringVar()
f2_distance_value_miles.set("---------")
f2_distance_label_miles = tk.Label(frame2, textvariable=f2_distance_value_miles, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12), width=5, anchor='e')
f2_distance_label_miles.pack()
f2_distance_label_miles.place(x=295,y=135)

# Miles distance unit label 
f2_miles_text = tk.Label(frame2, text="mi", bg="#D9D9D9", font=("Arial 12"))
f2_miles_text.pack()
f2_miles_text.place(x=345,y=135)

# Distance in kilometers to be displayed
f2_distance_value_kilometers = tk.StringVar()
f2_distance_value_kilometers.set("---------")
f2_distance_label_kilometers = tk.Label(frame2, textvariable=f2_distance_value_kilometers, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=5, anchor='e')
f2_distance_label_kilometers.pack()
f2_distance_label_kilometers.place(x=295,y=155)

# Kilometers distance unit label
f2_kilometers_text = tk.Label(frame2, text="km", bg="#D9D9D9", font=("Arial 12"))
f2_kilometers_text.pack()
f2_kilometers_text.place(x=345,y=155)

# Azimuth label
f2_azimuth_text = tk.Label(frame2, text="Azimuth:", bg="#D9D9D9", font=("Arial 12"))
f2_azimuth_text.pack()
f2_azimuth_text.place(x=410,y=135)

# Amimuth at start lat/lon to end lat/lon
f2_azimuth_value_degrees = tk.StringVar()
f2_azimuth_value_degrees.set("-----")
f2_azimuth_bearing_degrees = tk.Label(frame2, textvariable=f2_azimuth_value_degrees, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=3, anchor='e')
f2_azimuth_bearing_degrees.pack()
f2_azimuth_bearing_degrees.place(x=480,y=135)

# Degrees distance unit label
f2_degress_text = tk.Label(frame2, text="deg", bg="#D9D9D9", font=("Arial 12"))
f2_degress_text.pack()
f2_degress_text.place(x=512,y=135)


# ***********************************
# Create Frame #3 - Distance and Azimuth (Grid ID)
frame3 = ttk.Frame(notebook, height=245)
frame3.pack(fill='both', expand=True)
notebook.add(frame3, text='Distance and Azimuth (Grid ID)')

# Grid ID (Start) Label
f3_start_grid_id_text = tk.Label(frame3, text="Grid ID (Start)", bg="#D9D9D9", font=("Arial 12"))
f3_start_grid_id_text.pack()
f3_start_grid_id_text.place(x=36,y=40)

# Grid ID (Start) Entry
f3_start_grid_id_value = tk.StringVar()
f3_start_grid_id_entry = tk.Entry(frame3, width=13, textvariable=f3_start_grid_id_value, font=("Arial 10"))
f3_start_grid_id_entry.pack()
f3_start_grid_id_entry.place(x=40,y=65)

# Grid ID End Label
f3_end_grid_id_text = tk.Label(frame3, text="Grid ID (End)", bg="#D9D9D9", font=("Arial 12"))
f3_end_grid_id_text.pack()
f3_end_grid_id_text.place(x=225,y=40)

# End Longitude Entry
f3_end_grid_id_value = tk.StringVar()
f3_end_grid_id_entry = tk.Entry(frame3, width=13, textvariable=f3_end_grid_id_value, font=("Arial 10"))
f3_end_grid_id_entry.pack()
f3_end_grid_id_entry.place(x=225,y=65)

# "Calculate" button to activate calulation
f3_cmd_button1 = tk.Button(frame3, text="     Calculate     ", command=calc_dist_brg_grid_id)
f3_cmd_button1.pack()
f3_cmd_button1.place(x=40,y=105)

# Distance label
f3_distance_latitude_text = tk.Label(frame3, text="Distance:", bg="#D9D9D9", font=("Arial 12"))
f3_distance_latitude_text.pack()
f3_distance_latitude_text.place(x=225,y=100)

# Distance in miles to be displayed
f3_distance_value_miles = tk.StringVar()
f3_distance_value_miles.set("---------")
f3_distance_label_miles = tk.Label(frame3, textvariable=f3_distance_value_miles, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12), width=5, anchor='e')
f3_distance_label_miles.pack()
f3_distance_label_miles.place(x=295,y=100)

# Miles distance unit label 
f3_miles_text = tk.Label(frame3, text="mi", bg="#D9D9D9", font=("Arial 12"))
f3_miles_text.pack()
f3_miles_text.place(x=345,y=100)

# Distance in kilometers to be displayed
f3_distance_value_kilometers = tk.StringVar()
f3_distance_value_kilometers.set("---------")
f3_distance_label_kilometers = tk.Label(frame3, textvariable=f3_distance_value_kilometers, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=5, anchor='e')
f3_distance_label_kilometers.pack()
f3_distance_label_kilometers.place(x=295,y=120)

# Kilometers distance unit label
f3_kilometers_text = tk.Label(frame3, text="km", bg="#D9D9D9", font=("Arial 12"))
f3_kilometers_text.pack()
f3_kilometers_text.place(x=345,y=120)

# Azimuth label
f3_azimuth_text = tk.Label(frame3, text="Azimuth:", bg="#D9D9D9", font=("Arial 12"))
f3_azimuth_text.pack()
f3_azimuth_text.place(x=410,y=100)

# Amimuth at start lat/lon to end lat/lon
f3_azimuth_value_degrees = tk.StringVar()
f3_azimuth_value_degrees.set("-----")
f3_azimuth_bearing_degrees = tk.Label(frame3, textvariable=f3_azimuth_value_degrees, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=3, anchor='e')
f3_azimuth_bearing_degrees.pack()
f3_azimuth_bearing_degrees.place(x=480,y=100)

# Degrees distance unit label
f3_degress_text = tk.Label(frame3, text="deg", bg="#D9D9D9", font=("Arial 12"))
f3_degress_text.pack()
f3_degress_text.place(x=512,y=100)


# ***********************************
# Create Frame #4 - Grid ID Size
frame4 = ttk.Frame(notebook, height=245)
frame4.pack(fill='both', expand=True)
notebook.add(frame4, text='Grid ID Size')

# Grid ID Label
f4_grid_id_text = tk.Label(frame4, text="Grid ID", bg="#D9D9D9", font=("Arial 12"))
f4_grid_id_text.pack()
f4_grid_id_text.place(x=36,y=40)

# Grid ID Entry
f4_grid_id_value = tk.StringVar()
f4_grid_id_entry = tk.Entry(frame4, width=13, textvariable=f4_grid_id_value, font=("Arial 10"))
f4_grid_id_entry.pack()
f4_grid_id_entry.place(x=40,y=65)

# "Calculate" button to activate calulation
f4_cmd_button1 = tk.Button(frame4, text="     Calculate     ", command=calc_grid_size)
f4_cmd_button1.pack()
f4_cmd_button1.place(x=40,y=105)

# ---------- Area label ----------
f4_area_text = tk.Label(frame4, text="Area:", bg="#D9D9D9", font=("Arial 12 bold"))
f4_area_text.pack()
f4_area_text.place(x=215,y=20)

# Area in square miles to be displayed
f4_area_value_sq_miles = tk.StringVar()
f4_area_value_sq_miles.set("--------------------")
f4_area_label_sq_mi = tk.Label(frame4, textvariable=f4_area_value_sq_miles, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f4_area_label_sq_mi.pack()
f4_area_label_sq_mi.place(x=215,y=40)

# Square miles unit label
f4_sq_mi_text = tk.Label(frame4, text="sq mi", bg="#D9D9D9", font=("Arial 12"))
f4_sq_mi_text.pack()
f4_sq_mi_text.place(x=320,y=40)

# Area in square kilometers to be displayed
f4_area_value_sq_kilometers = tk.StringVar()
f4_area_value_sq_kilometers.set("--------------------")
f4_area_label_sq_km = tk.Label(frame4, textvariable=f4_area_value_sq_kilometers, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f4_area_label_sq_km.pack()
f4_area_label_sq_km.place(x=215,y=60)

# Square kilometers unit label
f4_sq_mi_text = tk.Label(frame4, text="sq km", bg="#D9D9D9", font=("Arial 12"))
f4_sq_mi_text.pack()
f4_sq_mi_text.place(x=320,y=60)

# ---------- Perimeter label ----------
f4_perimeter_text = tk.Label(frame4, text="Perimeter:", bg="#D9D9D9", font=("Arial 12 bold"))
f4_perimeter_text.pack()
f4_perimeter_text.place(x=400,y=20)

# Perimeter in miles to be displayed
f4_perimeter_value_miles = tk.StringVar()
f4_perimeter_value_miles.set("--------------------")
f4_perimeter_label_mi = tk.Label(frame4, textvariable=f4_perimeter_value_miles, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f4_perimeter_label_mi.pack()
f4_perimeter_label_mi.place(x=400,y=40)

# Miles unit label
f4_sq_mi_text = tk.Label(frame4, text="mi", bg="#D9D9D9", font=("Arial 12"))
f4_sq_mi_text.pack()
f4_sq_mi_text.place(x=505,y=40)

# Perimeter in kilometers to be displayed
f4_perimeter_value_kilometers = tk.StringVar()
f4_perimeter_value_kilometers.set("--------------------")
f4_perimeter_label_km = tk.Label(frame4, textvariable=f4_perimeter_value_kilometers, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f4_perimeter_label_km.pack()
f4_perimeter_label_km.place(x=400,y=60)

# Kilometers unit label
f4_sq_km_text = tk.Label(frame4, text="km", bg="#D9D9D9", font=("Arial 12"))
f4_sq_km_text.pack()
f4_sq_km_text.place(x=505,y=60)

# ---------- Sides label ----------
f4_sides_text = tk.Label(frame4, text="Sides:", bg="#D9D9D9", font=("Arial 12 bold"))
f4_sides_text.pack()
f4_sides_text.place(x=215,y=90)

# ---------- North label ----------
f4_north_text = tk.Label(frame4, text="North", bg="#D9D9D9", font=("Arial 12"))
f4_north_text.pack()
f4_north_text.place(x=225,y=110)

# North side in miles to be displayed
f4_north_value_miles = tk.StringVar()
f4_north_value_miles.set("--------------------")
f4_north_label_mi = tk.Label(frame4, textvariable=f4_north_value_miles, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f4_north_label_mi.pack()
f4_north_label_mi.place(x=280,y=110)

# Miles unit label
f4_north_mi_text = tk.Label(frame4, text="mi", bg="#D9D9D9", font=("Arial 12"))
f4_north_mi_text.pack()
f4_north_mi_text.place(x=385,y=110)

# North side in kilometers to be displayed
f4_north_value_kilometers = tk.StringVar()
f4_north_value_kilometers.set("--------------------")
f4_north_label_km = tk.Label(frame4, textvariable=f4_north_value_kilometers, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f4_north_label_km.pack()
f4_north_label_km.place(x=410,y=110)

# Kilometers unit label
f4_north_km_text = tk.Label(frame4, text="km", bg="#D9D9D9", font=("Arial 12"))
f4_north_km_text.pack()
f4_north_km_text.place(x=515,y=110)

# ---------- South label ----------
f4_south_text = tk.Label(frame4, text="South", bg="#D9D9D9", font=("Arial 12"))
f4_south_text.pack()
f4_south_text.place(x=225,y=130)

# South side in miles to be displayed
f4_south_value_miles = tk.StringVar()
f4_south_value_miles.set("--------------------")
f4_south_label_mi = tk.Label(frame4, textvariable=f4_south_value_miles, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f4_south_label_mi.pack()
f4_south_label_mi.place(x=280,y=130)

# Miles unit label
f4_north_mi_text = tk.Label(frame4, text="mi", bg="#D9D9D9", font=("Arial 12"))
f4_north_mi_text.pack()
f4_north_mi_text.place(x=385,y=130)

# South side in kilometers to be displayed
f4_south_value_kilometers = tk.StringVar()
f4_south_value_kilometers.set("--------------------")
f4_south_label_km = tk.Label(frame4, textvariable=f4_south_value_kilometers, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f4_south_label_km.pack()
f4_south_label_km.place(x=410,y=130)

# Kilometers unit label
f4_south_km_text = tk.Label(frame4, text="km", bg="#D9D9D9", font=("Arial 12"))
f4_south_km_text.pack()
f4_south_km_text.place(x=515,y=130)

# ---------- East label ----------
f4_east_text = tk.Label(frame4, text="East", bg="#D9D9D9", font=("Arial 12"))
f4_east_text.pack()
f4_east_text.place(x=225,y=150)

# East side in miles to be displayed
f4_east_value_miles = tk.StringVar()
f4_east_value_miles.set("--------------------")
f4_east_label_mi = tk.Label(frame4, textvariable=f4_east_value_miles, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f4_east_label_mi.pack()
f4_east_label_mi.place(x=280,y=150)

# Miles unit label
f4_east_mi_text = tk.Label(frame4, text="mi", bg="#D9D9D9", font=("Arial 12"))
f4_east_mi_text.pack()
f4_east_mi_text.place(x=385,y=150)

# East side in kilometers to be displayed
f4_east_value_kilometers = tk.StringVar()
f4_east_value_kilometers.set("--------------------")
f4_east_label_km = tk.Label(frame4, textvariable=f4_east_value_kilometers, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f4_east_label_km.pack()
f4_east_label_km.place(x=410,y=150)

# Kilometers unit label
f4_east_km_text = tk.Label(frame4, text="km", bg="#D9D9D9", font=("Arial 12"))
f4_east_km_text.pack()
f4_east_km_text.place(x=515,y=150)

# ---------- West label ----------
f4_west_text = tk.Label(frame4, text="West", bg="#D9D9D9", font=("Arial 12"))
f4_west_text.pack()
f4_west_text.place(x=225,y=170)

# West side in miles to be displayed
f4_west_value_miles = tk.StringVar()
f4_west_value_miles.set("--------------------")
f4_west_label_mi = tk.Label(frame4, textvariable=f4_west_value_miles, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f4_west_label_mi.pack()
f4_west_label_mi.place(x=280,y=170)

# Miles unit label
f4_west_mi_text = tk.Label(frame4, text="mi", bg="#D9D9D9", font=("Arial 12"))
f4_west_mi_text.pack()
f4_west_mi_text.place(x=385,y=170)

# West side in kilometers to be displayed
f4_west_value_kilometers = tk.StringVar()
f4_west_value_kilometers.set("--------------------")
f4_west_label_km = tk.Label(frame4, textvariable=f4_west_value_kilometers, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f4_west_label_km.pack()
f4_west_label_km.place(x=410,y=170)

# Kilometers unit label
f4_west_km_text = tk.Label(frame4, text="km", bg="#D9D9D9", font=("Arial 12"))
f4_west_km_text.pack()
f4_west_km_text.place(x=515,y=170)

# ***********************************
# Create Frame #5 - Grid ID Bounds
frame5 = ttk.Frame(notebook, height=245)
frame5.pack(fill='both', expand=True)
notebook.add(frame5, text='Grid ID Boundary')

# Grid ID Label
f4_start_grid_id_text = tk.Label(frame5, text="Grid ID", bg="#D9D9D9", font=("Arial 12"))
f4_start_grid_id_text.pack()
f4_start_grid_id_text.place(x=36,y=40)

# Grid ID Entry
f5_grid_id_value = tk.StringVar()
f5_grid_id_entry = tk.Entry(frame5, width=13, textvariable=f5_grid_id_value, font=("Arial 10"))
f5_grid_id_entry.pack()
f5_grid_id_entry.place(x=40,y=65)

# "Calculate" button to activate calulation
f5_cmd_button1 = tk.Button(frame5, text="     Calculate     ", command=calc_grid_boundary)
f5_cmd_button1.pack()
f5_cmd_button1.place(x=40,y=105)

# ---------- Grid Boundary Label----------
f5_grid_boundary_text = tk.Label(frame5, text="Grid Boundary", bg="#D9D9D9", font=("Arial 12 bold"))
f5_grid_boundary_text.pack()
f5_grid_boundary_text.place(x=210,y=30)

# ---------- Lat Label ----------
f5_Lat_text = tk.Label(frame5, text="Lat", bg="#D9D9D9", font=("Arial 12"))
f5_Lat_text.pack()
f5_Lat_text.place(x=365,y=50)

# ---------- Lon Label ----------
f5_Lon_text = tk.Label(frame5, text="Lon", bg="#D9D9D9", font=("Arial 12"))
f5_Lon_text.pack()
f5_Lon_text.place(x=495,y=50)

# ---------- NE Corner Label ----------
f5_NE_corner_text = tk.Label(frame5, text="NE Corner", bg="#D9D9D9", font=("Arial 12"))
f5_NE_corner_text.pack()
f5_NE_corner_text.place(x=210,y=70)

# NE Latitude to be displayed
f5_NE_lat_value = tk.StringVar()
f5_NE_lat_value.set("-----------------")
f5_NE_corner_label = tk.Label(frame5, textvariable=f5_NE_lat_value, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f5_NE_corner_label.pack()
f5_NE_corner_label.place(x=320,y=70)

# NE Longitude to be displayed
f5_NE_lon_value = tk.StringVar()
f5_NE_lon_value.set("-----------------")
f5_NE_lon_label = tk.Label(frame5, textvariable=f5_NE_lon_value, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f5_NE_lon_label.pack()
f5_NE_lon_label.place(x=450,y=70)

# ---------- SE Corner Label ----------
f5_SE_corner_text = tk.Label(frame5, text="SE Corner", bg="#D9D9D9", font=("Arial 12"))
f5_SE_corner_text.pack()
f5_SE_corner_text.place(x=210,y=90)

# SE Latitude to be displayed
f5_SE_lat_value = tk.StringVar()
f5_SE_lat_value.set("-----------------")
f5_SE_corner_label = tk.Label(frame5, textvariable=f5_SE_lat_value, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f5_SE_corner_label.pack()
f5_SE_corner_label.place(x=320,y=90)

# SE Longitude to be displayed
f5_SE_lon_value = tk.StringVar()
f5_SE_lon_value.set("-----------------")
f5_SE_lon_label = tk.Label(frame5, textvariable=f5_SE_lon_value, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f5_SE_lon_label.pack()
f5_SE_lon_label.place(x=450,y=90)

# ---------- SW Corner Label ----------
f5_SW_corner_text = tk.Label(frame5, text="SW Corner", bg="#D9D9D9", font=("Arial 12"))
f5_SW_corner_text.pack()
f5_SW_corner_text.place(x=210,y=110)

# SW Latitude to be displayed
f5_SW_lat_value = tk.StringVar()
f5_SW_lat_value.set("-----------------")
f5_SW_corner_label = tk.Label(frame5, textvariable=f5_SW_lat_value, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f5_SW_corner_label.pack()
f5_SW_corner_label.place(x=320,y=110)

# SW Longitude to be displayed
f5_SW_lon_value = tk.StringVar()
f5_SW_lon_value.set("-----------------")
f5_SW_lon_label = tk.Label(frame5, textvariable=f5_SW_lon_value, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f5_SW_lon_label.pack()
f5_SW_lon_label.place(x=450,y=110)

# ---------- NW Corner Label ----------
f5_NW_corner_text = tk.Label(frame5, text="NW Corner", bg="#D9D9D9", font=("Arial 12"))
f5_NW_corner_text.pack()
f5_NW_corner_text.place(x=210,y=130)

# NW Latitude to be displayed
f5_NW_lat_value = tk.StringVar()
f5_NW_lat_value.set("-----------------")
f5_NW_corner_label = tk.Label(frame5, textvariable=f5_NW_lat_value, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f5_NW_corner_label.pack()
f5_NW_corner_label.place(x=320,y=130)

# NW Longitude to be displayed
f5_NW_lon_value = tk.StringVar()
f5_NW_lon_value.set("-----------------")
f5_NW_lon_label = tk.Label(frame5, textvariable=f5_NW_lon_value, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f5_NW_lon_label.pack()
f5_NW_lon_label.place(x=450,y=130)

# ---------- Grid Center Label ----------
f5_grid_center_text = tk.Label(frame5, text="Grid Center", bg="#D9D9D9", font=("Arial 12"))
f5_grid_center_text.pack()
f5_grid_center_text.place(x=210,y=150)

# Grid Center Latitude to be displayed
f5_grid_center_lat_value = tk.StringVar()
f5_grid_center_lat_value.set("-----------------")
f5_grid_center_lat_label = tk.Label(frame5, textvariable=f5_grid_center_lat_value, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f5_grid_center_lat_label.pack()
f5_grid_center_lat_label.place(x=320,y=150)

# Grid Center Longitude to be displayed
f5_grid_center_lon_value = tk.StringVar()
f5_grid_center_lon_value.set("-----------------")
f5_grid_center_lon_label = tk.Label(frame5, textvariable=f5_grid_center_lon_value, fg="#0603ff", bg="#D9D9D9", font=("Arial", 12),  width=11, anchor='e')
f5_grid_center_lon_label.pack()
f5_grid_center_lon_label.place(x=450,y=150)

# =========================================================
# Call main event loop for the application window
root.mainloop()