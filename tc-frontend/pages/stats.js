
import * as Plot from '@observablehq/plot';
import { addTooltips } from '../lib/plotTooltips';
import Head from 'next/head';
import Layout from '../components/layout';
import Header from '../components/header';
import LecturePingChart from '../components/lecturePingChart';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/router';

export default function Stats() {
  const { userData, logoutUser, userDataLoaded } = useContext(CurrentUserContext);
  const [moduleData, setModuleData] = useState([]);
  const [lectureData, setLectureData] = useState();
  const [pingData, setPingData] = useState([]);
  const [profileData, setProfileData] = useState();
  const [lectureFetchComplete, setLectureFetchComplete] = useState(false);
  const router = useRouter();
  const dotChartRef = useRef();
  const pingsPerModuleChartRef = useRef();
  const [selectedLecture, setSelectedLecture] = useState();

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

  // set up avg pings per module bar chart
  useEffect(() => {
    console.debug("pingData is:", pingData);
    console.debug("pingsPerModuleChartRef is:", pingsPerModuleChartRef);
    let chart;

    async function fetchPingsBarChart() {
      // fv check for lectureData complete here

      // create map of lecture names and average ping values
      const pingSummary = [];

      for (const lecture of lectureData.lectures) {
        const res = await fetch(`http://localhost:8000/tcapp/api/lectures/${lecture.lecture_shortname}/pings`, {
          headers: {
            'Authorization': `Bearer ${userData.access_token}`,
          },
        });
        const data = await res.json();
        // count and store number of pings for each lecture in the numPings structure
        pingSummary.push({ 'name': lecture.lecture_name, 'pings': data.length });
      }
      console.log(pingSummary);
      chart = addTooltips(Plot.plot({
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
            title: (summary) => `${summary.pings} Ping${summary.pings == 1 ? '' : 's'}`
          })
        ]
      }), {
        stroke: 'white',
        fill: 'gray',
        'stroke-width': 4,
      });
      pingsPerModuleChartRef?.current?.append(chart);
    }
    // if lectureData exists, run ping bar chart function
    lectureData && fetchPingsBarChart();
    return () => chart?.remove();
  }, [pingsPerModuleChartRef.current, lectureData]);

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
    setSelectedLecture(undefined);
    console.log(event.target.value);

    // target correct API endpoint and bring in lectures for the chosen module
    const res = await fetch(`http://localhost:8000/tcapp/api/modules/${event.target.value}/`, {
      headers: {
        'Authorization': `Bearer ${userData.access_token}`,
      },
    });
    const data = await res.json();
    setLectureData(data);
    setLectureFetchComplete(true);
    console.log("Lecture data is ", data);
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
              <option defaultValue value="">Select a Module</option>
              {moduleData.map((module) => (
                <option value={module.module_shortname} key={module.module_shortname}>
                  {module.module_shortname}
                </option>
              ))}
              {!moduleData.length &&
                <option>There are no modules to display.</option>
              }
            </select>

            {/* pings per module graph here */}
            {lectureFetchComplete &&
              <div className="mt-3 mb-2" ref={pingsPerModuleChartRef}>
              </div>
            }

            {/* menu for lectures here */}
            {lectureData?.lectures &&
              <div>
                <p></p>
                <select
                  className="form-select"
                  aria-label="Lecture selection"
                  onChange={(event) => { setSelectedLecture(event.target.value) }}
                >
                  <option defaultValue value="">Select a Lecture</option>
                  {lectureData.lectures.map((lecture) => (
                    <option value={lecture.lecture_shortname} key={lecture.lecture_shortname}>
                      {lecture.lecture_name}
                    </option>
                  ))}
                  {!lectureData.lectures.length &&
                    <option disabled>There are no lectures to display.</option>
                  }
                </select>

                {/* chart here */}
                <LecturePingChart lectureName={selectedLecture} />
              </div>
            }
          </div>
        }

        <div>
          <button className="w-30 mt-2 mb-5 btn btn-md btn-light" type={'submit'} onClick={logoutUser}>Log Out</button>
        </div>
      </div>
    </Layout >
  );
}