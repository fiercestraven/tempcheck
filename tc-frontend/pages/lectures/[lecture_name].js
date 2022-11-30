import Head from 'next/head';
import Link from 'next/link';
import Layout from '../../components/layout';

export default function Lecture({ lecture_detail }) {
  return (
    <Layout>
        <Head>
            <title>{lecture_detail.lecture_name}</title>
        </Head>
        <h2>{lecture_detail.lecture_name}</h2>
        <p>{lecture_detail.lecture_date}: {lecture_detail.lecture_description}</p>
        <h3><Link href="/lectures">Back to Lectures</Link></h3>

    </Layout>
);
}

Lecture.getInitialProps = async (ctx) => {
    const { lecture_name } = ctx.query;
    const res = await fetch(`http://localhost:8000/tcapp/api/lectures/${lecture_name}/`);
    const lecture_detail = await res.json()
    return { lecture_detail: lecture_detail }
  }