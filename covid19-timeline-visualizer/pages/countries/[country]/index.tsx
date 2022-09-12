import Head from 'next/head';

const countryPage = ({ country }:any) => {
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

        </div>
    );
};

countryPage.getInitialProps = async ({ query }:any) => {
    const { country } = query;
    return { country };
};

export default countryPage;