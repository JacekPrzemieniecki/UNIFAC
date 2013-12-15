'''
Created on 08-10-2012

@author: Jacek Przemieniecki
'''
from . import errors

class Database(object):
    
    def get_atom_valency(self, symbol):
        return valency[symbol]
    
    def get_q_r(self, symbol):
        grp_id = str_to_id[symbol][0]
        return q_r_data[grp_id]
    
    def get_parameter(self, symbol1, symbol2):
        
        if symbol1 == symbol2:
            return 0.0
        
        grp1 = str_to_id[symbol1][1] - 1 # Adjust for list indexing starting at 0
        grp2 = str_to_id[symbol2][1] - 1
        
        param = params[grp1][grp2]
        
        if param is None:
            raise errors.ValueNotFound()
        else:
            return param
    
    def iterate_strings(self):
        for key in str_to_id:
            yield key
    
    def __init__(self):
        pass

valency = {"C" : 4,
           "N" : 3,
           "O" : 2,
           "S" : 2,
           "Si" : 4,
           "Cl" : 1,
           "Br" : 1,
           "I" : 1,
           "F" : 1}

### Data from http://www.aim.env.uea.ac.uk/aim/info/UNIFACgroups.html
params = [[0.0, 86.02, 61.13, 76.5, 986.5, 697.2, 1318.0, 1333.0, 476.4, 677.0, 232.1, 507.0, 251.5, 391.5, 255.7, 206.6, 920.7, 287.77, 597.0, 663.5, 35.93, 53.76, 24.9, 104.3, 11.44, 661.5, 543.0, 153.6, 184.4, 354.55, 3025.0, 335.8, 479.5, 298.9, 526.5, 689.0, -4.189, 125.8, 485.3, -2.859, 387.1, -450.4, 252.7, 220.3, -5.869, 390.9, 553.3, 187.0, 216.1, 92.99, None, 808.59, 408.3, 718.01, None, 153.72, ], #1
[-35.36, 0.0, 38.81, 74.15, 524.1, 787.6, 270.6, 526.1, 182.6, 448.8, 37.85, 333.5, 214.5, 240.9, 163.9, 61.11, 749.3, 280.5, 336.9, 318.9, -36.87, 58.55, -13.99, -109.7, 100.1, 357.5, None, 76.302, None, 262.9, None, None, 183.8, 31.14, 179.0, -52.87, -66.46, 359.3, -70.45, 449.4, 48.33, None, None, 86.46, None, 200.2, 268.1, -617.0, 62.56, None, None, 200.94, 219.9, -677.25, None, None, ], #2
[-11.12, 3.446, 0.0, 167.0, 636.1, 637.35, 903.8, 1329.0, 25.77, 347.3, 5.994, 287.1, 32.14, 161.7, 122.8, 90.49, 648.2, -4.449, 212.5, 537.4, -18.81, -144.4, -231.9, 3.0, 187.0, 168.0, 194.9, 52.07, -10.43, -64.69, 210.4, 113.3, 261.3, 154.26, 169.9, 383.9, -259.1, 389.3, 245.6, 22.67, 103.5, -432.3, 238.9, 30.04, -88.11, None, 333.3, None, -59.58, -39.16, None, 360.82, 171.49, 272.33, 22.06, 174.35, ], #3
[-69.7, -113.6, -146.8, 0.0, 803.2, 603.25, 5695.0, 884.9, -52.1, 586.6, 5688.0, 197.8, 213.1, 19.02, -49.29, 23.5, 664.2, 52.8, 6096.0, 872.3, -114.1, -111.0, -80.25, -141.3, -211.0, 3629.0, 4448.0, -9.451, 393.6, 48.49, 4975.0, 259.0, 210.0, -152.55, 4284.0, -119.2, -282.5, 101.4, 5629.0, -245.39, 69.26, 683.3, 355.5, 46.38, None, None, 421.9, None, -203.6, 184.9, None, 233.51, -184.68, 9.63, 795.38, -280.9, ], #4
[156.4, 457.0, 89.6, 25.82, 0.0, -137.1, 353.5, -259.7, 84.0, -203.6, 101.1, 267.8, 28.06, 83.02, 42.7, -323.0, -52.39, 170.0, 6.712, 199.0, 75.62, 65.28, -98.12, 143.1, 123.5, 256.5, 157.1, 488.9, 147.5, -120.5, -318.9, 313.5, 202.1, 727.8, -202.1, 74.27, 225.8, 44.78, -143.9, None, 190.3, -817.7, 202.7, -504.2, 72.96, -382.7, -248.3, None, 104.7, 57.65, None, 215.81, 6.39, None, None, 147.97, ], #5
[16.51, -12.52, -50.0, -44.5, 249.1, 0.0, -181.0, -101.7, 23.39, 306.4, -10.72, 179.7, -128.6, 359.3, -20.98, 53.9, 489.7, 580.5, 53.28, -202.0, -38.32, -102.5, -139.4, -44.76, -28.25, 75.14, 457.88, -31.09, 17.5, -61.76, -119.2, 212.1, 106.3, -119.1, -399.3, -5.224, 33.47, -48.25, -172.4, None, 165.7, None, None, None, -52.1, None, None, 37.63, -59.4, -46.01, None, 150.02, 98.2, None, None, None, ], #6
[300.0, 496.1, 362.3, 377.6, -229.1, 289.6, 0.0, 324.5, -195.4, -116.0, 72.87, 233.87, 540.5, 48.89, 168.0, 304.0, 459.0, 459.0, 112.6, -14.09, 325.4, 370.4, 353.7, 497.5, 133.9, 220.6, 399.5, 887.1, None, 188.0, 12.72, None, 777.1, None, -139.0, 160.8, None, None, 319.0, None, -197.5, -363.8, None, -452.2, None, 835.6, 139.6, None, 407.9, None, None, -255.63, -144.77, None, None, 580.28, ], #7
[275.8, 217.5, 25.34, 244.2, -451.6, -265.2, -601.8, 0.0, -356.1, -271.1, -449.4, -32.52, -162.9, -832.97, None, None, -305.5, -305.5, None, 408.9, None, 517.27, None, 1827.0, 6915.0, None, -413.48, 8484.0, None, None, -687.1, None, None, None, None, None, None, None, None, None, -494.2, None, None, -659.0, None, None, None, None, None, 1005.0, None, None, None, None, None, None, ], #8
[26.76, 42.92, 140.1, 365.8, 164.5, 108.7, 472.5, -133.1, 0.0, -37.36, -213.7, -190.4, -103.6, None, -174.2, -169.0, 6201.0, 7.341, 481.7, 669.4, -191.7, -130.3, -354.6, -39.2, -119.8, 137.5, 548.5, 216.1, -46.28, -163.7, 71.46, 53.59, 245.2, -246.6, -44.58, -63.5, -34.57, None, -61.7, None, -18.8, -588.9, None, None, None, None, 37.54, None, None, -162.6, None, None, -288.94, 91.01, None, 179.74, ], #9
[505.7, 56.3, 23.39, 106.0, 529.0, -340.2, 480.8, -155.6, 128.0, 0.0, -110.3, 766.0, 304.1, None, None, None, None, None, -106.4, 497.5, 751.9, 67.52, -483.7, None, None, None, None, None, None, None, None, 117.0, None, 2.21, None, -339.2, 172.4, None, -268.8, None, -275.5, None, None, None, None, None, None, None, None, None, None, None, 79.71, None, None, None, ], #10
[114.8, 132.1, 85.84, -170.0, 245.4, 249.63, 200.8, -36.72, 372.2, 185.1, 0.0, -241.8, -235.7, None, -73.5, -196.7, 475.5, -0.13, 494.6, 660.2, -34.74, 108.9, -209.7, 54.57, 442.4, -81.13, None, 183.0, None, 202.3, -101.7, 148.3, 18.88, 71.48, 52.08, -28.61, -275.2, None, 85.33, None, 560.2, None, None, None, None, None, 151.8, None, None, None, None, None, 36.34, 446.9, None, None, ], #11
[329.3, 110.4, 18.12, 428.0, 139.4, 227.8, 124.63, -234.25, 385.4, -236.5, 1167.0, 0.0, -234.0, None, None, None, None, -233.4, -47.25, -268.1, None, 31.0, -126.2, 179.7, 24.28, None, None, None, 103.9, None, None, None, 298.13, None, None, None, -11.4, None, 308.9, None, -70.24, None, None, None, None, None, None, None, None, None, None, None, -77.96, None, None, None, ], #12
[83.36, 26.51, 52.13, 65.69, 237.7, 238.4, -314.7, -178.5, 191.1, -7.838, 461.3, 457.3, 0.0, -78.36, 251.5, 5422.3, -46.39, 213.2, -18.51, 664.6, 301.1, 137.8, -154.3, 47.67, 134.8, 95.18, 155.11, 140.9, -8.538, 170.1, -20.11, -149.5, -202.3, -156.57, 128.8, None, 240.2, -273.9, 254.8, -172.51, 417.0, 1338.0, None, None, None, None, None, None, None, None, None, None, 567.0, 102.21, None, None, ], #13
[-30.48, 1.163, -44.85, 296.4, -242.8, -481.7, -330.48, -870.8, None, None, None, None, 222.1, 0.0, -107.2, -41.11, -200.7, None, 358.9, None, -82.92, None, None, -99.81, 30.05, None, None, None, -70.14, None, None, None, None, None, 874.19, None, None, None, -164.0, None, None, -664.4, 275.9, None, None, None, None, None, None, None, None, None, None, None, None, None, ], #14
[65.33, -28.7, -22.31, 223.0, -150.0, -370.3, -448.2, None, 394.6, None, 136.0, None, -56.08, 127.4, 0.0, -189.2, 138.54, 431.49, 147.1, None, None, None, None, 71.23, -18.93, None, None, None, None, None, 939.07, None, None, None, None, None, None, 570.9, -255.22, None, -38.77, 448.1, -1327.0, None, None, None, None, None, None, None, None, None, None, None, None, None, ], #15
[-83.98, -25.38, -223.9, 109.9, 28.6, -406.8, -598.8, None, 225.3, None, 2889.0, None, -194.1, 38.89, 865.9, 0.0, 287.43, None, 1255.1, None, -182.91, -73.85, -352.9, -262.0, -181.9, None, None, None, None, None, None, None, None, None, 243.1, None, None, -196.3, 22.05, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, ], #16
[1139.0, 2000.0, 247.5, 762.8, -17.4, -118.1, -341.6, -253.1, -450.3, None, -294.8, None, 285.36, -15.07, 64.3, -24.46, 0.0, 89.7, -281.6, -396.0, 287.0, -111.0, None, 882.0, 617.5, None, -139.3, None, None, None, 0.1004, None, None, None, None, None, None, None, -334.4, None, -89.42, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, ], #17
[-101.6, -47.63, 31.87, 49.8, -132.3, -378.2, -332.9, -341.6, 29.1, None, 8.87, 554.4, -156.1, None, -207.66, None, 117.4, 0.0, -169.7, -153.7, None, -351.6, -114.7, -205.3, -2.17, None, 2845.0, None, None, None, None, None, -60.78, None, None, None, 160.7, -158.8, None, None, None, None, None, None, None, None, None, None, None, -136.6, None, None, None, 98.82, None, None, ], #18
[24.82, -40.62, -22.97, -138.4, 185.4, 162.6, 242.8, None, -287.5, 224.66, -266.6, 99.37, 38.81, -157.3, -108.5, -446.86, 777.4, 134.3, 0.0, 205.27, 4.933, -152.7, -15.62, -54.86, -4.624, -0.515, None, 230.9, 0.4604, None, 177.5, None, -62.17, -203.0, None, 81.57, -55.77, None, -151.5, None, 120.3, None, None, None, None, None, 16.23, None, None, None, None, None, None, None, None, None, ], #19
[315.3, 1264.0, 62.32, 89.86, -151.0, 339.8, -66.17, -11.0, -297.8, -165.5, -256.3, 193.9, -338.5, None, None, None, 493.8, -313.5, 92.07, 0.0, 13.41, -44.7, 39.63, 183.4, -79.08, None, None, None, None, -208.9, None, 228.4, -95.0, None, -463.6, None, -11.16, None, -228.0, None, -337.0, 169.3, 127.2, None, None, -322.3, None, None, None, None, None, None, 12.55, -60.07, 88.09, None, ], #20
[91.46, 40.25, 4.68, 122.9, 562.2, 529.0, 698.2, None, 286.3, -47.51, 35.38, None, 225.4, 131.2, None, 151.38, 429.7, None, 54.32, 519.1, 0.0, 108.3, 249.2, 62.42, 153.0, 32.73, 86.2, 450.1, 59.02, 65.56, None, 2.22, 344.4, None, None, None, -168.2, None, 6.57, None, 63.67, None, None, None, None, None, None, None, None, None, None, None, -127.9, None, None, None, ], #21
[34.01, -23.5, 121.3, 140.8, 527.6, 669.9, 708.7, 1633.5, 82.86, 190.6, -132.9, 80.99, -197.7, None, None, -141.4, 140.8, 587.3, 258.6, 543.3, -84.53, 0.0, 0.0, 56.33, 223.1, 108.9, None, None, None, 149.56, None, 177.6, 315.9, None, 215.0, None, -91.8, None, -160.28, None, -96.87, None, None, None, None, None, 361.1, None, None, None, None, None, None, None, None, None, ], #22
[36.7, 51.06, 288.5, 69.9, 742.1, 649.1, 826.76, None, 552.1, 242.8, 176.5, 235.6, -20.93, None, None, -293.7, None, 18.98, 74.04, 504.2, -157.1, 0.0, 0.0, -30.1, 192.1, None, None, 116.6, None, -64.38, None, 86.4, 168.8, None, 363.7, None, 111.2, None, None, None, 255.8, None, None, -35.68, None, None, None, 565.9, None, None, None, None, 165.67, None, None, None, ], #23
[-78.45, 160.9, -4.7, 134.7, 856.3, 709.6, 1201.0, 10000.0, 372.0, None, 129.5, 351.9, 113.9, 261.1, 91.13, 316.9, 898.2, 368.5, 492.0, 631.0, 11.8, 17.97, 51.9, 0.0, -75.97, 490.9, 534.7, 132.2, None, 546.7, None, 247.8, 146.6, None, 337.7, 369.5, 187.1, 215.2, 498.6, None, 256.5, None, 233.1, None, None, None, 423.1, 63.95, None, 108.5, None, 585.19, 291.87, 532.73, None, 127.16, ], #24
[106.8, 70.32, -97.27, 402.5, 325.7, 612.8, -274.5, 622.3, 518.4, None, -171.1, 383.3, -25.15, 108.5, 102.2, 2951.0, 334.9, 20.18, 363.5, 993.4, -129.7, -8.309, -0.2266, -248.4, 0.0, 132.7, 2213.0, None, None, None, None, None, 593.4, None, 1337.37, None, None, None, 5143.14, 309.58, -145.1, None, None, -209.7, None, None, 434.1, None, None, None, None, None, None, None, None, 8.48, ], #25
[-32.69, -1.996, 10.38, -97.05, 261.6, 252.6, 417.9, None, -142.6, None, 129.3, None, -94.49, None, None, None, None, None, 0.2827, None, 113.0, -9.639, None, -34.68, 132.9, 0.0, 533.2, 320.2, None, None, 139.8, 304.3, 10.17, -27.7, None, None, 10.76, None, -223.1, None, 248.4, None, None, None, -218.9, None, None, None, None, -4.565, None, None, None, None, None, None, ], #26
[5541.0, None, 1824.0, -127.8, 561.6, 511.29, 360.7, 815.12, -101.5, None, None, None, 220.66, None, None, None, 134.9, 2475.0, None, None, 1971.0, None, None, 514.6, -123.1, -85.12, 0.0, None, None, None, None, 2990.0, -124.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1742.53, ], #27
[-52.65, 16.62, 21.5, 40.68, 609.8, 914.2, 1081.0, 1421.0, 303.7, None, 243.8, None, 112.4, None, None, None, None, None, 335.7, None, -73.09, None, -26.06, -60.71, None, 277.8, None, 0.0, None, None, None, 292.7, None, None, None, None, -47.37, None, None, None, 469.8, None, None, None, None, None, None, None, None, None, None, None, None, 684.78, None, None, ], #28
[-7.481, None, 28.41, 19.56, 461.6, 448.6, None, None, 160.6, None, None, 201.5, 63.71, 106.7, None, None, None, None, 161.0, None, -27.94, None, None, None, None, None, None, None, 0.0, None, None, None, None, None, 31.66, None, None, None, 78.92, None, None, None, None, 1004.0, None, None, None, -18.27, None, None, None, None, None, None, None, None, ], #29
[-25.31, 82.64, 157.3, 128.8, 521.6, 287.0, 23.48, None, 317.5, None, -146.3, None, -87.31, None, None, None, None, None, None, 570.6, -39.46, -116.21, 48.48, -133.16, None, None, None, None, None, 0.0, None, None, None, None, None, None, 262.9, None, None, None, 43.37, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, ], #30
[140.0, None, 221.4, 150.6, 267.6, 240.8, -137.4, 838.4, 135.4, None, 152.0, None, 9.207, None, -213.74, None, 192.3, None, 169.6, None, None, None, None, None, None, 481.3, None, None, None, None, 0.0, None, None, None, -417.2, None, None, None, 302.2, None, 347.8, None, None, -262.0, None, None, -353.5, None, None, None, None, None, None, None, None, None, ], #31
[128.0, None, 58.68, 26.41, 501.3, 431.3, None, None, 138.0, 245.9, 21.92, None, 476.6, None, None, None, None, None, None, 616.6, 179.25, -40.82, 21.76, 48.49, None, 64.28, 2448.0, -27.45, None, None, None, 0.0, 6.37, None, None, None, None, None, None, None, 68.55, None, None, None, None, None, None, None, None, None, None, None, None, 190.81, None, None, ], #32
[-31.52, 174.6, -154.2, 1112.0, 524.9, 494.7, 79.18, None, -142.6, None, 24.37, -92.26, 736.4, None, None, None, None, -42.71, 136.9, 5256.0, -262.3, -174.5, -46.8, 77.55, -185.3, 125.3, 4288.0, None, None, None, None, 37.1, 0.0, None, 32.9, None, -48.33, None, 336.25, None, -195.1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, ], #33
[-72.88, 41.38, -101.12, 614.52, 68.95, 967.71, None, None, 443.6, -55.87, -111.45, None, 173.77, None, None, None, None, None, 329.1, None, None, None, None, None, None, 174.4, None, None, None, None, None, None, None, 0.0, None, None, 2073.0, None, -119.8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, ], #34
[50.49, 64.07, -2.504, -143.2, -25.87, 695.0, -240.0, None, 110.4, None, 41.57, None, -93.51, -366.51, None, -257.2, None, None, None, -180.2, None, -215.0, -343.6, -58.43, -334.12, None, None, None, 85.7, None, 535.8, None, -111.2, None, 0.0, None, None, None, -97.71, None, 153.7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, ], #35
[-165.9, 573.0, -123.6, 397.4, 389.3, 218.8, 386.6, None, 114.55, 354.0, 175.5, None, None, None, None, None, None, None, -42.31, None, None, None, None, -85.15, None, None, None, None, None, None, None, None, None, None, None, 0.0, -208.8, None, -8.804, None, 423.4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, ], #36
[47.41, 124.2, 395.8, 419.1, 738.9, 528.0, None, None, -40.9, 183.8, 611.3, 134.5, -217.9, None, None, None, None, 281.6, 335.2, 898.2, 383.2, 301.9, -149.8, -134.2, None, 379.4, None, 167.9, None, 82.64, None, None, 322.42, 631.5, None, 837.2, 0.0, None, 255.0, None, 730.8, None, None, None, None, None, None, 2429.0, None, None, None, None, -127.06, None, None, None, ], #37
[-5.132, -131.7, -237.2, -157.3, 649.7, 645.9, None, None, None, None, None, None, 167.1, None, -198.8, 116.5, None, 159.8, None, None, None, None, None, -124.6, None, None, None, None, None, None, None, None, None, None, None, None, None, 0.0, -110.65, -117.2, None, None, None, 26.35, None, None, None, None, None, None, None, None, None, None, None, 117.59, ], #38
[-31.95, 249.0, -133.9, -240.2, 64.16, 172.2, -287.1, None, 97.04, 13.89, -82.12, -116.7, -158.2, 49.7, 10.03, -185.2, 343.7, None, 150.6, -97.77, -55.21, 397.24, None, -186.7, -374.16, 223.6, None, None, -71.0, None, -191.7, None, -176.26, 6.699, 136.6, 5.15, -137.7, 50.06, 0.0, -5.579, 72.31, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 39.84, ], #39
[147.3, 62.4, 140.6, 839.83, None, None, None, None, None, None, None, None, 278.15, None, None, None, None, None, None, None, None, None, None, None, 33.95, None, None, None, None, None, None, None, None, None, None, None, None, 185.6, 55.8, 0.0, None, None, None, None, 111.8, None, None, None, None, None, None, None, None, None, None, None, ], #40
[529.0, 1397.0, 317.6, 615.8, 88.63, 171.0, 284.4, -167.3, 123.4, 577.5, -234.9, 65.37, -247.8, None, 284.5, None, -22.1, None, -61.6, 1179.0, 182.2, 305.4, -193.0, 335.7, 1107.0, -124.7, None, 885.5, None, -64.28, -264.3, 288.1, 627.7, None, -29.34, -53.91, -198.0, None, -28.65, None, 0.0, None, None, None, None, None, None, None, None, None, None, None, None, -100.53, None, None, ], #41
[-34.36, None, 787.9, 191.6, 1913.0, None, 180.2, None, 992.4, None, None, None, 448.5, 961.8, 1464.0, None, None, None, None, 2450.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0.0, -2166.0, None, None, None, None, None, None, None, None, None, None, None, None, None, ], #42
[110.2, None, 234.4, 221.8, 84.85, None, None, None, None, None, None, None, None, -125.2, 1604.0, None, None, None, None, 2496.0, None, None, None, 70.81, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 745.3, 0.0, None, None, None, None, None, None, None, None, None, None, None, None, None, ], #43
[13.89, -16.11, -23.88, 6.214, 796.9, None, 832.2, -234.7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, -196.2, None, 161.5, None, None, None, -274.1, None, 262.0, None, None, None, None, None, -66.31, None, None, None, None, None, None, 0.0, None, None, None, None, None, None, None, None, None, None, None, None, ], #44
[30.74, None, 167.9, None, 794.4, 762.7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 844.0, None, None, None, None, None, None, None, None, None, None, None, None, None, -32.17, None, None, None, None, 0.0, None, None, None, None, None, None, None, None, None, None, None, ], #45
[27.97, 9.755, None, None, 394.8, None, -509.3, None, None, None, None, None, None, None, None, None, None, None, None, -70.25, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0.0, None, None, None, None, None, None, None, None, None, None, ], #46
[-11.92, 132.4, -86.88, -19.45, 517.5, None, -205.7, None, 156.4, None, -3.444, None, None, None, None, None, None, None, 119.2, None, None, -194.7, None, 3.163, 7.082, None, None, None, None, None, 515.8, None, None, None, None, None, None, None, None, None, 101.2, None, None, None, None, None, 0.0, None, None, None, None, None, None, None, None, None, ], #47
[39.93, 543.6, None, None, None, 420.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, -363.1, -11.3, None, None, None, None, 6.971, None, None, None, None, None, None, None, 148.9, None, None, None, None, None, None, None, None, None, None, 0.0, None, None, None, None, None, None, None, None, ], #48
[-23.61, 161.1, 142.9, 274.1, -61.2, -89.24, -384.3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0.0, None, None, None, None, None, None, None, ], #49
[-8.479, None, 23.93, 2.845, 682.5, 597.8, None, 810.5, 278.8, None, None, None, None, None, None, None, None, 221.4, None, None, None, None, None, -79.34, None, 176.3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, ], #50
[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, ], #51
[245.21, 384.45, 47.05, 347.13, 72.19, 265.75, 627.39, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 75.04, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, ], #52
[21.49, -2.8, 344.42, 510.32, 244.67, 163.76, 833.21, None, 569.18, -1.25, -38.4, 69.7, -375.6, None, None, None, None, None, None, 600.78, 291.1, None, -286.26, -52.93, None, None, None, None, None, None, None, None, None, None, None, None, 177.12, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, ], #53
[272.82, 569.71, 165.18, 369.89, None, None, None, None, -62.02, None, -229.01, None, -196.59, None, None, None, None, 100.25, None, 472.04, None, None, None, 196.73, None, None, None, 434.32, None, None, None, 313.14, None, None, None, None, None, None, None, None, -244.59, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, ], #54
[None, None, 920.49, 305.77, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 171.94, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, ], #55
[-20.31, None, -106.7, 568.47, 284.28, None, 401.2, None, 106.21, None, None, None, None, None, None, None, None, None, None, None, None, None, None, -108.37, 5.76, None, -272.01, None, None, None, None, None, None, None, None, None, None, 107.84, -33.93, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, ]] #56

