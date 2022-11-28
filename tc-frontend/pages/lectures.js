import Head from 'next/head';
import Link from 'next/link';
import Layout from '../components/layout';

export default function LectureList() {
    return (
        <Layout>
            <Head>
                <title>Lecture List</title>
            </Head>
            <h1>
                List of lectures
            </h1>
            <h3>
                <Link href="/modules">Modules</Link>
            </h3>
        </Layout>
    );
  }
  