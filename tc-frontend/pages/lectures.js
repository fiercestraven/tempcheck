import Head from 'next/head';
import Link from 'next/link';
import Layout from '../components/layout';
import { getLectureData } from '../lib/lectures';

export async function getStaticProps() {
    const allLectureData = await getLectureData();
    return {
        props: {
            allLectureData,
        },
    };
}

export default function LectureList({ allLectureData }) {
    return (
        <Layout>
            <Head>
                <title>Lecture List</title>
            </Head>
            <h2>Lectures</h2>
            <ul>
                {allLectureData.map(({ id, lecture_name }) => (
                    <li key={id}>
                        <a href={`/lectures/${lecture_name}`}>{lecture_name}</a>
                    </li>
                ))}
            </ul>
            <Link href="/modules">← Modules</Link>
        </Layout>
    );
}
