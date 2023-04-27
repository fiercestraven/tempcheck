import Head from 'next/head';
import Layout from '../components/layout';
import Header from '../components/header';
import Login from '../components/login';
import ModuleList from '../components/modulelist';
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

                <header>
                    <Header />
                </header>

                <div className="container content">
                    <div className="row">
                        <div className="col-6">

                        </div>

                        <div className="col-6">
                            {!userData.username && (
                                <Login />
                            )}

                            {userData.username && (
                                <ModuleList />
                            )}

                        </div>

                    </div>
                </div>
            </Layout>
        </div>
    );
}