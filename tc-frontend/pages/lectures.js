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
            <h1>Lectures</h1>
            <ul>
                {/* fv - fix urls to go to correct ones, not api ones - REACT ROUTER - or use event listener which will call a component to create a lecture page */}
                {allLectureData.map(({ id, lecture_name }) => (
                    <li key={id}>
                        <a href={`/lectures/${lecture_name}`}>{lecture_name}</a>
                    </li>
                ))}
            </ul>
            <h3>
                <Link href="/modules">Modules</Link>
            </h3>
        </Layout>
    );
}
