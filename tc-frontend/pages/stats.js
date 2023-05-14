
import Head from 'next/head';
import Layout from '../components/layout';
import Header from '../components/header';
import LecturePingChart from '../components/lecturePingChart';
import ModulePingChart from '../components/modulePingChart';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/router';

export default function Stats() {
  const { userData, logoutUser, userDataLoaded } = useContext(CurrentUserContext);
  const [moduleData, setModuleData] = useState([]);
  const [lectureData, setLectureData] = useState();
  const [profileData, setProfileData] = useState();
  const router = useRouter();
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

  // wait until user data and profile data are loaded
  if (!userDataLoaded || !profileData) {
    return (
      <div>Loading...</div>
    );
  }

  // if not signed in or classed as a student user, re-route
  if (!userData.username || !profileData?.is_staff) {
    router.push("/");
  }

  // take user-selected data for module and look up lecture info
  async function handleModuleChange(event) {
    // reset state to prevent old charts hanging around
    setSelectedLecture(undefined);
    setLectureData(undefined);

    // target correct API endpoint and bring in lectures for the chosen module
    if (event.target.value) {
      const res = await fetch(`http://localhost:8000/tcapp/api/modules/${event.target.value}/`, {
        headers: {
          'Authorization': `Bearer ${userData.access_token}`,
        },
      });
      const data = await res.json();
      setLectureData(data);
    }
  }

  return (
    <Layout>
      <Head>
        <title>Stats</title>
      </Head>

      <div class="row">
        <div className="col-1"></div>

        <div className="col-10 content">
          <header>
            <Header />
          </header>

          <div>
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

                {/* pings per module chart here */}
                < ModulePingChart lectures={lectureData?.lectures} />

                {/* menu for lectures here */}
                {lectureData?.lectures && lectureData.lectures.length != 0 &&
                  <div>
                    <p></p>
                    <select
                      className="mb-4 form-select"
                      aria-label="Lecture selection"
                      onChange={(event) => { setSelectedLecture(event.target.value) }}
                    >
                      <option defaultValue value="">Select a Lecture</option>
                      {lectureData.lectures.map((lecture) => (
                        <option value={lecture.lecture_shortname} key={lecture.lecture_shortname}>
                          {lecture.lecture_name}
                        </option>
                      ))}
                    </select>

                    {/* lecture ping chart here */}
                    <LecturePingChart lectureName={selectedLecture} />
                  </div>
                }
              </div>
            }
          </div>
        </div>
      </div>
    </Layout >
  );
}