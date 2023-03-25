// fv - don't forget to try to add capabililty for data export here

import Head from 'next/head';
import Link from 'next/link';
import Layout from '../components/layout';
import Header from '../components/header';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect, useState } from 'react';
// import { useForm } from 'react-hook-form';
import { useRouter } from 'next/router';
// initialize and register chart.js elements
import {
  Chart as ChartJS,
  LineController,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  LineController,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
);

export default function Stats() {
  // const { register, handleSubmit, formState: { errors } } = useForm();
  const { userData, logoutUser, userDataLoaded } = useContext(CurrentUserContext);
  const [moduleData, setModuleData] = useState([]);
  const [lectureData, setLectureData] = useState();
  const [pingData, setPingData] = useState();
  const [profileData, setProfileData] = useState();
  const [selectedModule, setSelectedModule] = useState();
  const [selectedLecture, setSelectedLecture] = useState();
  const router = useRouter();

  // set up options for chart
  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Pings Over Time',
      },
    },
  };

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

    async function getPingData() {
      // fv - change this later to just pull in pings from certain lecture
      const res = await fetch('http://localhost:8000/tcapp/api/pings/', {
        headers: {
          'Authorization': `Bearer ${userData.access_token}`,
        },
      });
      const data = await res.json();
      setPingData(data);
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
      getPingData();
      getProfileData();
    }
  }, [userData]);

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

    // fv - stop hard coding lecture here and instead use event.target.value (fix serializer or view for allPing data to use username and lecture_name)
    let lecturePings = pingData.filter(ping => ping.lecture==45)
    console.log(lecturePings);

    // fv - insert time stamps here (for pingData.ping_date) - what I'd rather do is have the lecture start time and then every 5 min
    // const labels = [event.target.value.lecture_date];
    // set 'lectureEnd' equal to the time of the last ping
    // for (i=0; i<lectureEnd; i+=5) {
    //     labels.append(i);
    // }

  // set up data for chart
  // const chartData = {
  //   labels,
  //   datasets: [
  //     {
  //       label: 'Lecture ' + selectedLecture.lecture_name,
  //       // set ping data for chart
  //       data: labels.map(() => pingData.ping_date({ min: -1000, max: 1000 })),
  //       borderColor: 'rgb(255, 99, 132)',
  //       backgroundColor: 'rgba(255, 99, 132, 0.5)',
  //     },
      // fv - may want to come back and add the option of displaying multiple lectures at once
      // {
      //   label: 'Dataset 2',
      //   data: labels.map(() => faker.datatype.number({ min: -1000, max: 1000 })),
      //   borderColor: 'rgb(53, 162, 235)',
      //   backgroundColor: 'rgba(53, 162, 235, 0.5)',
      // },
    // ],
  // };

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
              {/* <Line options={chartOptions} data={chartData} />; */}
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