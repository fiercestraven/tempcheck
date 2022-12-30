import Head from 'next/head';
import Link from 'next/link';
import Layout from '../components/layout';
import { getLectureData } from '../lib/lectures';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect } from 'react';
import { useRouter } from 'next/router';

export async function getStaticProps() {
    const allLectureData = await getLectureData();
    return {
        props: {
            allLectureData,
        },
    };
}

export default function LectureList({ allLectureData }) {
    const { userData, logoutUser } = useContext(CurrentUserContext);
    const router = useRouter();

    useEffect(() => {
        if (!userData.username) {
            router.push('/');
        }
    }, [userData]);

    return (
        <Layout>
            <Head>
                <title>Lecture List</title>
            </Head>
            {userData.username && (
                <div>
                    <h2>Lectures</h2>
                    <ul>
                        {allLectureData.map(({ id, lecture_name }) => (
                            <li key={id}>
                                <a href={`/lectures/${lecture_name}`}>{lecture_name}</a>
                            </li>
                        ))}
                    </ul>
                    <Link href="/modules">← Modules</Link>
                    <p></p>
                    <button className="w-30 mt-2 mb-5 btn btn-md btn-primary" type={'submit'} onClick={logoutUser}>Log Out</button>
                </div>
            )}
        </Layout>
    );
}
