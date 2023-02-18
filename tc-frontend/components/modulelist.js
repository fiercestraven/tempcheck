import Head from 'next/head';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/router';

export default function ModuleList() {
    const { userData, logoutUser, userDataLoaded } = useContext(CurrentUserContext);
    const [studentModuleData, setStudentModuleData] = useState([]);
    const router = useRouter();

    useEffect(() => {
        async function getStudentModuleData() {
            let res = await fetch('http://localhost:8000/tcapp/api/student_modules/', {
                headers: {
                    'Authorization': `Bearer ${userData.access_token}`,
                },
            });
            let data = await res.json();
            setStudentModuleData(data);
            console.log(data);
        }

        if (userDataLoaded && userData.username) {
            getStudentModuleData();
        }
    }, [userData]);

    if (!userDataLoaded) {
        return (
            <div>Loading...</div>
        );
    }

    if (!userData.username) {
        router.push("/modules");
    }

    return (
        <div>
            <Head>
                <title>Modules</title>
            </Head>

            <div className="container">
                <h3 style={{ fontStyle: 'italic' }}>Welcome, {userData?.username || "Visitor"}!</h3>

                {(userData.username && studentModuleData.length) &&
                    <div className="container">
                        <h3>Modules</h3>
                        <section>
                            <ul>
                                {studentModuleData.map(({ module }) => (
                                    <li key={module.module_shortname}>
                                        <a href={`modules/${module.module_shortname}`}>{module.module_shortname}: {module.module_name}</a>
                                    </li>
                                ))}
                            </ul>
                        </section>
                        <p></p>
                        <button className="w-30 mt-2 mb-5 btn btn-md btn-light" type={'submit'} onClick={logoutUser}>Log Out</button>
                    </div>
                }

                {!studentModuleData.length &&
                    <div className="container user-message">You are not currently registered for any modules.</div>
                }
            </div>
        </div>
    );
}