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
outputDirectory = "Output"
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

##########################################################


