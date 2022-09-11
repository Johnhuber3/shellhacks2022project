## by Zain E. Yousaf Fuentes // zeyf
import pandas as pd;
import json;

G19 = ["Argentina", "Australia", "Brazil", "Canada", "China", "France", "Germany", "India", "Indonesia", "Italy", "Japan", "South Korea", "Mexico", "Russia", "Saudi Arabia", "South Africa", "Turkey", "United Kingdom", "US"]
df = pd.read_csv("./data/covid_19_clean_complete.csv");
filteredByG19 = df[df["Country/Region"].isin(G19)][["Country/Region", "Lat", "Long"]];

countryLatitudeLongitudeMap = { row[1]["Country/Region"]: { "Latitude": row[1]["Lat"], "Longitude": row[1]["Long"] } for row in filteredByG19.iterrows() };

countryLatitudeLongitudeMap["United States"] = countryLatitudeLongitudeMap["US"];
del countryLatitudeLongitudeMap["US"];

with open("latitudeLongitudeByCountry.json", "w") as f:
    json.dump(countryLatitudeLongitudeMap, f, ensure_ascii=False, indent=4);
