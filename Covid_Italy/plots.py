
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import skmob
import math
import datetime as dt

in_Covid_Data = "input\\Italy_Covid_Data_Province.csv"
in_Origin_Dest_Flows_Path = "output\\Italy_Origin_Destination_Flows_Date.csv"


# In and out of Lodi before and after lockdown
od_df = pd.read_csv(in_Origin_Dest_Flows_Path)
# Make sure date is registered correctly
startDate = dt.date(2020,2,10)
endDate = dt.date(2020,2,28)
od_df['date'] = od_df['date'].astype('datetime64[ns]')
od_df['date'] = pd.to_datetime(od_df['date']).dt.date

mask = (od_df['date']>=startDate) & (od_df['date']<endDate)
mask2 = (od_df['origin']==98) & (od_df['destination']!=98)
lodi_out = od_df.loc[mask].loc[mask2].sort_values(by='date')

lodi_out = od_df.loc[mask].loc[mask2].groupby(['date']).sum()[["flow"]]
ax = lodi_out.plot(y = "flow", xlabel = "Days of Month")
ax.legend(['Outcoming Flows from Lodi'])
# plt.show()
print(lodi_out.head())
# plt.show()

mask2 = (od_df['destination']==98) & (od_df['origin']!=98)
lodi_in = od_df.loc[mask].loc[mask2].sort_values(by='date')
# print(lodi_in.head(100))
lodi_in = od_df.loc[mask].loc[mask2].groupby(['date']).sum()[["flow"]]
bx = lodi_in.plot(y = "flow", xlabel = "Days of Month", ax = ax)
bx.legend(['Outcoming flows','Incoming flows','Αυστηροποίηση'])
# xposition = [dt.date(2020,2,10])
plt.axvline(x='2020-2-21',linewidth =1, color='r', linestyle='--', label = "Αυστηροπ. μέτρων")

plt.xticks(rotation = 90)
plt.tight_layout()
print(lodi_in.head())
plt.show()