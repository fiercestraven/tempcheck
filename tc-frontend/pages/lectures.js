import Head from 'next/head';
import Link from 'next/link';
import Layout from '../components/layout';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/router';

export default function LectureList() {
    const [lectureList, setLectureList] = useState([]);
    const { userData, logoutUser, userDataLoaded } = useContext(CurrentUserContext);
    const router = useRouter();

    useEffect(() => {
        async function getLectureList() {
            let res = await fetch('http://localhost:8000/tcapp/api/lectures/', {
                headers: {
                    'Authorization': `Bearer ${userData.access_token}`,
                },});
            let data = await res.json();
            setLectureList(data);
        }

        if (userDataLoaded && userData) {
            getLectureList();
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
                <title>Lecture List</title>
            </Head>

            {userData.username &&
                <div class="container">
                    <h2>Lectures</h2>
                    <section>
                        <ul>
                            {lectureList.map(({ id, lecture_name }) => (
                                <li key={id}>
                                    <a href={`/lectures/${lecture_name}`}>{lecture_name}</a>
                                </li>
                            ))}
                        </ul>
                    </section>
                    <Link href="/modules">← Modules</Link>
                    <p></p>
                    <Link href="/">← Home</Link>
                    <p></p>
                    <button className="w-30 mt-2 mb-5 btn btn-md btn-primary" type={'submit'} onClick={logoutUser}>Log Out</button>
                </div>
            }
        </Layout>
    );
}
