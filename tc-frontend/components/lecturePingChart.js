import * as Plot from '@observablehq/plot';
import * as d3 from "d3";
import { addTooltips } from '../lib/plotTooltips';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect, useState, useRef } from 'react';
// https://www.npmjs.com/package/react-csv-downloader
import CsvDownloader from 'react-csv-downloader';

export default function LecturePingChart({ lectureName }) {
    const { userData, userDataLoaded } = useContext(CurrentUserContext);
    const [pingData, setPingData] = useState([]);
    const [pingFetchComplete, setPingFetchComplete] = useState(false);
    const dotChartRef = useRef();

    // fetch data
    useEffect(() => {
        setPingFetchComplete(false);

        async function fetchData() {
            // target correct API endpoint and bring in pings for chosen lecture
            const res = await fetch(`http://localhost:8000/tcapp/api/lectures/${lectureName}/pings/`, {
                headers: {
                    'Authorization': `Bearer ${userData.access_token}`,
                },
            });

            const data = await res.json();
            // turn ping date into an actual date for graphing purposes
            const parsedData = data.map(datum => {
                datum.ping_date = new Date(datum.ping_date);
                datum.normalized = new Date(
                    // ignoring year, month, day - any given lecture occurs on only one day
                    // convert hours and minutes into milliseconds
                    (datum.ping_date.getUTCHours() * 60 * 60 * 1000) +
                    (datum.ping_date.getUTCMinutes() * 60 * 1000)
                    // ignoring seconds - too granular for the chart
                )
                // make a version of the date for csv export that is more easily readable
                datum.readableDate = datum.ping_date.toISOString().slice(11, 19);
                return datum;
            });
            setPingData(parsedData);
            setPingFetchComplete(true);
        }

        if (userDataLoaded && lectureName) {
            fetchData();
        }
    }, [userDataLoaded, lectureName]);

    // set up ping visualisation chart
    useEffect(() => {
        // https://observablehq.com/@observablehq/plot?collection=@observablehq/plot
        const chart = addTooltips(Plot.plot({
            style: { background: 'transparent' },
            width: 1000,
            height: 100,
            marks: [
                Plot.dot(pingData, Plot.binX(
                    { r: 'count', title: (pings) => `${pings.length} Ping${pings.length == 1 ? '' : 's'}` },
                    { x: 'normalized', thresholds: d3.timeMinute.every(1) }
                )),
                Plot.frame({ stroke: 'black' }),
                // make marks every 5 min on x-axis
                Plot.axisX({
                    label: 'UTC Time',
                    interval: d3.timeMinute.every(5)
                }),
            ],
            // provide visual padding for first and last pings
            insetLeft: 30,
            insetRight: 30,
        }), {
            stroke: 'black',
            fill: 'gray',
            'stroke-width': 4,
        });
        dotChartRef?.current?.append(chart);
        return () => chart?.remove();
    }, [dotChartRef.current, pingData]);


    // set up column names for csv export file
    const csvColumns = [
        { id: 'readableDate', displayName: 'Ping Date' },
        { id: 'student', displayName: 'Student' },
        { id: 'lecture', displayName: 'Lecture' }
    ];

    if (!lectureName) {
        return;
    }

    if (!pingFetchComplete) {
        return (<div>Loading...</div>)
    }

    if (pingData.length == 0) {
        return (
            <div>
                <p></p>
                <p className="user-message">There are no pings associated with this lecture.</p>
            </div>
        )
    }

    // we know fetch is done and we have data to display
    return (
        <>
            <p></p>
            <div ref={dotChartRef}></div>
            {/* show/hide ping data table */}
            <details>
                <summary>Show Ping Table</summary>
                <table>
                    <tr>
                        <th>Ping Date</th>
                        <th>Student</th>
                        <th>Lecture</th>
                    </tr>
                    {pingData.map((ping) => (
                        <tr>
                            {/* return string of date here instead of object, and slice it to return only the time, not date */}
                            <td>{ping.readableDate}</td>
                            <td>{ping.student}</td>
                            <td>{ping.lecture}</td>
                        </tr>
                    ))}
                    {!pingData.length &&
                        <tr>
                            <td>There are no pings to display.</td>
                        </tr>
                    }
                </table>
            </details>
            <CsvDownloader className="w-30 mt-4 mb-5 btn btn-md btn-primary" text="Download Ping Data" datas={pingData} columns={csvColumns} filename={`${pingData[0].lecture}.csv`} />
        </>
    )
}