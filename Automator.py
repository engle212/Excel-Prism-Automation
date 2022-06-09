import csv
import os

inDir = 'Input Files'
outDir = 'Output Files'
varList = ['ppt', 'temp_low', 'temp_high']

if not os.path.exists(outDir):
    # create output directory
    os.mkdir(outDir)
    print('[output directory created]')

for var in varList:
    # create/open and populate respective file

    outFileName = 'NEW_' + var + '_00_20.csv'
    outFilePath = os.path.join(outDir, outFileName)

    # list stores data across input files to be put into output file
    list = [['YEAR', 'DOY', 'Date']]
    list.extend([[], [], []])

    # open current file
    with open(outFilePath, 'w', newline='') as outFile:
        outWriter = csv.writer(outFile)

        print(var + ' csv output: [in progress]')

        # iterate through input files (located in 'Input Files' folder)
        for inFileName in os.listdir(inDir):
            inFilePath = os.path.join(inDir, inFileName)

            with open(inFilePath, 'r', newline='') as inFile:
                inReader = csv.reader(inFile)

                # skip 11 rows to get to data
                for n in range(11):
                    next(inReader)

                checkLoc = True
                col = varList.index(var) + 5 # column where info is stored
                doy = 1
                outCol = 4 # column where data is to be outputted

                # load contents of file into data list
                for row in inReader:
                    # check if row is blank
                    if row:
                        # take contents of each row and add to list
                        name = row[0]
                        date = row[4]
                        year = date.split('-')[0] # take year from date
                        ppt = row[col]

                        # check if a new location column needs to be created
                        if name not in list[0]:
                            # add new column
                            list[0].append(name)
                            list.append([])

                        # check if new year is started to reset DOY
                        if year not in list[1]:
                            doy = 1 # reset DOY

                        # check if date has already been added
                        if date not in list[3]:
                            # add row of date info if not added
                            list[1].append(year)
                            list[2].append(doy)
                            list[3].append(date)


                        outCol = list[0].index(name) + 1 # set column to output

                        # check if data has already been added
                        if not ((date in list[3]) and (len(list[outCol]) >= len(list[3]))):
                            list[outCol].append(str(ppt)) # extract data into list

                        doy += 1 # increment DOY

        numOfColumns = len(list[0])
        numOfRows = len(list[1])

        outWriter.writerow(list[0]) # write header row to output file

        # iterate through data and write to output file row-by-row
        for i in range(numOfRows):
            rowList = []
            for j in range(1, numOfColumns + 1):
                rowList.append(list[j][i])
            outWriter.writerow(rowList)

        print(var + ' csv output: [complete]')
