import Head from 'next/head';
import Layout from '../components/layout';
import Header from '../components/header';
import Login from '../components/login';
import ModuleList from '../components/modulelist';
import React, { useContext } from 'react';
import { CurrentUserContext } from '../context/auth';
import Image from 'next/image';

export default function HomePage() {
    // get user management functions from context
    const { userData } = useContext(CurrentUserContext);
    const imageURL = "/images/rainbow_thermometer.svg"

    return (
        <div>
            <Layout>
                <Head>
                    <title>Tempcheck Login</title>
                </Head>

                <div class="row">
                    <div className="col-3 sidebar">
                        <Image id="side-img"
                            priority
                            src={imageURL}
                            width={420}
                            height={700}
                        />
                    </div>

                    <div className="col-9 content">
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