import Head from 'next/head';
import Link from 'next/link';
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
    const { userData, logoutUser } = useContext(CurrentUserContext);
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
                    {/* fv check line below to see if working 2/1/23 */}
                    <h3 style='italic'>Welcome, { userData.username }!</h3>
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
                    <p></p>
                    <Link href="/">← Home</Link>
                    <p></p>
                    <button className="w-30 mt-2 mb-5 btn btn-md btn-primary" type={'submit'} onClick={logoutUser}>Log Out</button>
                </div>
            )}

        </Layout>
    );
}