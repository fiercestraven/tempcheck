import Head from 'next/head';
import Layout from '../components/layout';
import { getModuleData } from '../lib/modules';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect } from 'react';
import { useRouter } from 'next/router';

export async function getStaticProps() {
    const allModuleData = await getModuleData();
    return {
        props: {
            allModuleData,
        },
    };
}

export default function ModuleList({ allModuleData }) {
    const { userData } = useContext(CurrentUserContext);
    const router = useRouter();

    useEffect(() => {
        if (!userData.username) {
          router.push('/');
        }
      }, [userData]);

    return (
        <Layout>
            <Head>
                <title>Module List</title>
            </Head>

            {userData.username && (
                <div>
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
                </div>
            )}

        </Layout>
    );
}