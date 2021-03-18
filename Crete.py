# DATASET LINK: http://www.mysignals.gr/research.php
# Relative dataset path dataset\dataset\measurementsGSM_alldata_cells_6065x
import skmob
import pandas as pd
from skmob.measures.individual import *
import folium 
import geopandas as gpd
from skmob.privacy import attacks
from skmob.models.markov_diary_generator import MarkovDiaryGenerator
from skmob.preprocessing import filtering, compression, detection, clustering


dataset = "Input\\Dataset.csv"
df = pd.read_csv(dataset, sep=",", header = 0)

# names = ['timestamp','iPhoneUID','dt1','dt2','dt3','dt4','dt5','rssi','rssi1','rssi2','rssi3','rssi4','rssi5','latitude','longitude','finalLatitude','finalLongitude','horizontalAccuracy','isMoving','txPower','cellID','LAC','MNC','ARFCN','freq_dlink','freq_uplink']# dsl_df = distance_straight_line(tdf)
# dsl_rog = radius_of_gyration(tdf)
# dsl_lf = location_frequency(tdf)
# dsl_jl = jump_lengths(tdf)
# dsl_nol = number_of_locations(tdf)
# print(dsl_df.head())
# print(dsl_rog.head())
# print(dsl_lf.head())
# print(dsl_jl.head())
# print(dsl_nol.head())
# print(hl_df.head())


# add all trajectories in a dataframe
tdf = skmob.TrajDataFrame(df, latitude='latitude', longitude='longitude', datetime='timestamp', user_id='iPhoneUID')

print(tdf.head())

##########################################################
# Data preprocessing

# Filter the traj dataframe by removing consecutive locations with speed > 200 kmh
filtered_tdf = filtering.filter(tdf, max_speed_kmh = 200)
num_deleted_points = len(tdf) - len(filtered_tdf)
print("Deleted",num_deleted_points,"out of",len(tdf))

filtered_tdf = filtered_tdf[filtered_tdf['uid']!="510635002cb29804d54bff664cab52be"]

##########################################################

# # Calculate home locations and display them in a folium map
# # Start of the night is at 3.00, end of the night is at 5.00
# hl_df = home_location(tdf, start_night = "03:00", end_night = "05:00")


# # print the home locations on a map
# chania_homes_map = folium.Map(location=[35.5,24.0], zoom_start = 11)
# for index, row in hl_df.iterrows():
#     folium.Marker( location=[ row[1], row[2] ], fill_color='#43d9de', radius=8, popup=row[0]).add_to( chania_homes_map )
# chania_homes_map

##########################################################

# print(hl_df.head())
# gdf = gpd.GeoDataFrame(
#     hl_df, geometry=gpd.points_from_xy(hl_df.lat, hl_df.lng))

# tdf.plot_trajectory(zoom=12, weight=3, opacity=0.9, tiles='Stamen Toner')

##########################################################
# #Calculate privacy attack

# at = attacks.HomeWorkAttack()
# r = at.assess_risk(tdf)

# print(r)

# at = attacks.LocationSequenceAttack(knowledge_length = 2)
# r = at.assess_risk(tdf)

# print(r)

##########################################################

# # Markov Diary generator
# # Gonna calculate locations based on a Markov generator

# # filtered_tdf is already calculated

# # Trajectory compression.
# # Reduce the number of points in a trajectory for each individual in a TrajDataFrame. 
# # All points within a radius of spatial_radius_km kilometers from a given initial point are compressed into 
# # a single point that has the median coordinates of all points and the time of the initial point 
# ctdf = compression.compress(filtered_tdf)


# # Stops detection.
# # Detect the stops for each individual in a TrajDataFrame. 
# # A stop is detected when the individual spends at least minutes_for_a_stop minutes 
# # within a distance stop_radius_factor * spatial_radius km from a given trajectory point. 
# # The stop’s coordinates are the median latitude and longitude values 
# # of the points found within the specified distance 
# stdf = detection.stops(filtered_tdf)

# # Clustering of locations.
# # Cluster the stops of each individual in a TrajDataFrame. 
# # The stops correspond to visits to the same location at different times, 
# # based on spatial proximity [RT2004]. The clustering algorithm used is DBSCA
# cstdf = clustering.cluster(stdf)

# mdg = MarkovDiaryGenerator()

# # Train the markov mobility diary from real trajectories.
# mdg.fit(cstdf, 10, lid='cluster')

# start_time = pd.to_datetime('2013/01/01 08:00:00')

# # Start the generation of the mobility diary.
# diary = mdg.generate(1000, start_time)

# print(diary.head())
# print(diary)

##########################################################