import Head from 'next/head';
import Link from 'next/link';
import Layout from '../../components/layout';
import Header from '../../components/header';
import { CurrentUserContext } from '../../context/auth';
import { useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/router';

export default function Module() {
  const [moduleData, setModuleData] = useState();
  const { userData, logoutUser, userDataLoaded } = useContext(CurrentUserContext);
  const router = useRouter();
  const { module_name } = router.query;

  useEffect(() => {
    async function getModuleData() {
      const res = await fetch(`http://localhost:8000/tcapp/api/modules/${module_name}/`, {
        headers: {
          'Authorization': `Bearer ${userData.access_token}`,
        },
      });
      const data = await res.json();
      setModuleData(data);
    }

    if (userDataLoaded && userData) {
      getModuleData();
    }
  }, [userData, router.query]);

  if (!userDataLoaded) {
    return (
      <div>Loading...</div>
    );
  }

  if (!userData.username) {
    router.push("/modules");
  }

  return (
    <Layout>
      <Head>
        <h3 style={{ fontStyle: 'italic' }}>Welcome, {userData?.username || "Visitor"}!</h3>
        <title>{moduleData?.module_name || "Module Details"}</title>
      </Head>

      <div className="container content">
        <div className="row">
          <div className="col-6">
            <header>
              <Header />
            </header>
          </div>

          {/* fv - handle student landing here accidentally or through specific url but not being enrolled */}

          {moduleData?.module_name &&
            <div className="col-6">
              <h2>{moduleData.module_name}</h2>
              <p>{moduleData.module_description}</p>

              <p>Lecturer: {moduleData.instructor.first_name} {moduleData.instructor.last_name}</p>
              <p>Lectures:</p>
              <ul>
                {moduleData.lectures.map(({ id, lecture_name }) => (
                  <li key={id}>
                    <a href={`lectures/${lecture_name}`}>{lecture_name}</a>
                  </li>
                ))}
              </ul>
              <Link href="/modules">← Modules List</Link>
              <p></p>
              <button className="w-30 mt-2 mb-5 btn btn-md btn-light" type={'submit'} onClick={logoutUser}>Log Out</button>
            </div>

          }
        </div>
      </div>
    </Layout>
  );
}