# {symbol : (group_unique_id, main_group_id), ...}
# main_group_id stands for ids as listed at:
# http://www.aim.env.uea.ac.uk/aim/info/UNIFACgroups.html
# in "Group" column
str_to_id = {   'AC': (11, 3),
    'ACBr': (119, 56),
    'ACC#N': (118, 55),
    'ACCH': (14, 4),
    'ACCH2': (13, 4),
    'ACCH3': (12, 4),
    'ACCl': (54, 25),
    'ACF': (71, 38),
    'ACH': (10, 3),
    'ACN(=O)=O': (58, 27),
    'ACNH2': (37, 17),
    'ACOH': (18, 8),
    'Br': (65, 33),
    'C#C': (67, 34),
    'C(=O)N(CH2)CH2': (99, 46),
    'C(=O)N(CH3)CH2': (98, 46),
    'C(=O)N(CH3)CH3': (97, 46),
    'C(=O)NH2': (94, 46),
    'C(=O)NHCH2': (96, 46),
    'C(=O)NHCH3': (95, 46),
    'C(=O)OH': (43, 20),
#    'C2H4O2': (101, 47),
#    'C2H5O2': (100, 47),
#    'C4H2S': (108, 50),
#    'C4H3S': (107, 50),
#    'C4H4S': (106, 50),
#    'C5H3N': (40, 18),
#    'C5H4N': (39, 18),
#    'C5H5N': (38, 18),
    'C=CCl': (70, 37),
    'CCl': (47, 21),
    'CCl2': (50, 22),
    'CCl2F': (87, 45),
    'CCl2F2': (93, 45),
    'CCl3': (52, 23),
    'CCl3F': (86, 45),
    'CCl4': (53, 24),
    'CClF2': (90, 45),
    'CClF3': (92, 45),
    'CF': (76, 40),
    'CF2': (75, 40),
    'CF3': (74, 40),
    'CH': (3, 1),
    'CH#C': (66, 34),
    'CH(=O)O': (24, 12),
    'CH(=O)OH': (44, 20),
    'CH0': (4, 1),
    'CH0=CH0': (9, 2),
    'CH0OCH0': (116, 53),
    'CH2': (2, 1),
    'CH2=CH': (5, 2),
    'CH2=CH0': (7, 2),
    'CH2=CHC#N': (69, 36),
    'CH2OH0': (26, 13),
    'CH2C#N': (42, 19),
    'CH2C(=O)O': (23, 11),
    'CH2C=O': (20, 9),
    'CH2Cl': (45, 21),
    'CH2Cl2': (48, 22),
    'CH2N(=O)=O': (56, 26),
    'CH2NH': (33, 15),
    'CH2NH0': (36, 16),
    'CH2NH2': (30, 14),
#    'CH2OCH': (112, 53),    # these are oxides, not ethers
#    'CH2OCH0': (113, 53),
#    'CH2OCH2': (111, 53),
    'CH2S': (103, 48),
    'CH2SH': (61, 29),
#    'CH2SuCH': (110, 52),
#    'CH2SuCH2': (109, 52),
    'CH3': (1, 1),
    'CH3OH0': (25, 13),
    'CH3C#N': (41, 19),
    'CH3C(=O)O': (22, 11),
    'CH3C=O': (19, 9),
    'CH3N(=O)=O': (55, 26),
    'CH3NH': (32, 15),
    'CH3NH0': (35, 16),
    'CH3NH2': (29, 14),
    'CH3OH': (16, 6),
    'CH3S': (102, 48),
    'CH3SH': (60, 29),
    'CH=CH': (6, 2),
    'CH=CH0': (8, 2),
    'CHOH0': (27, 13),
    'CHCl': (46, 21),
    'CHCl2': (49, 22),
    'CHCl2F': (88, 45),
    'CHCl3': (51, 23),
    'CHClF': (89, 45),
    'CHClF2': (91, 45),
    'CHN(=O)=O': (57, 26),
    'CHNH': (34, 15),
    'CHNH2': (31, 14),
#    'CHOCH': (114, 53),    #these are oxides, not ethers
#    'CHOCH0': (115, 53),
    'CHS': (104, 48),
#    'COO': (77, 41),
#    'DMF': (72, 39),
#    'DMSO': (68, 35),
#    'DOH': (63, 31),
#    'HCON(CH2)2': (73, 39),
    'I': (64, 32),
#    'MORPH': (105, 49),
#    'NMP': (85, 44),
    'O=COC=O': (117, 54),
    'OH': (15, 5),
    'OH2': (17, 7),
    'SCS': (59, 28),
    'Si': (81, 42),
    'SiH': (80, 42),
    'SiH2': (79, 42),
    'SiH2O': (82, 43),
    'SiH3': (78, 42),
    'SiHO': (83, 43),
    'SiO': (84, 43),
#    'THF': (28, 13),
#    'furfural': (62, 30)
    }

