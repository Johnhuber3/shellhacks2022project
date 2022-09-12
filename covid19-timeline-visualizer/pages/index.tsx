import type { NextPage } from 'next';
import Link from 'next/link';
import { useEffect, useState } from 'react';
import Head from 'next/head'
import Image from 'next/image'
import styles from '../styles/Home.module.css'
import MAPSET from '../public/features.json';
import DATASET from '../public/fullDataSet';
import { ComposableMap, Geographies, Geography, Marker, Sphere, Graticule } from "react-simple-maps";
import ReactTooltip from 'react-tooltip';


interface DatedCOVIDCountryProfile {
  "Date": string,
  "Country/Region": string,
  "Confirmed": number,
  "Deaths": number,
  "dayOfConfirmed": number,
  "dayOfDeaths": number
};

interface CountryLocation {
  "Latitude": number,
  "Longitude": number
};

// interface DatedCOVIDWorldProfile {
//   "totalDayDeaths": number,
//   "totalDayConfirmed": number,
//   "countrySpread": DatedCOVIDCountryProfile[][];
// };

// interface DataSet {
//   "unstructuredDateSortedData": DatedCOVIDCountryProfile[],
//   "structuredDateGroupedData": DatedCOVIDWorldProfile[],
//   "Country/Region Specific Geographic Coordinates": {  };
// };

const dset:any = DATASET;

interface mapAppProps {
  setTooltipContent: Function,
  tooltipContent: string
};

// List of all G19 country names
const G19:string[] = ['Argentina', 'Australia', 'Brazil', 'Canada', 'China', 'France', 'Germany', 'India', 'Indonesia', 'Italy', 'Japan', 'South Korea', 'Mexico', 'Russia', 'Saudi Arabia', 'South Africa', 'Turkey', 'United Kingdom', 'United States'];

// List of all G19 country flags
const G19EmojiFlags = ["🇦🇷","🇦🇺","🇧🇷","🇨🇦","🇨🇳","🇨🇵","🇩🇪","🇮🇳","🇲🇨","🇮🇹","🇯🇵","🇰🇷","🇲🇽","🇷🇺","🇸🇦","🇿🇦","🇹🇷","🇬🇧","🇺🇸"];

// "Tupled" list of each G19 country with their respective emoji flag
const pairWiseG19 = G19.map((countryName:string, index:number) => [ countryName, G19EmojiFlags[index] ]);

// initialize the country name key and country flag value paired map and seed key/value pairs
const countryEmojiMap:any = {  };
for (const [ G19countryName, G19EmojiFlag ] of pairWiseG19)
  countryEmojiMap[G19countryName] = G19EmojiFlag;

// get's country location data for markers into array format
const markerData:[string, CountryLocation][] = Object.entries(dset["Country/Region Specific Geographic Coordinates"]);

// get the number of days in the data set
const numberOfDays:number = dset["structuredDateGroupedData"].length;

