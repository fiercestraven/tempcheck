import Head from 'next/head';
import Layout from '../components/layout';
import Header from '../components/header';
import Sidebar from '../components/sidebar';
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

                <div class="row">
                    <div className="col-3 sidebar">
                        <Sidebar />
                    </div>

                    <div className="col-9">
                        <header>
                            <Header />
                        </header>

                        <div>
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