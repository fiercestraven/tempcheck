
import * as Plot from '@observablehq/plot';
import * as d3 from "d3";
import { addTooltips } from '../lib/plotTooltips';
import Head from 'next/head';
import Link from 'next/link';
import Layout from '../components/layout';
import Header from '../components/header';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/router';

export default function Stats() {
  const { userData, logoutUser, userDataLoaded } = useContext(CurrentUserContext);
  const [moduleData, setModuleData] = useState([]);
  const [lectureData, setLectureData] = useState();
  const [pingData, setPingData] = useState([]);
  const [pingFetchComplete, setPingFetchComplete] = useState(false);
  const [profileData, setProfileData] = useState();
  const router = useRouter();
  const chartRef = useRef();

  useEffect(() => {
    async function getModuleData() {
      const res = await fetch('http://localhost:8000/tcapp/api/modules/', {
        headers: {
          'Authorization': `Bearer ${userData.access_token}`,
        },
      });
      let data = await res.json();
      setModuleData(data);
    }

    async function getProfileData() {
      const res = await fetch(`http://localhost:8000/tcapp/api/profile/`, {
        headers: {
          'Authorization': `Bearer ${userData.access_token}`,
        },
      });
      const data = await res.json();
      setProfileData(data);
    }

    // once user data is populated, do other api calls
    if (userDataLoaded && userData.username) {
      getModuleData();
      getProfileData();
    }
  }, [userData]);

  // set up chart
  // https://observablehq.com/@observablehq/plot?collection=@observablehq/plot
  useEffect(() => {
    console.debug("pingData is:", pingData);
    console.debug("chartRef is:", chartRef);
    const chart = addTooltips(Plot.plot({
      style: { background: 'transparent' },
      width: 1000,
      height: 100,
      marks: [
        // fv - remove this comment: Plot.ruleX(pingData, {x: 'normalized', strokeOpacity: 0.2, thresholds: d3.timeMinute.every(1)}),Plot.frame({stroke: 'white'}),
        Plot.dot(pingData, Plot.binX(
          { r: 'count', title: (pings) => `${pings.length} Ping${pings.length == 1 ? '' : 's'}` },
          { x: 'normalized', thresholds: d3.timeMinute.every(1) }
        )),
        Plot.frame({ stroke: 'white' }),
        // make marks every 5 min on x-axis
        Plot.axisX({
          label: 'UTC Time',
          interval: d3.timeMinute.every(5)
        }),
      ],
      // provide visual padding for first and last pings
      insetLeft: 30,
      insetRight: 30,
    }));
    chartRef?.current?.append(chart);
    return () => chart?.remove();
  }, [chartRef.current, pingData]);

  // wait until user data and profile data are loaded
  if (!userDataLoaded || !profileData) {
    return (
      <div>Loading...</div>
    );
  }

  // if not signed in or classed as a student user, re-route
  if (!userData.username || !profileData?.is_staff) {
    router.push("/modules");
  }

  // take user-selected data for module and look up lecture info
  async function handleModuleChange(event) {
    console.log(event.target.value);

    // target correct API endpoint and bring in lectures for the chosen module
    const res = await fetch(`http://localhost:8000/tcapp/api/modules/${event.target.value}/`, {
      headers: {
        'Authorization': `Bearer ${userData.access_token}`,
      },
    });
    const data = await res.json();
    setLectureData(data);
    console.log("Lecture data is ", data);
  }

  async function handleLectureChange(event) {
    console.log(event.target.value);

    // target correct API endpoint and bring in pings for chosen lecture
    const res = await fetch(`http://localhost:8000/tcapp/api/lectures/${event.target.value}/pings/`, {
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
      return datum;
    });
    setPingData(parsedData);
    setPingFetchComplete(true);
    console.log(pingData);
  }


  return (
    <Layout>
      <Head>
        <title>Stats</title>
      </Head>

      <header>
        <Header />
      </header>

      <div className="container content">
        {(userData.username && moduleData.length) &&
          <div>
            {/* menu for modules here */}
            {/* https://getbootstrap.com/docs/5.2/forms/select/ */}
            <select
              className="form-select"
              aria-label="Module selection"
              onChange={handleModuleChange}
            >
              {/* on using defaultValue: https://stackoverflow.com/questions/44786669/warning-use-the-defaultvalue-or-value-props-on-select-instead-of-setting */}
              <option defaultValue>Select a Module</option>
              {moduleData.map((module) => (
                <option value={module.module_shortname} key={module.module_shortname}>
                  {module.module_shortname}
                </option>
              ))}
              {!moduleData.length &&
                <option>There are no modules to display.</option>
              }
            </select>

            {/* menu for lectures here */}
            {lectureData?.lectures &&
              <div>
                <p></p>
                <select
                  className="form-select"
                  aria-label="Lecture selection"
                  onChange={handleLectureChange}
                >
                  <option defaultValue>Select a Lecture</option>
                  {lectureData.lectures.map((lecture) => (
                    <option value={lecture.lecture_shortname} key={lecture.lecture_shortname}>
                      {lecture.lecture_shortname}
                    </option>
                  ))}
                  {!lectureData.lectures.length &&
                    <option disabled>There are no lectures to display.</option>
                  }
                </select>

                {/* chart here */}
                {/* make sure pingData.length is a Boolean to prevent 0 being printed to page */}
                {pingFetchComplete && !!pingData.length &&
                  <div>
                    <p></p>
                    <div ref={chartRef}></div>
                  </div>
                }

                {/* if no pings for chosen lecture, display message */}
                {pingFetchComplete && !pingData.length &&
                  <div>
                    <p></p>
                    <p className="user-message">There are no pings associated with this lecture.</p>
                  </div>
                }
              </div>
            }

            <button className="w-30 mt-2 mb-5 btn btn-md btn-light" type={'submit'} onClick={logoutUser}>Log Out</button>
          </div>
        }
      </div>
    </Layout>
  );
}