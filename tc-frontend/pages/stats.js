import Head from 'next/head';
import Link from 'next/link';
import Layout from '../components/layout';
import Header from '../components/header';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/router';

export default function Stats() {
  const [moduleData, setModuleData] = useState([]);
  const [lectureData, setLectureData] = useState();
  const [pingData, setPingData] = useState();
  const { userData, logoutUser, userDataLoaded } = useContext(CurrentUserContext);
  const [profileData, setProfileData] = useState();
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

    // fv ask Dan how to fetch lecture info on this page-- have to select module first. So maybe have a form that on change triggers this api call?
    async function getLectureData() {
      const res = await fetch(`http://localhost:8000/tcapp/api/modules/${module_name}/`, {
        headers: {
          'Authorization': `Bearer ${userData.access_token}`,
        },
      });
      const data = await res.json();
      setLectureData(data);
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

    if (userDataLoaded && userData.username) {
      getModuleData();
      getPingData();
      getProfileData();
    }
  }, [userData]);

  if (!userDataLoaded) {
    return (
      <div>Loading...</div>
    );
  }

  // fv check that below line is working, or find a better way to handle a non-staff user here
  // if (!userData.username || !profileData.is_staff) {
    if (!userData.username) {
    router.push("/");
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
            <h2>Please select a module:</h2>
            {/* dropdown for modules here */}
            <ul>
              {moduleData.map((module) => (
                <li key={module.module_shortname}>
                  <p>{module.module_name}</p>
                </li>
              ))}
            </ul>
            <h2>Please select a lecture:</h2>
            {/* dropdown for lectures here */}
            <ul>
              {moduleData.lectures.map(({ id, lecture_name }) => (
                <li key={id}>
                  <p>{lecture_name}</p>
                </li>
              ))}
              {!moduleData.lectures.length &&
                <p>There are no lectures associated with this module.</p>
              }
            </ul>
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