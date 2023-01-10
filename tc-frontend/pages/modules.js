import Head from 'next/head';
import Link from 'next/link';
import Layout from '../components/layout';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/router';

export default function ModuleList() {
    const [moduleList, setModuleList] = useState([]);
    const { userData, logoutUser, userDataLoaded } = useContext(CurrentUserContext);
    const router = useRouter();

    useEffect(() => {
        async function getModuleList() {
            let res = await fetch('http://localhost:8000/tcapp/api/modules/');
            let data = await res.json();
            setModuleList(data);
        }

        if (userDataLoaded && userData) {
            getModuleList();
        }
    }, [userData]);

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
                <title>Module List</title>
            </Head>

            {userData.username && 
                <div class="container">
                    {/* <h3 style={{fontStyle: 'italic'}}>Welcome, { userData.username }!</h3> */}
                    <h2>Modules</h2>
                    <section>
                        <ul>
                            {moduleList.map(({ module_shortname }) => (
                                <li key={module_shortname}>
                                    <a href={`modules/${module_shortname}`}>{module_shortname}</a>
                                </li>
                            ))}
                        </ul>
                    </section>
                    <p></p>
                    <Link href="/">← Home</Link>
                    <p></p>
                    <button className="w-30 mt-2 mb-5 btn btn-md btn-primary" type={'submit'} onClick={logoutUser}>Log Out</button>
                </div>
            }

        </Layout>
    );
}