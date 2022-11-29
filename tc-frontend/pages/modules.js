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
            <h1>Modules</h1>
            <section>
                <ul>
                    {allModuleData.map(({ id, url, module_name }) => (
                        <li key={id}>
                            <a href={url}>{module_name}</a>
                        </li>
                    ))}
                </ul>
            </section>
        </Layout>
    );
}