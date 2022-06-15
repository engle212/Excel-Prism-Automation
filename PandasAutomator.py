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

        for name in inDF.iloc[:, 0].drop_duplicates(inplace=False):
            column = inDF.loc[inDF['Name'] == name, 'ppt (mm)']
            #print(inDF.iloc[inDF.index[inDF['Name'] == name], 5])
            #print(name + ' ' + str(len(inDF.loc[inDF['Name'] == name, 'ppt (mm)'])))
            # new column, fill with data
            outCur[name] = column
            # try concatenation again
            #outCur = pd.concat([outCur, column], axis=1)

        print(outCur)
        outList.append(outCur)
    outDF = pd.concat(outList, ignore_index=True)
    print(outDF)
    print(" ")

#inDF = pd.read_csv('PRISM_ppt_tmin_tmax_stable_4km_20080101_20081231.csv', skiprows=10)


#outDF = pd.DataFrame(columns=['YEAR', 'DOY', 'Date'])