q_r_data = {
    1: (0.848, 0.9011),
    2: (0.54, 0.6744),
    3: (0.228, 0.4469),
    4: (0.0, 0.2195),
    5: (1.176, 1.3454),
    6: (0.867, 1.1167),
    7: (0.988, 1.1173),
    8: (0.676, 0.8886),
    9: (0.485, 0.6605),
    10: (0.4, 0.5313),
    11: (0.12, 0.3652),
    12: (0.968, 1.2663),
    13: (0.66, 1.0396),
    14: (0.348, 0.8121),
    15: (1.2, 1.0),
    16: (1.432, 1.4311),
    17: (1.4, 0.92),
    18: (0.68, 0.8952),
    19: (1.448, 1.6724),
    20: (1.18, 1.4457),
    21: (0.948, 0.998),
    22: (1.728, 1.9031),
    23: (1.42, 1.6764),
    24: (1.188, 1.242),
    25: (1.088, 1.145),
    26: (0.78, 0.9183),
    27: (0.468, 0.6908),
    28: (1.1, 0.9183),
    29: (1.544, 1.5959),
    30: (1.236, 1.3692),
    31: (0.924, 1.1417),
    32: (1.244, 1.4337),
    33: (0.936, 1.207),
    34: (0.624, 0.9795),
    35: (0.94, 1.1865),
    36: (0.632, 0.9597),
    37: (0.816, 1.06),
    38: (2.113, 2.9993),
    39: (1.833, 2.8332),
    40: (1.553, 2.667),
    41: (1.724, 1.8701),
    42: (1.416, 1.6434),
    43: (1.224, 1.3013),
    44: (1.532, 1.528),
    45: (1.264, 1.4654),
    46: (0.952, 1.238),
    47: (0.724, 1.0106),
    48: (1.998, 2.2564),
    49: (1.684, 2.0606),
    50: (1.448, 1.8016),
    51: (2.41, 2.87),
    52: (2.184, 2.6401),
    53: (2.91, 3.39),
    54: (0.844, 1.1562),
    55: (1.868, 2.0086),
    56: (1.56, 1.7818),
    57: (1.248, 1.5544),
    58: (1.104, 1.4199),
    59: (1.65, 2.057),
    60: (1.676, 1.877),
    61: (1.368, 1.651),
    62: (2.484, 3.168),
    63: (2.248, 2.4088),
    64: (0.992, 1.264),
    65: (0.832, 0.9492),
    66: (1.088, 1.292),
    67: (0.784, 1.0613),
    68: (2.472, 2.8266),
    69: (2.052, 2.3144),
    70: (0.724, 0.791),
    71: (0.524, 0.6948),
    72: (2.736, 3.0856),
    73: (2.12, 2.6322),
    74: (1.38, 1.406),
    75: (0.92, 1.0105),
    76: (0.46, 0.615),
    77: (1.2, 1.38),
    78: (1.263, 1.6035),
    79: (1.006, 1.4443),
    80: (0.749, 1.2853),
    81: (0.41, 1.047),
    82: (1.062, 1.4838),
    83: (0.764, 1.303),
    84: (0.466, 1.1044),
    85: (3.2, 3.981),
    86: (2.644, 3.0356),
    87: (1.916, 2.2287),
    88: (2.116, 2.406),
    89: (1.416, 1.6493),
    90: (1.648, 1.8174),
    91: (1.828, 1.967),
    92: (2.1, 2.1721),
    93: (2.376, 2.6243),
    94: (1.248, 1.4515),
    95: (1.796, 2.1905),
    96: (1.488, 1.9637),
    97: (2.428, 2.8589),
    98: (2.12, 2.6322),
    99: (1.812, 2.4054),
    100: (1.904, 2.1226),
    101: (1.592, 1.8952),
    102: (1.368, 1.613),
    103: (1.06, 1.3863),
    104: (0.748, 1.1589),
    105: (2.796, 3.474),
    106: (2.14, 2.8569),
    107: (1.86, 2.6908),
    108: (1.58, 2.5247),
    109: (2.12, 2.6869),
    110: (1.808, 2.4595),
    111: (1.32, 1.5926),
    112: (1.008, 1.3652),
    113: (0.78, 1.1378),
    114: (0.696, 1.1378),
    115: (0.468, 0.9103),
    116: (0.24, 0.6829),
    117: (1.52, 1.7732),
    118: (0.996, 1.3342),
    119: (0.972, 1.3629)}

