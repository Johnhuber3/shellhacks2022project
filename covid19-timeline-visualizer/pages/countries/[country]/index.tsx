import Head from 'next/head';
import DATASET from '../../../public/fullDataSet';
import Image from 'next/image';

const dset:any = DATASET;

const countryPage = ({ country }:any) => {

    const structuredDateGroupedData = dset["structuredDateGroupedData"];
    const numberOfDays = structuredDateGroupedData.length;
    const countryData = structuredDateGroupedData[numberOfDays-1]["countrySpread"].filter((countryData:any) => countryData["Country/Region"] === country)[0];

    const precision = (value:number, decimalPrecision:number):number => {
        let answer = [  ], baseString = String(value), foundDecimal = false;

        for (const character of baseString) {
            if (foundDecimal) {
                if (decimalPrecision-->0)
                    answer.push(character);
                else
                    break;
            } else {
                answer.push(character);

                if (character === ".")
                    foundDecimal = true;
            };
        };

        if (!foundDecimal)
            answer.push(".");

        while (decimalPrecision-->0)
            answer.push("0");

        return Number(answer.join(""));
    };

    return (
        <div style={ { width: "100vw", height: "100vh", display: "flex", flexDirection: "column", alignItems: "center" } }>
            <Head>
                <title>{`${country}'s Data`}</title>
            </Head>

            <h1>
                { `${country} Data Visualization and Statistics` }
            </h1>
            <div style={{ width: "100vw", display: "flex", justifyContent: "space-around", alignItems: "center" }}>
                <video controls src={ `/videoGraphs/${country}.mp4` } autoPlay />
                <img src={ `/staticGraphs/${country}.png` } />
            </div>
            <div style={{ width: "100vw", display: "flex", flexDirection: "column", alignItems: "center" }}>
                <h1> Confirmed Cases: <span style={{ color: "red" }}>{ countryData["Confirmed"] } </span> from 01/22/2020 - 07/27/2022 </h1>
                <h1> Confirmed Deaths: <span style={{ color: "red" }}>{ countryData["Deaths"] } </span> from 01/22/2020 - 07/27/2022 </h1>
                <h1> Survival Rate: <span style={{ color: "red" }}>{ `${ precision((countryData["Confirmed"] - countryData["Deaths"]) / (countryData["Confirmed"]) * 100, 2) }%` } </span> from 01/22/2020 - 07/27/2022 </h1>
                <h1> Average Cases Per Day: <span style={{ color: "red" }}>{ `${ precision(countryData["Confirmed"] / numberOfDays, 2) }` } </span> from 01/22/2020 - 07/27/2022 </h1>
            </div>

        </div>
    );
};

countryPage.getInitialProps = async ({ query }:any) => {
    const { country } = query;
    return { country };
};

export default countryPage;