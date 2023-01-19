import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/router';

export default function ModuleList() {
    // const [moduleList, setModuleList] = useState([]);
    const { userData, logoutUser, userDataLoaded } = useContext(CurrentUserContext);
    const [studentModuleData, setStudentModuleData] = useState([]);
    const router = useRouter();

    useEffect(() => {
        // async function getModuleList() {
        //     let res = await fetch('http://localhost:8000/tcapp/api/modules/', {
        //         headers: {
        //             'Authorization': `Bearer ${userData.access_token}`,
        //         },});
        //     let data = await res.json();
        //     setModuleList(data);
        //     console.log(moduleList);
        // }

        async function getStudentModuleData() {
            let res = await fetch('http://localhost:8000/tcapp/api/student_modules/', {
                headers: {
                    'Authorization': `Bearer ${userData.access_token}`,
                },});
            let data = await res.json();
            setStudentModuleData(data);
            console.log(studentModuleData);
        }

        if (userDataLoaded && userData.username) {
            // getModuleList();
            getStudentModuleData();
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
        <div>
            {(userData.username && studentModuleData.module) &&
                <div className="container">
                    <h4 className="mt-4 mb-3" style={{fontStyle: 'italic'}}>Welcome, { userData.username }!</h4>
                    <h3>Modules</h3>
                    <section>
                        <ul>
                            {studentModuleData.map(({ module__module_shortname, module__module_name }) => (
                                <li key={ module__module_shortname }>
                                    <a href={ `modules/${module__module_shortname}` }>{ module__module_shortname }: { module__module_name }</a>
                                </li>
                            ))}
                            {/* {moduleList.map(({ module_shortname, module_name }) => (
                                <li key={module_shortname}>
                                        <a href={`modules/${module_shortname}`}>{module_shortname}: {module_name}</a>
                                </li>
                            ))} */}
                        </ul>
                    </section>
                    <p></p>
                    <button className="w-30 mt-2 mb-5 btn btn-md btn-primary" type={'submit'} onClick={logoutUser}>Log Out</button>
                </div>
            }

            {(!studentModuleData.module &&
                <div className="container user-message">You are not currently registered for any modules.</div>
            )}
        </div>
    );
}