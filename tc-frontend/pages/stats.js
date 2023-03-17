import Head from 'next/head';
import Link from 'next/link';
import Layout from '../components/layout';
import Header from '../components/header';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/router';
// import { useForm } from "react-hook-form";

export default function Stats() {
  // const { register, handleSubmit, formState: { errors } } = useForm();
  const { userData, logoutUser, userDataLoaded } = useContext(CurrentUserContext);
  const [moduleData, setModuleData] = useState([]);
  const [lectureData, setLectureData] = useState();
  const [pingData, setPingData] = useState();
  const [profileData, setProfileData] = useState();
  const [selectedModule, setSelectedModule] = useState();
  const router = useRouter();

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
    console.log(userData, profileData);
    router.push("/modules");
  }

  // take user-selected data for module and look up lecture info
  async function handleModuleChange(event) {
    console.log(event.target.value);
    setSelectedModule(event.target.value);

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
                  {module.module_name}
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