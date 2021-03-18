# Dataset Link https://data.humdata.org/dataset/covid-19-mobility-italy
# Italy population from wikipedia
# Italy shapefile from https://www.eea.europa.eu/data-and-maps/data/eea-reference-grids-2/gis-files/italy-shapefile
# https://www4.istat.it/it/archivio/209722
# geojson https://github.com/openpolis/geojson-italy/blob/master/geojson/limits_IT_provinces.geojson
# Covid data per province https://www.kaggle.com/virosky/italy-covid19?select=covid19-ita-province.csv

import pandas as pd
import math
import Levenshtein as lv
import timeit
from decimal import *

##############################################################
#Paths
##############################################################

# INPUTS

# File downloaded from https://github.com/openpolis/geojson-italy/blob/master/geojson/limits_IT_provinces.geojson,
# The file contains information about the locations and ids of Italian provinces
in_Geojson_Provinces_IT = "input\\Italy_Provinces_Geojson.json"



# File downloaded from https://data.humdata.org/dataset/covid-19-mobility-italy. The populations for each province were 
# edited from https://www.citypopulation.de/en/italy/admin/
in_Italian_ProvincesID_Population_Path = "input\\Italy_ProvincesID_Population.csv"

# File downloaded from https://data.humdata.org/dataset/covid-19-mobility-italy. Contains origin-destination provinces
# from Italy, on a time scale
in_Origin_Destination_Matrix_Path = "input\\Italy_origin_destination_matrix.csv"

##############################################################

# OUTPUTS 

# The convered file from the geojson. Contains only the province id and the geometry of the province
out_ProvinceID_Geometry_CSV_Path = "output\\Italy_ProvinceID_Geometry.csv"

# Merged file which contains the Italian provinces along with population and ids
out_ProvinceID_Geometry_Population_Path = "output\\Italy_ProvinceID_Geometry_Population.csv"

# Path of the origin-destination Matrix created by Python
out_Origin_Dest_Flows_Path = "output\\Italy_Origin_Destination_Flows_Date.csv"
out_Origin_Dest_Flows_Mini_Path = "output\\Italy_Origin_Destination_Flows_Date_Mini.csv"
#############################################################

df1 = pd.read_csv(out_Origin_Dest_Flows_Path)
# print(df1.head())
df1_part = df1[df1['date']=="01-03-20"]
for x in range(10):
    df2_part = df1[df1['date']=="{0:0=2d}".format(x+2)+"-03-20"]
    start = timeit.default_timer()
    LOD,NLOD = lv.calculateLOD(df1_part,df2_part)
    stop = timeit.default_timer()
    # print('Time: ', stop - start)  
    mNLOD = lv.calculateMean(NLOD)
    mLOD  = lv.calculateMean(LOD)
    # print(mNLOD)
    print("From 01-03-20 to "+"{0:0=2d}".format(x+1)+"-03-20:","\tmean_NLOD:",mNLOD,"\tmean_LOD:",mLOD)