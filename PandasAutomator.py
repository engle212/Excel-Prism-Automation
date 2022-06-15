import os
import pandas as pd
#pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

inDir = 'Input Files'
outDir = 'Output Files'
varList = ['ppt', 'temp_low', 'temp_high']

if not os.path.exists(outDir):
    # create output directory
    os.mkdir(outDir)
    print('[output directory created]')


for var in varList:
    outFileName = 'NEW_' + var + '_00_20.csv'
    outFilePath = os.path.join(outDir, outFileName)

    # create outDF for current var
    outDF = pd.DataFrame(columns=['YEAR', 'DOY', 'Date'])
    outList = []
    
    if var == 'ppt':
        colName = 'ppt (mm)'
    elif var == 'temp_low':
        colName = 'tmin (degrees C)'
    else:
        colName = 'tmax (degrees C)'

    # create inDF for each input file
    for inFileName in os.listdir(inDir):
        outCur = pd.DataFrame(columns=['YEAR', 'DOY', 'Date'])

        inFilePath = os.path.join(inDir, inFileName)
        inDF = pd.read_csv(inFilePath, skiprows=10)
        inDF.dropna(how="all", inplace=True) # Remove empty rows
        # read each input file into outDF
        inDF.drop_duplicates(subset=['Name', 'Date'], inplace=True)
        inDF.reset_index(drop=True, inplace=True)


        outCur['Date'] = inDF.iloc[:, 4].drop_duplicates(inplace=False)

        outCur[['YEAR', 'month-day']] = inDF.iloc[:, 4].drop_duplicates(inplace=False).str.split('-', n=1, expand=True)
        outCur.drop('month-day', axis=1, inplace=True)

        outCur['DOY'] = inDF.drop_duplicates(subset='Date', inplace=False).index
        outCur['DOY'] = outCur['DOY'] + 1

        names = inDF.iloc[:, 0].drop_duplicates(inplace=False)
        names.reset_index(drop=True, inplace=True)

        for name in names:
            column = pd.Series(inDF.loc[inDF['Name'] == name, colName]).to_frame()
            column.rename(columns = {colName : name}, inplace = True)
            # tack on new column and data
            outCur = pd.concat([outCur, column.reset_index(drop=True)], axis=1, ignore_index=False)

        outList.append(outCur)
    outDF = pd.concat(outList, ignore_index=True)

    # write outDF to CSV file
    outDF.to_csv(outFilePath, index=False)
