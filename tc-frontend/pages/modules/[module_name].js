import Head from 'next/head';
import Link from 'next/link';
import Layout from '../../components/layout';
import Header from '../../components/header';
import Sidebar from '../../components/sidebar';
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
      // if student/instructor not associated with module, re-route to user's modules page
      if (res.status == 404) {
        router.push("/");
      }
      else {
        const data = await res.json();
        setModuleData(data);
      }
    }

    // only get module data after the module name is resolved
    if (userDataLoaded && userData && router.query.module_name) {
      getModuleData();
    }
  }, [userData, router.query]);

  if (!userDataLoaded) {
    return (
      <div>Loading...</div>
    );
  }

  if (!userData.username) {
    router.push("/");
  }

  return (
    <Layout>
      <Head>
        {/* assign title to head, supplying generic version if no module name available */}
        <title>{moduleData?.module_name || "Module Details"}</title>
      </Head>

      <div class="row">
        <div className="col-3 sidebar">
          <Sidebar />
        </div>

        <div className="col-9 content">
          <header>
            <Header />
          </header>

          <div className="container content">
            {moduleData?.module_name &&
              <h2>{moduleData.module_name}</h2>
            }

            {moduleData?.module_name &&
              <div>
                <p>{moduleData.module_description}</p>
                <p>Lecturer: {moduleData.instructor.first_name} {moduleData.instructor.last_name}</p>
                <p>Lectures:</p>
                <ul>
                  {moduleData.lectures.map(({ id, lecture_shortname, lecture_name }) => (
                    <li key={id}>
                      <a className="fancy-link" href={`lectures/${lecture_shortname}`}>{lecture_name}</a>
                    </li>
                  ))}
                  {!moduleData.lectures.length &&
                    <p>There are no lectures associated with this module.</p>
                  }
                </ul>
                <Link className="fancy-link" href="/">← Modules List</Link>
              </div>
            }
          </div>
        </div>
      </div>
    </Layout>
  );
}