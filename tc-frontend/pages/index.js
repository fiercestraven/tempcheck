import Head from 'next/head';
import Layout from '../components/layout';
import Login from './login';
import ModuleList from './modules';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect, useState } from 'react';

export default function HomePage() {
  const { userData, logoutUser, userDataLoaded } = useContext(CurrentUserContext);

  if (!userDataLoaded) {
    return (
      <div>Loading...</div>
    );
  }

  return (
    <div>
      <Layout home>
        <Head>
          <title>Home</title>
        </Head>

        {!userData.username && (
          <Login />
        )}

        {userData.username && (
          <ModuleList />
        )}
      </Layout>
    </div>
  );
}
