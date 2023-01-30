import Head from 'next/head';
import Layout from '../components/layout';
import Header from '../components/header';
import Login from './login';
import ModuleList from './modules';
import { CurrentUserContext } from '../context/auth';
import { useContext } from 'react';

export default function HomePage() {
  const { userData,userDataLoaded } = useContext(CurrentUserContext);

  if (!userDataLoaded) {
    return (
      <div>Loading...</div>
    );
  }

  return (
    <div>
      <Layout>
        <Head>
          <title>Home</title>
        </Head>

        <header>
          <Header />
        </header>

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
