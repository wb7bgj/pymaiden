'''
Lookup tuples and dictionarys used by pymaiden to create a grid ID from
and given lat/lon or lat/lon boundary locations from a given grid ID. 

Written by: Kevin Hallquist, WB7BGJ
'''

# =============================================================================
# Tuples used to determine grid ID letter for a given latitude or longitude

# Used to calculate first letter pair (AA-RR) 
field = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R')

# Used to calculate third letter pair (aa-xx)
subsquare = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x')

# Used to calculate fifth letter pair (AA-XX)
supsextsubsquare = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X')

# ============================== Latitude tables ==============================
# Used to provide a numeric degree, minute or seconds value for a given latitude letter 

# Field boundary values in degrees
lat_field = {'A':-90,
             'B':-80,
             'C':-70,
             'D':-60,
             'E':-50,
             'F':-40,
             'G':-30,
             'H':-20,
             'I':-10,
             'J':0,
             'K':10,
             'L':20,
             'M':30,
             'N':40,
             'O':50,
             'P':60,
             'Q':70,
             'R':80
             }

# Square boundary values in degrees
lat_square = {'0':0,
              '1':1,
              '2':2,
              '3':3,
              '4':4,
              '5':5,
              '6':6,
              '7':7,
              '8':8,
              '9':9
              }

# Subsquare boundary values in minutes
lat_subsquare = {'a':0.0,
                 'b':2.5,
                 'c':5.0,
                 'd':7.5,
                 'e':10.0,
                 'f':12.5,
                 'g':15.0,
                 'h':17.5,
                 'i':20.0,
                 'j':22.5,
                 'k':25.0,
                 'l':27.5,
                 'm':30.0,
                 'n':32.5,
                 'o':35.0,
                 'p':37.5,
                 'q':40.0,
                 'r':42.5,
                 's':45.0,
                 't':47.5,
                 'u':50.0,
                 'v':52.5,
                 'w':55.0,
                 'x':57.5
                }

# Extended square boundary values in seconds
lat_extendedsquare = {'0':0,
                      '1':15,
                      '2':30,
                      '3':45,
                      '4':60,
                      '5':75,
                      '6':90,
                      '7':105,
                      '8':120,
                      '9':135
                     }

# Super extended square boundary values in seconds
lat_supextsquare = {'A':0,
                    'B':0.625,
                    'C':1.25,
                    'D':1.875,
                    'E':2.5,
                    'F':3.125,
                    'G':3.75,
                    'H':4.375,
                    'I':5,
                    'J':5.625,
                    'K':6.25,
                    'L':6.875,
                    'M':7.5,
                    'N':8.125,
                    'O':8.75,
                    'P':9.375,
                    'Q':10,
                    'R':10.625,
                    'S':11.25,
                    'T':11.875,
                    'U':12.5,
                    'V':13.125,
                    'W':13.75,
                    'X':14.375
                }

# ============================== Longitude tables =============================
# Used to provide a numeric degree, minute or seconds value for a given longitude letter 

# Field boundary values in degrees
lon_field = {'A':-180,
             'B':-160,
             'C':-140,
             'D':-120,
             'E':-100,
             'F':-80,
             'G':-60,
             'H':-40,
             'I':-20,
             'J':0,
             'K':20,
             'L':40,
             'M':60,
             'N':80,
             'O':100,
             'P':120,
             'Q':140,
             'R':160
             }

# Square boundary values in degrees
lon_square = {'0':0,
              '1':2,
              '2':4,
              '3':6,
              '4':8,
              '5':10,
              '6':12,
              '7':14,
              '8':16,
              '9':18
              }

# Subsquare boundary values in minutes
lon_subsquare = {'a':0,
                 'b':5,
                 'c':10,
                 'd':15,
                 'e':20,
                 'f':25,
                 'g':30,
                 'h':35,
                 'i':40,
                 'j':45,
                 'k':50,
                 'l':55,
                 'm':60,
                 'n':65,
                 'o':70,
                 'p':75,
                 'q':80,
                 'r':85,
                 's':90,
                 't':95,
                 'u':100,
                 'v':105,
                 'w':110,
                 'x':115
                 }

# Extended boundary values in seconds
lon_extendedsquare = {'0':0,
                      '1':30,
                      '2':60,
                      '3':90,
                      '4':120,
                      '5':150,
                      '6':180,
                      '7':210,
                      '8':240,
                      '9':270
                     }

# Super extended boundary values in seconds
lon_supextsquare = {'A':0,
                    'B':1.25,
                    'C':2.5,
                    'D':3.75,
                    'E':5,
                    'F':6.25,
                    'G':7.5,
                    'H':8.75,
                    'I':10,
                    'J':11.25,
                    'K':12.5,
                    'L':13.75,
                    'M':15,
                    'N':16.25,
                    'O':17.5,
                    'P':18.75,
                    'Q':20,
                    'R':21.25,
                    'S':22.5,
                    'T':23.75,
                    'U':25,
                    'V':26.25,
                    'W':27.5,
                    'X':28.75
                }