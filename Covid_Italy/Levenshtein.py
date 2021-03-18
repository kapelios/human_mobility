#  Algorithm from paper:
#  A novel approach for the structural comparison of origin-destination matrices: Levenshtein distance

import pandas as pd
import math

# Edit the first and last column of the L matrix 
def printTable(T):
    for r in T:
        for c in r:
            print(c,end = "\t")
        print()

def calculateMean(list):
    return sum(list)/len(list)

def calculateLOD(df1,df2):
    # Convert first Dataframe
    od_df = df1.pivot_table(values='flow', index="origin", columns='destination',
            fill_value=0)
    maxValue1= max(df1.origin.max(), df1.destination.max())
    r2x = od_df

    # Convert second Dataframe
    od_df = df2.pivot_table(values='flow', index="origin", columns='destination',
            fill_value=0)
    maxValue2= max(df2.origin.max(), df2.destination.max())
    r2y = od_df
    maxValue = max(maxValue1, maxValue2)
    # i = row
    # j = column
    LOD = [0 for x in range(maxValue)]
    NLOD = [0 for x in range(maxValue)]
    for N in range(1,maxValue+1):
        try:
            r2x_maxRow = r2x.loc[N]
            r2x_maxRow = r2x_maxRow.sort_values(ascending=False)
        except:
            r2x_maxRow = 0
        try:
            r2y_maxRow = r2y.loc[N]
            r2y_maxRow = r2y_maxRow.sort_values(ascending=False)
        except:
            r2y_maxRow = 0

        sumx = 0
        sumy = 0
        # Assign cumulative flows
        L = [[0 for x in range(maxValue+1)] for x in range(maxValue+1)]
        for x in range(1,maxValue+1):
            try:
                sumx += r2x_maxRow[r2x_maxRow.index[x-1]]
            except:
                sumx = sumx

            try:
                sumy += r2y_maxRow[r2y_maxRow.index[x-1]]
            except:
                sumy = sumy
            
            L[0][x] = sumx
            L[x][0] = sumy
        for row in range(1, maxValue+1):
            for column in range(1,maxValue+1):
                try:
                    Dx = r2x_maxRow.index[column-1]
                    Ax = r2x_maxRow[Dx]
                except:
                    Dx = 0
                    Ax = 0
                try:
                    Dy = r2y_maxRow.index[row-1]
                    Ay = r2y_maxRow[Dy]
                except:
                    Dy = 0
                    Ay = 0
                if (Dx == Dy):
                    Cost = abs(Ax - Ay)
                else:
                    Cost = abs(Ax + Ay)
                L[row][column] = min(L[row-1][column]+Ay, L[row][column-1]+Ax,L[row-1][column-1]+Cost)
        # Calculate LOD, NLOD
        LOD[N-1]    =   L[maxValue][maxValue]
        if (L[0][maxValue]+L[maxValue][0] != 0):
            NLOD[N-1]   =   LOD[N-1]/(L[0][maxValue]+L[maxValue][0])
        else:
            NLOD[N-1]   =   0
    return (LOD,NLOD)


def calculateLOD_Common (df1,df2):
    new_df = pd.merge(df1, df2,  how='inner', left_on=['origin','destination'], right_on =['origin','destination'])
    new_df = new_df.drop(columns = ['flow_x']).rename(columns = {'flow_y': 'flow'})
    LOD,NLOD = calculateLOD(df1, new_df)
    return (LOD,NLOD)

def calculateLOD_Common_v2 (df1,df2):
    # delete rows for which we have no information
    new_df = pd.merge(df1, df2,  how='inner', left_on=['origin','destination'], right_on =['origin','destination'])
    new_df = new_df.drop(columns = ['flow_x']).rename(columns = {'flow_y': 'flow'})
    tot_outflows = new_df[new_df['origin'] != new_df['destination']].groupby(by='origin', axis=0)['flow'].sum().fillna(0).values
    # print(tot_outflows)
    # print("For DF2")
    # tot_outflows = df2[df2['origin'] != df2['destination']].groupby(by='origin', axis=0)['flow'].sum().fillna(0).values
    # print(tot_outflows)
    # Total1 = df1['flow'].sum()
    Total2 = df2['flow'].sum()
    Total3 = new_df['flow'].sum()
    
    multiplier = Total2 / Total3

    new_df['flow'] = (multiplier * new_df['flow']).astype(int)
    
    # print("Added flows")
    # Total3 = new_df['flow'].sum()
    # Total1 = df1['flow'].sum()
    # Total2 = df2['flow'].sum()
    # percentage = 1-1*Total3/Total2,2
    # print(Total1,Total2)
    # print("Df1 flows:\t",Total1)
    
    # print("Total synth. flows before cropping:\t",Total2)
    # print("Total synth. flows after cropping:\t",Total3)
    # print("Lost ",round(100-100*Total3/Total2,2),"% of flows", sep = "")
    LOD,NLOD = calculateLOD(df1, new_df)
    return (LOD,NLOD)
    # tot_outflows = new_df[new_df['origin'] != new_df['destination']].groupby(by='origin', axis=0)['flow'].sum().fillna(0).values
    # print(tot_outflows)

def calculateLOD_Common_v3 (df1,df2):
    # Merge dataframes
    new_df = pd.merge(df1, df2,  how='inner', left_on=['origin','destination'], right_on =['origin','destination'])
    new_df = new_df.drop(columns = ['flow_x']).rename(columns = {'flow_y': 'flow'})

    # Calculate outflows
    tot_outflows = new_df[new_df['origin'] != new_df['destination']].groupby(by='origin', axis=0)['flow'].sum().fillna(0).values
    tot_outflows2 = df2[df2['origin'] != df2['destination']].groupby(by='origin', axis=0)['flow'].sum().fillna(0).values
    tot_outflows3_mult = (tot_outflows2 / tot_outflows)

    # Create origin multiplier dataframe
    new_df_my = new_df['origin'].unique()
    df = pd.DataFrame({'origin':new_df_my,'multiplier':tot_outflows3_mult})

    # multiply dataframe with values
    new_df2 = pd.merge(new_df, df,  how='inner', left_on=['origin'], right_on =['origin'])
    new_df2['flow'] = (new_df2['flow'] * new_df2['multiplier']).astype(int)
    new_df2 = new_df2.drop(columns = ['multiplier'])
    # tot_outflows2 = new_df2[new_df2['origin'] != new_df2['destination']].groupby(by='origin', axis=0)['flow'].sum().fillna(0).values

    LOD,NLOD = calculateLOD(df1, new_df2)
    return (LOD,NLOD)

# file1 = "output\\aggregated_flows\\2020_01_20_2020_01_26_aggregated.csv"
# file2 = "hello_january.csv"

# df1 = pd.read_csv(file1)
# df2 = pd.read_csv(file2)

# print("mean nLOD is...:")
# LOD,NLOD = calculateLOD(df1,df2)
# mLOD = calculateMean(NLOD)
# print("Without optimisation:",mLOD)

# LOD,NLOD = calculateLOD_Common(df1,df2)
# mLOD = calculateMean(NLOD)
# print("After removing extra flows:",mLOD)

# LOD,NLOD = calculateLOD_Common_v3(df1,df2)
# mLOD = calculateMean(NLOD)
# print("After removing extra flows AND restoring lost flows:",mLOD)