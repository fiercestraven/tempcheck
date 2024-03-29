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
            data = data.filter((module) => module.is_active)
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

            <div className="content">
                <h1>modules</h1>

                {/* !! prevents this block from defaulting to (and printing out) 0 if no modules are returned */}
                {(userData.username && !!moduleData.length) &&
                    <div>
                        <section>
                            <ul>
                                {moduleData.map((module) => (
                                    <li key={module.module_shortname}>
                                        <a className="fancy-link" href={`modules/${module.module_shortname}`}>{module.module_shortname}: {module.module_name}</a>
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