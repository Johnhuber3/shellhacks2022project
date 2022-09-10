## By Zain E. Yousaf Fuentes // zeyf

import json;

## load the dataframe dumped data
jsonDataSet = json.load(open("data.json", "r"));

## Clean the pandas JSON dumped data into columnKey and column data arrays in a tuple pair
jsonDataSetKV = [ (columnKey, [ v for k,v in columnData.items() ]) for columnKey, columnData in jsonDataSet.items() ];

## get size of data set
entries = len(jsonDataSetKV[0][1]);

## get the column keys
columnKeys = [ k for k,v in jsonDataSetKV ];

## initialize the final dictionary that will be converted to a JSON file
formattedDataSet = { "unstructuredDateSortedData": [  ], "structuredDateGroupedData": [  ] };

## initialize the dateSet to allow to be able to group all same dates into the same arrays (considering data is already in-order by date)
dateSet = set();

## iterate over all of the data entries to recreate the data points
for x in range(entries):
    
    ## generate the dictionary for the current entry's row data by iterating over all columnKeys and mapping to the specific information of a entry per column
    dataPoint = { columnKeys[y]: jsonDataSetKV[y][1][x] for y in range(len(columnKeys)) };

    ## split the date by - to reformat it from YYYY-MM-DD to MM-DD-YYYY
    dateSplit = dataPoint["Date"].split("-");
    dataPoint["Date"] = "-".join([ dateSplit[1],dateSplit[2],dateSplit[0] ]);

    ## add the data point into the unstructured date sorted data set
    formattedDataSet["unstructuredDateSortedData"].append(dataPoint);

    ## if we are at a new date, we are at the beginning of a "block" of values (as they are already sorted by date)
    ## account for the date (add it into the set) and add a new list to signify a new date day collection
    if dataPoint["Date"] not in dateSet:
        dateSet.add(dataPoint["Date"]);
        formattedDataSet["structuredDateGroupedData"].append([  ]);

    ## reformat the US across all data points to United States instead of US
    if dataPoint["Country/Region"] == "US":
        dataPoint["Country/Region"] = "United States";

    ## add the current data point to the end of the latest day as we are in-order by date
    formattedDataSet["structuredDateGroupedData"][-1].append(dataPoint);


## initalize the list to reformat the data by tuples
newDataFormat = [];

## iterate over the processed data points that are grouped by day
for x in range(len(formattedDataSet["structuredDateGroupedData"])):
    
    ## tracks the total deaths and the confirmed cases on the current day after iterating over all elements on a given day
    totalDayDeaths, totalDayConfirmed = 0, 0;
    
    ## iterate over all countries on a given date to have localized data point information as the data set is cumulative
    for y in range(len(formattedDataSet["structuredDateGroupedData"][x])):
        ## if we are at the very first date in the data set
        if x == 0:
            ## seed the dayOfConfirmed and dayOfDeaths to the very first value since there is no previous to compare or calculate from
            formattedDataSet["structuredDateGroupedData"][x][y]["dayOfConfirmed"] = formattedDataSet["structuredDateGroupedData"][x][y]["Confirmed"];
            formattedDataSet["structuredDateGroupedData"][x][y]["dayOfDeaths"] = formattedDataSet["structuredDateGroupedData"][x][y]["Deaths"];
        
        ## perform a day wise calculation by comparing the previous day's data on confirmed cases and also deaths
        else:
            formattedDataSet["structuredDateGroupedData"][x][y]["dayOfConfirmed"] = formattedDataSet["structuredDateGroupedData"][x][y]["Confirmed"] - formattedDataSet["structuredDateGroupedData"][x-1][y]["Confirmed"];
            formattedDataSet["structuredDateGroupedData"][x][y]["dayOfDeaths"] = formattedDataSet["structuredDateGroupedData"][x][y]["Deaths"] - formattedDataSet["structuredDateGroupedData"][x-1][y]["Deaths"];
        
        ## create a local cumulative of the deaths and confirmed cases of all G19 countries on a given day
        totalDayDeaths += formattedDataSet["structuredDateGroupedData"][x][y]["dayOfDeaths"];
        totalDayConfirmed += formattedDataSet["structuredDateGroupedData"][x][y]["dayOfConfirmed"];

    ## add the tuple with the total number of deaths per day, the total number of confirmed cases per day, and the data set across all of the G19 countries on a given day
    newDataFormat.append((totalDayDeaths, totalDayConfirmed, formattedDataSet["structuredDateGroupedData"][x]));

## reformat the data points in the data set
for x in range(len(formattedDataSet["structuredDateGroupedData"])):
    
    ## destructure the local day data
    totalDayDeaths, totalDayConfirmed, countrySpread = newDataFormat[x];
    countrySpreadCopy = countrySpread[::];
    countrySpread.sort(key=lambda countryData: countryData["Confirmed"]);
    # reformat data point with new information
    formattedDataSet["structuredDateGroupedData"][x] = {
        "totalDayDeaths": totalDayDeaths,
        "totalDayConfirmed": totalDayConfirmed,
        "countrySpread" : [ countrySpread ]
    };
    
## write the file to a json
with open("transformedData.json", "w") as f:
    json.dump(formattedDataSet, f, ensure_ascii=False, indent=4);