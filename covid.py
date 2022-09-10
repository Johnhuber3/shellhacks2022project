import pandas as pd;
import json;

# read csv of fullGroup
fullGroup = pd.read_csv('./data/full_grouped.csv');

# condense data to Date, Country, Confirmed 
condensed = pd.DataFrame(fullGroup, columns=['Date', 'Country/Region', 'Confirmed', 'Deaths']);

# filtered to only G19 countries
G19 = ['Argentina', 'Australia', 'Brazil', 'Canada', 'China', 'France', 'Germany', 'India', 'Indonesia', 'Italy', 'Japan', 'South Korea', 'Mexico', 'Russia', 'Saudi Arabia', 'South Africa', 'Turkey', 'United Kingdom', 'US']
df = pd.DataFrame(condensed.loc[condensed['Country/Region'].isin(G19)]);
# make dataframe a dictionary
g19Dict = df.to_dict();

# save to JSON File
with open('untransformedData.json', 'w') as f: 
    json.dump(g19Dict, f, ensure_ascii=False, indent=4);

