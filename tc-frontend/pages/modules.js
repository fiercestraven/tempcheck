import Head from 'next/head';
import Layout from '../components/layout';
import Header from '../components/header';
import Login from '../components/login';
import ModuleList from '../components/modulelist';
import Link from 'next/link';
import React, { useContext } from 'react';
import { CurrentUserContext } from '../context/auth';

export default function HomePage() {
    // get user management functions from context
    const { userData } = useContext(CurrentUserContext);

    return (
        <div>
            <Layout>
                <Head>
                    <title>Tempcheck Login</title>
                </Head>

                <div className="container content">
                    <div className="row">
                        <div className="col-6">
                            <header>
                                <Header />
                            </header>
                        </div>

                        <div className="col-6">
                            {!userData.username && (
                                <Login />
                            )}

                            {userData.username && (
                                <ModuleList />
                            )}

                            <p></p>
                            <Link href="/">← Home</Link>
                            <p></p>
                        </div>

                    </div>
                </div>
            </Layout>
        </div>
    );
}