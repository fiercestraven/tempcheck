import Head from 'next/head';
import Link from 'next/link';
import Layout from '../../components/layout';

export default function Module({ module_detail }) {
  return (
    <Layout>
        <Head>
            <title>{module_detail.module_name}</title>
        </Head>
        <h1>{module_detail.module_name}</h1>
        <p>{module_detail.module_description}</p>
        {/* fv - link to instructor here */}
        <h3><Link href="/modules">Back to Modules</Link></h3>
        <h3><Link href="/lectures">Lectures</Link></h3>
    </Layout>
);
}

Module.getInitialProps = async (ctx) => {
    const { module_name } = ctx.query;
    const res = await fetch(`http://localhost:8000/tcapp/api/modules/${module_name}/`);
    const module_detail = await res.json()
    return { module_detail: module_detail }
  }