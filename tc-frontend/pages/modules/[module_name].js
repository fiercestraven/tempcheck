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
      <p>Lecturer: {module_detail.instructor.first_name} {module_detail.instructor.last_name}</p>
      {/* <p>Lectures:</p> */}

      <Link href="/modules">Back to Modules</Link>
      <p></p>
      <Link href="/lectures">All Lectures</Link>
    </Layout>
  );
}

https://nextjs.org/docs/api-reference/data-fetching/get-initial-props
Module.getInitialProps = async (ctx) => {
  const { module_name } = ctx.query;
  const res = await fetch(`http://localhost:8000/tcapp/api/modules/${module_name}/`);
  const module_detail = await res.json()
  return { module_detail: module_detail }
}