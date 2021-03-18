# Dataset Link https://data.humdata.org/dataset/covid-19-mobility-italy
# Italy population from wikipedia
# Italy shapefile from https://www.eea.europa.eu/data-and-maps/data/eea-reference-grids-2/gis-files/italy-shapefile
# https://www4.istat.it/it/archivio/209722
# geojson https://github.com/openpolis/geojson-italy/blob/master/geojson/limits_IT_provinces.geojson
# Covid data per province https://www.kaggle.com/virosky/italy-covid19?select=covid19-ita-province.csv

import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import skmob
import math
import numpy as np
from skmob.models import Gravity, Radiation
import Levenshtein

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


# Read geojson file containing provinces locations
geoJson_Path = open(in_Geojson_Provinces_IT)
gpd_df_geojson = gpd.read_file(geoJson_Path)

# Delete extra columns from geojson dataframe
del gpd_df_geojson['prov_istat_code_num']
del gpd_df_geojson['prov_acr']
del gpd_df_geojson['reg_istat_code_num']
del gpd_df_geojson['reg_istat_code']
del gpd_df_geojson['prov_name']
del gpd_df_geojson['reg_name']
# Dataset Link https://data.humdata.org/dataset/covid-19-mobility-italy
# Italy population from wikipedia
# Italy shapefile from https://www.eea.europa.eu/data-and-maps/data/eea-reference-grids-2/gis-files/italy-shapefile
# https://www4.istat.it/it/archivio/209722
# geojson https://github.com/openpolis/geojson-italy/blob/master/geojson/limits_IT_provinces.geojson

import geopandas as gpd
import pandas as pd
import skmob
import math

##############################################################
#Paths
##############################################################

# INPUTS

# File downloaded from https://github.com/openpolis/geojson-italy/blob/master/geojson/limits_IT_provinces.geojson,
# The file contains information about the locations and ids of Italian provinces
in_Geojson_Provinces_IT = "input\Italy_Provinces_Geojson.json"



# File downloaded from https://data.humdata.org/dataset/covid-19-mobility-italy. The populations for each province were 
# edited from https://www.citypopulation.de/en/italy/admin/
in_Italian_ProvincesID_Population_Path = "input\Italy_ProvincesID_Population.csv"

# File downloaded from https://data.humdata.org/dataset/covid-19-mobility-italy. Contains origin-destination provinces
# from Italy, on a time scale
in_Origin_Destination_Matrix_Path = "input\Italy_origin_destination_matrix.csv"

##############################################################

# OUTPUTS 

# The convered file from the geojson. Contains only the province id and the geometry of the province
out_ProvinceID_Geometry_CSV_Path = "output\Italy_ProvinceID_Geometry.csv"

# Merged file which contains the Italian provinces along with population and ids
out_ProvinceID_Geometry_Population_Path = "output\Italy_ProvinceID_Geometry_Population.csv"

# Path of the origin-destination Matrix created by Python
out_Origin_Dest_Flows_Path = "output\Italy_Origin_Destination_Flows_Date.csv"
out_Origin_Dest_Flows_Mini_Path = "output\Italy_Origin_Destination_Flows_Date_Mini.csv"
#############################################################


# Read geojson file containing provinces locations
geoJson_Path = open(in_Geojson_Provinces_IT)
gpd_df_geojson = gpd.read_file(geoJson_Path)

# Delete extra columns from geojson dataframe
del gpd_df_geojson['prov_istat_code_num']
del gpd_df_geojson['prov_acr']
del gpd_df_geojson['reg_istat_code_num']
del gpd_df_geojson['reg_istat_code']
del gpd_df_geojson['prov_name']
del gpd_df_geojson['reg_name']

# save the resulting dataframe in a csv file
gpd_df_geojson.to_csv(out_ProvinceID_Geometry_CSV_Path, index = False)


# Read the provinces with population file
it_dtset_file = open(in_Italian_ProvincesID_Population_Path)
pd_df_ProvID_Population = pd.read_csv(it_dtset_file)

# Convert the geopandas to pandas dataframe, in order to merge it with the population dataframe
pd_Geojson = pd.DataFrame(gpd_df_geojson)

