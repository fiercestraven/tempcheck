import Head from 'next/head';
import Link from 'next/link';
import Layout from '../../components/layout';

export default function Module({ module_detail }) {
  return (
    <Layout>
      <Head>
        <title>{module_detail.module_name}</title>
      </Head>
      <h2>{module_detail.module_name}</h2>
      <p>{module_detail.module_description}</p>
      <p>Lecturer: {module_detail.instructor.first_name} {module_detail.instructor.last_name}</p>
      <p>Lectures:</p>
      <ul>
        {module_detail.lectures.map(({ id, lecture_name }) => (
          <li key={id}>
            <a href={`lectures/${lecture_name}`}>{lecture_name}</a>
          </li>
        ))}
      </ul>
      <Link href="/modules">Back to Modules</Link>
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