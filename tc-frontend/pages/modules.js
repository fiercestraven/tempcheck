import Head from 'next/head';
import Layout from '../components/layout';
import { getModuleData } from '../lib/modules';

export async function getStaticProps() {
    const allModuleData = await getModuleData();
    return {
        props: {
            allModuleData,
        },
    };
}

export default function ModuleList({ allModuleData }) {
    return (
        <Layout>
            <Head>
                <title>Module List</title>
            </Head>
            <h2>Modules</h2>
            <section>
                <ul>
                    {allModuleData.map(({ id, module_shortname }) => (
                        <li key={id}>
                            <a href={`modules/${module_shortname}`}>{module_shortname}</a>
                        </li>
                    ))}
                </ul>
            </section>
        </Layout>
    );
}