# Merge dataframes based on province id
pd_Geojson['prov_istat_code']=pd_Geojson['prov_istat_code'].astype(int)
df_Geometry_ProvID_Population = pd.merge(pd_Geojson,pd_df_ProvID_Population,on='prov_istat_code')
df_Geometry_ProvID_Population.columns = ['tile_ID', 'geometry', 'index', 'province_code', 'province_name', 'population']


# Save the resulting dataframe in a file
df_Geometry_ProvID_Population = df_Geometry_ProvID_Population.sort_values(by='tile_ID')
print(df_Geometry_ProvID_Population.head())
df_Geometry_ProvID_Population.to_csv(out_ProvinceID_Geometry_Population_Path, index = False)


# Convert to Origin-Destination Matrix

df_Origin_Destination = pd.read_csv(in_Origin_Destination_Matrix_Path)
df_It_Prov_Geom_Pop = pd.read_csv(out_ProvinceID_Geometry_Population_Path)

# convert column types
df_Origin_Destination['origin']=df_Origin_Destination['origin'].astype(int)
df_Origin_Destination['destination']=df_Origin_Destination['destination'].astype(int)

# rename columns
temp_csv_string = "flow,origin,destination,date\n"


################################################################
# Create Origin Destination CSV file
index = 0 
temp_csv_string = "flow,origin,destination,date\n"
for index, row in df_Origin_Destination.iterrows():
    # print("Finished row "+str(index))
    index += 1

    popRow = df_It_Prov_Geom_Pop.loc[df_It_Prov_Geom_Pop['tile_ID'] == row[0]]
    prov_population = popRow['population'].item()
    for y in range(len(row[2:])):
        flows = math.ceil(row[y+2]*prov_population)
        if (flows!=0):
            temp_csv_string += str(flows)+','+str(row[0])+','+str(row[1])+','+str(df_Origin_Destination.columns[y+2])+'\n'


# Write to file
Origin_Destination_File = open(out_Origin_Dest_Flows_Path, "w")
Origin_Destination_File.write(temp_csv_string.replace(".0",""))
Origin_Destination_File.close()
################################################################


# make tesselation work
tessellation = gpd.GeoDataFrame(df_Geometry_ProvID_Population, geometry=df_Geometry_ProvID_Population.geometry)

del tessellation['index']
print(tessellation.head())
# print (gdf_Geometry_ProvID_Population.head())

# FLOW DATAFRAME
fdf_All_Flows = skmob.FlowDataFrame.from_file(out_Origin_Dest_Flows_Path,
                                    tessellation=tessellation,
				                    tile_id='tile_ID',
                                    datetime = 'date',
                                    origin = 'origin',
                                    destination = 'destination',
                                    flow = 'flow',
				                    sep=",")

print(fdf_All_Flows.head())

# # Plot flow dataframe
# fdf_All_Flows.plot_flows(flow_color='red')
# save the resulting dataframe in a csv file
gpd_df_geojson.to_csv(out_ProvinceID_Geometry_CSV_Path, index = False)


# Read the provinces with population file
it_dtset_file = open(in_Italian_ProvincesID_Population_Path)
pd_df_ProvID_Population = pd.read_csv(it_dtset_file)

# Convert the geopandas to pandas dataframe, in order to merge it with the population dataframe
pd_Geojson = pd.DataFrame(gpd_df_geojson)

# Merge dataframes based on province id
pd_Geojson['prov_istat_code']=pd_Geojson['prov_istat_code'].astype(int)
df_Geometry_ProvID_Population = pd.merge(pd_Geojson,pd_df_ProvID_Population,on='prov_istat_code')
df_Geometry_ProvID_Population.columns = ['tile_ID', 'geometry', 'index', 'province_code', 'province_name', 'population']


# Save the resulting dataframe in a file
df_Geometry_ProvID_Population = df_Geometry_ProvID_Population.sort_values(by='tile_ID')
print(df_Geometry_ProvID_Population.head())
df_Geometry_ProvID_Population.to_csv(out_ProvinceID_Geometry_Population_Path, index = False)


# Convert to Origin-Destination Matrix

df_Origin_Destination = pd.read_csv(in_Origin_Destination_Matrix_Path)
df_It_Prov_Geom_Pop = pd.read_csv(out_ProvinceID_Geometry_Population_Path)