const HeatMapVisualization = ({ setTooltipContent, tooltipContent }: mapAppProps) => {

  interface RankingCardProps {
    countryEmojiFlag: string,
    countryName: string,
    countryRanking: number
  };

  const RankingCard = ({ countryEmojiFlag, countryName, countryRanking }:RankingCardProps) =>
    <p style={ { fontWeight: "bold", fontSize: 32 } }>
      { `${countryRanking}. ${countryName} ${countryEmojiFlag}` }
    </p>

  // Initialize state value/function for the current day
  const [ day, setDay ] = useState<number>(0);
  
  // On mount effecting for interval of day progression every 300 seconds with clean up
  useEffect(() => {
    let timelineHeatMapInterval = setInterval(() => {
      if (day+1 < numberOfDays) setDay(day+1);
      else clearInterval(timelineHeatMapInterval);
    }, 300);

    return () => clearInterval(timelineHeatMapInterval);
  }, [ day ]);
  
  // This function calculates the current week of the data set
  const calculateWeek = () => Math.ceil(day / 7);

  // return the country color based on whether or not it is a part of the G19
  const setCountryColor = (isG19:boolean) => isG19 ? "red" : "black";

  // This function calculates the opacity score of a given country based on "contribution" to the total confirmed cases across the world on a given day
  const calculateOpacity = (country:string, isG19:boolean) => {

    // if we have a nonG19 country, set it's opacity to 0.25 by default. This will be done for the black-colored countries
    if (!isG19) return 0.25;

    // get the information object of the current day worldwide including total confirmed cases, total deaths, and country spread of these metrics on a given day across the world
    const worldwideDayData = dset["structuredDateGroupedData"][day];

    // since we have ensured we are dealing with a G19 country, search for it's data in the countrySpread on the given day.
    const countryOnDay = worldwideDayData["countrySpread"].filter((countryData: any) => countryData["Country/Region"] === country)[0];

    // this is a minimum opacity threshold to make things have a specific minimum possible visibility
    const FLOORDELTA = 0.125;

    // calculate the raw opacity score by taking a specific country's confirmed cases and dividing it by the worldwide confirmed cases on a given day
    const rawOpacityScore = countryOnDay["dayOfConfirmed"] / worldwideDayData["totalDayConfirmed"];

    // integrate a floor delta of 12.5% to the opacity score
    const baselineOpacityScore = rawOpacityScore + FLOORDELTA;

    // integrate a ceiling to the score if > 1
    return baselineOpacityScore > 1 ? 1 : baselineOpacityScore;
  };

  return (
    <div style={{ height: "75vh" }}>

      {/* Shows the current date along with the current week based on the day index */}
      <h1 style={{ fontSize: 40 }}>
        { `${ dset["structuredDateGroupedData"][day]["countrySpread"][0]["Date"] } | Week ${ calculateWeek() }` } 
      </h1>

      {/* Wrapper div for reactTooltip on the map */}
      <div data-tip="" style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
        <ComposableMap style={ { width: "75vw", height: "75vh" } }>
          
          {/* Adds a sphere to the back of the Z stack */}
          <Sphere stroke="#E4E5E6" strokeWidth={0.5} id={"."} fill="white" />

          {/* Adds a sphere to overlay the ComposableMap of the Z stack */}
          <Graticule stroke="#E4E5E6" strokeWidth={0.5} />

          {/* Create the world map based off files from a previously made dataset file from online */}
          <Geographies geography="/features.json">
            {({ geographies }) => {
              return geographies.map((geo) => {
                
                // Pull out the name from the current geographic element object
                const { properties: { name } } = geo;

                // check if this the current country is a part of the G19
                const isG19 = dset["Country/Region Specific Geographic Coordinates"][name] !== undefined;
                
                // Return the respective Geographic Component based off customization
                return <Link href={ `/countries/${isG19 ? name : ""}` }>
                  <Geography
                  key={geo.rsmKey} geography={geo}

                  // Add name to tooltip on mouse enter
                  onMouseEnter={() => { setTooltipContent(name); }}
                  
                  // Remove name to tooltip on mouse leave
                  onMouseLeave={() => { setTooltipContent(""); }}

                  // Multiple object of styles by default (at rest), on hover, and on press for a given geography
                  style={{
                    // This is where the heat map changes are applied (the opacity)
                    default: {
                      fill: setCountryColor(isG19),
                      outline: "none",
                      opacity: calculateOpacity(name, isG19)
                    },
                    hover: {
                      fill: "blue",
                      outline: "none",
                      opacity: 0.5
                    },
                    pressed: {
                      fill: "#E42",
                      outline: "none"
                    }
                  }}
                  />
                </Link>
              }) }
            }
          </Geographies>

          {/* Add in the markers at the given latitudes and longitudes for each of the G19 countries */}
          {
            markerData.map(([country, coordinateData]:any /* marker */) => {
              return <Marker key={country} coordinates={[ coordinateData["Longitude"], coordinateData["Latitude"] ]}>
              <circle r={2.5} fill="#F00" stroke="#fff" strokeWidth={0.25} />
            </Marker>
            })
          }
        </ComposableMap>
        
        {/* Ranking section for the heat map of confirmed COVID cases per day for the top 10 countries in the G19 in descending order. */}
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", width: "40vw", height: "75vh" }}>
          <h2> { `Worldwide Confirmed Cases` } </h2>
          <div>
            {
              dset["structuredDateGroupedData"][day]["countrySpread"].slice(0,10).map((countryData:any, rankingIndex:number) =>
                <RankingCard countryRanking={ rankingIndex+1 } countryName={ countryData["Country/Region"] } countryEmojiFlag={ "" } key={ `${countryData["Country/Region"]}${rankingIndex+1}` } />
              )
            }
          </div>
        </div>
      </div>
    </div>
  );
};


const Home: NextPage = () => {

  // Initialize state value/function for the tooltip
  const [ tooltipContent, setTooltipContent ] = useState<string>("");

  return (
    <div className={styles.container}>
      <Head>
        <title>COVID19 Heat Map</title>
        <link rel="icon" href="/favicon.png" />
      </Head>
      <section>
        <HeatMapVisualization setTooltipContent={ setTooltipContent } tooltipContent={ tooltipContent } />
          <ReactTooltip>
            { tooltipContent }
          </ReactTooltip>
      </section>
    </div>
  )
}

export default Home
