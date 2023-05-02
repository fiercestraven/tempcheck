import Head from 'next/head';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/router';

export default function ModuleList() {
    const { userData, userDataLoaded } = useContext(CurrentUserContext);
    const [moduleData, setModuleData] = useState([]);
    const router = useRouter();

    useEffect(() => {
        async function getModuleData() {
            let res = await fetch('http://localhost:8000/tcapp/api/modules/', {
                headers: {
                    'Authorization': `Bearer ${userData.access_token}`,
                },
            });
            let data = await res.json();
            setModuleData(data);
        }

        if (userDataLoaded && userData.username) {
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
        <div>
            <Head>
                <title>Modules</title>
            </Head>

            <h3 className="welcome-message">Welcome, {userData?.first_name || "Visitor"}!</h3>
            <div className="container content">
                <h1>modules</h1>

                {(userData.username && moduleData.length) &&
                    <div className="container modules-section">
                        <section>
                            <ul>
                                {moduleData.filter((module) => module.is_active).map((module) => (
                                    <li key={module.module_shortname}>
                                        <a href={`modules/${module.module_shortname}`}>{module.module_shortname}: {module.module_name}</a>
                                    </li>
                                ))}
                            </ul>
                        </section>
                    </div>
                }

                {!moduleData.length &&
                    <div className="container user-message">You are not currently registered for any modules.</div>
                }
            </div>
        </div>
    );
}