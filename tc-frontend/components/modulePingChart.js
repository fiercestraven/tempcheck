import * as Plot from '@observablehq/plot';
import * as d3 from "d3";
import { addTooltips } from '../lib/plotTooltips';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect, useState, useRef } from 'react';
// https://www.npmjs.com/package/react-csv-downloader
import CsvDownloader from 'react-csv-downloader';

export default function ModulePingChart({ lectures }) {
    const { userData, userDataLoaded } = useContext(CurrentUserContext);
    const [pingSummary, setPingSummary] = useState([]);
    const [pingSummaryComplete, setPingSummaryComplete] = useState(false);
    const pingsPerModuleChartRef = useRef();

    // fetch data
    useEffect(() => {
        setPingSummaryComplete(false);
        async function fetchData() {
            const counts = [];
            for (const lecture of lectures) {
                const res = await fetch(`http://localhost:8000/tcapp/api/lectures/${lecture.lecture_shortname}/pings`, {
                    headers: {
                        'Authorization': `Bearer ${userData.access_token}`,
                    },
                });
                const data = await res.json();

                // count and store number of pings for each lecture in the numPings structure
                counts.push({ 'name': lecture.lecture_name, 'pings': data.length });
            }

            setPingSummary(counts);
            setPingSummaryComplete(true);
        }

        if (userDataLoaded && lectures) {
            fetchData();
        }
    }, [userDataLoaded, lectures]);

    // set up avg pings per module bar chart
    useEffect(() => {
        let chart = addTooltips(Plot.plot({
            marginBottom: 80,
            x: {
                tickRotate: -30,
                label: '',
            },
            style: { background: 'transparent' },
            marks: [
                Plot.ruleY([0]),
                Plot.barY(pingSummary, {
                    x: 'name',
                    y: 'pings',
                    title: (summary) => `${summary.pings} Ping${summary.pings == 1 ? '' : 's'}`,
                    fill: 'yellowgreen'
                })
            ]
        }), {
            stroke: 'white',
            fill: 'steelblue',
            'stroke-width': 4,
        });
        pingsPerModuleChartRef?.current?.append(chart);

        return () => chart?.remove();
    }, [pingsPerModuleChartRef.current, pingSummary]);

    if (!lectures) {
        return;
    }

    if (!pingSummaryComplete) {
        return (<div>Loading...</div>)
    }

    if (pingSummary.length == 0) {
        return (
            <div>
                <p></p>
                <p className="user-message">There are no pings associated with any lectures in this module.</p>
            </div>
        )
    }

    // we know fetch is done and we have data to display
    return (
        <>
            <p></p>
            <div ref={pingsPerModuleChartRef}></div>
        </>
    )
}