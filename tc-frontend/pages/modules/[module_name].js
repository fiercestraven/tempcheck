import Head from 'next/head';
import Link from 'next/link';
import Layout from '../../components/layout';
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
      const res = await fetch(`http://localhost:8000/tcapp/api/modules/${module_name}/`);
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
    router.push('/');
  }


  return (
    <Layout>
      <Head>
        <h3 style={{fontStyle: 'italic'}}>Welcome, { userData.username }!</h3>
        <title>{moduleData?.module_name || "Module Details"}</title>
      </Head>

      {moduleData?.module_name &&
        <div>
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
          <Link href="/modules">← Back to Modules</Link>
          <p></p>
          <Link href="/">← Home</Link>
          <p></p>
          <button className="w-30 mt-2 mb-5 btn btn-md btn-primary" type={'submit'} onClick={logoutUser}>Log Out</button>
        </div>
      } 
      {/* quick check */}
      <code> { JSON.stringify(moduleData) } </code>
    </Layout>
  );
}