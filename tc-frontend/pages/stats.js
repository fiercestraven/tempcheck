// fv - don't forget to try to add capabililty for data export for the chart
import * as Plot from '@observablehq/plot';
import * as d3 from "d3";
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
  const [profileData, setProfileData] = useState();
  const [selectedModule, setSelectedModule] = useState();
  const [selectedLecture, setSelectedLecture] = useState();
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
    console.debug("🤪 called charting effect");
    console.debug("pingData is:", pingData);
    console.debug("chartRef is:", chartRef);
    const chart = Plot.plot({
      x: {
        round: true
      },
      color: {
        scheme: "YlGnBu"
      },
      marks: [
        // fv - below not working - interval? thresholds? thresholds sets how many bins
        // fv - client side work to discard any data more than 5 minutes prior to lecture and 30 min after
        Plot.barX(pingData, Plot.binX({ fill: "count" }, { x: "ping_date" }))
      ]
    });
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
    setSelectedModule(event.target.value);

    // target correct API endpoint and bring in lectures for the chosen module
    const res = await fetch(`http://localhost:8000/tcapp/api/modules/${event.target.value}/`, {
      headers: {
        'Authorization': `Bearer ${userData.access_token}`,
      },
    });
    const data = await res.json();
    setLectureData(data);
    console.log(data);
  }

  async function handleLectureChange(event) {
    console.log(event.target.value);
    setSelectedLecture(event.target.value);

    // target correct API endpoint and bring in pings for chosen lecture
    const res = await fetch(`http://localhost:8000/tcapp/api/lectures/${event.target.value}/pings/`, {
      headers: {
        'Authorization': `Bearer ${userData.access_token}`,
      },
    });
    const data = await res.json();
    const parsedData = data.map(datum => {
      datum.ping_date = new Date(datum.ping_date);
      return datum;
    });
    setPingData(parsedData);
    console.log(pingData);
  }


return (
  <Layout>
    <Head>
      <title>Stats</title>
    </Head>

    <div className="container content">
      <header>
        {/* fv  - insert different stats header here */}
        <Header />
      </header>

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
                  <option value={lecture.lecture_name} key={lecture.lecture_name}>
                    {lecture.lecture_name}
                  </option>
                ))}
                {!lectureData.lectures.length &&
                  <option>There are no lectures to display.</option>
                }
              </select>

              {/* fv - update this to only display after lecture is chosen */}
              {/* chart */}
              <p></p>
              <div ref={chartRef}></div>
            </div>
          }

          <p></p>
          <Link href="/">← Home</Link>
          <p></p>
          <button className="w-30 mt-2 mb-5 btn btn-md btn-light" type={'submit'} onClick={logoutUser}>Log Out</button>
        </div>
      }
    </div>
  </Layout>
);
}