import Head from 'next/head';
import Link from 'next/link';
import Layout from '../../../components/layout';
import { CurrentUserContext } from '../../../context/auth';
import { useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/router';

export default function Lecture() {
    const [lectureData, setLectureData] = useState();
    const { userData, logoutUser, userDataLoaded } = useContext(CurrentUserContext);
    const router = useRouter();
    const { lecture_name } = router.query;

    useEffect(() => {
        async function getLectureData() {
            const res = await fetch(`http://localhost:8000/tcapp/api/lectures/${lecture_name}/`);
            const data = await res.json();
            setLectureData(data);
        }

        if (userDataLoaded && userData) {
            getLectureData();
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
                <title>{lectureData?.lecture_name || "Lecture Details"}</title>
            </Head>

            {lectureData?.lecture_name &&
                <div class="container">
                    <h2>{lectureData.module.module_name}</h2>
                    <h3>Lecture: {lectureData.lecture_name}</h3>
                    <p>{lectureData.lecture_date}: {lectureData.lecture_description}</p>

                    {/* fv - do error handling on this form */}
                    <form action="http://localhost:8000/tcapp/api/pings/" method="post">
                        <input type="submit" name="ping" id="ping" value="Ping"></input>
                        {/* fv - see if below student info is working */}
                        <input type="number" name="student" value={userData.pk}></input>
                        <input type="text" name="lecture_name" value={lectureData.lecture_name}></input>
                    </form>

                    <p></p>
                    <Link href={`/modules/${lectureData.module.module_shortname}`}>← Back to Module</Link>
                    <p></p>
                    <Link href="/">← Home</Link>
                    <p></p>
                    <button className="w-30 mt-2 mb-5 btn btn-md btn-primary" type={'submit'} onClick={logoutUser}>Log Out</button>
                </div>
            }
        </Layout>
    );
}