# convert column types
df_Origin_Destination['origin']=df_Origin_Destination['origin'].astype(int)
df_Origin_Destination['destination']=df_Origin_Destination['destination'].astype(int)

# rename columns
temp_csv_string = "flow,origin,destination,date\n"


################################################################
# Create Origin Destination CSV file
index = 0 
temp_csv_string = "flow,origin,destination,date\n"
for index, row in df_Origin_Destination.iterrows():
    # print("Finished row "+str(index))
    index += 1

    popRow = df_It_Prov_Geom_Pop.loc[df_It_Prov_Geom_Pop['tile_ID'] == row[0]]
    prov_population = popRow['population'].item()
    for y in range(len(row[2:])):
        flows = math.ceil(row[y+2]*prov_population)
        if (flows!=0):
            temp_csv_string += str(flows)+','+str(row[0])+','+str(row[1])+','+str(df_Origin_Destination.columns[y+2])+'\n'


# Write to file
Origin_Destination_File = open(out_Origin_Dest_Flows_Path, "w")
Origin_Destination_File.write(temp_csv_string.replace(".0",""))
Origin_Destination_File.close()
################################################################


# make tesselation work
tessellation = gpd.GeoDataFrame(df_Geometry_ProvID_Population, geometry=df_Geometry_ProvID_Population.geometry, crs = "WGS84")

# dokimes
# del tessellation['index']
print(tessellation.head())
# print (gdf_Geometry_ProvID_Population.head())

# FLOW DATAFRAME
fdf_All_Flows = skmob.FlowDataFrame.from_file(out_Origin_Dest_Flows_Path,
                                    tessellation=tessellation,
				                    tile_id='tile_ID',
                                    datetime = 'date',
                                    origin = 'origin',
                                    destination = 'destination',
                                    flow = 'flow',
				                    sep=",")

print(fdf_All_Flows.head())


# ################################################################
# # Gravity model of human mobility


# print("Going to calculate migration flows based on a Gravity model")

# fdf = fdf_All_Flows
# print(tessellation.head())

# print (fdf.head())

# tot_outflows = fdf[fdf['origin'] != fdf['destination']].groupby(by='origin', axis=0)['flow'].sum().fillna(0).values
# tessellation['tot_outflow'] = tot_outflows
# print(tessellation.head())

# # instantiate a singly constrained Gravity model

# gravity_singly = Gravity(gravity_type='singly constrained')
# print(gravity_singly)


# np.random.seed(0)

# synth_fdf = gravity_singly.generate(tessellation,
#                                    tile_id_column='tile_ID',
#                                    tot_outflows_column='tot_outflow',
#                                    relevance_column= 'population',
#                                    out_format='flows')

# print(synth_fdf.head())

# # fit the parameters of the Gravity model from real fluxes

# gravity_singly_fitted = Gravity(gravity_type='singly constrained')

# print(gravity_singly_fitted)

# gravity_singly_fitted.fit(fdf, relevance_column='population')

# print(gravity_singly_fitted)

# np.random.seed(0)

# synth_fdf_fitted = gravity_singly_fitted.generate(tessellation,
#                                                         tile_id_column='tile_ID',
#                                                         tot_outflows_column='tot_outflow',
#                                                         relevance_column= 'population',
#                                                         out_format='flows')


# print(synth_fdf_fitted.head())

# # ################################################################

# # Radiation model for human migration

# print ("Radiation model for human migration")

# fdf = fdf_All_Flows
# print("Printing tesselation \n")
# print(tessellation.head())
# print(tessellation.geometry.count())

# print("Printing fdf \n")
# print (fdf.head())
# print(fdf.flow.count())
# fdf.flow.count()

# tot_outflows = fdf[fdf['origin'] != fdf['destination']].groupby(by='origin', axis=0)['flow'].sum().fillna(0).values
# tessellation['tot_outflow'] = tot_outflows
# print(tessellation.head())

# np.random.seed(0)
# radiation = Radiation()
# rad_flows = radiation.generate(tessellation, tile_id_column='tile_ID',  tot_outflows_column='tot_outflow', relevance_column='population', out_format='flows_sample')
# print("Now I'ma print the head of the radiation flows")
# print(rad_flows.flow.count())
# print(rad_flows.head())
