import Head from 'next/head';
import Layout from '../components/layout';
import Header from '../components/header';
import Link from 'next/link';
import { CurrentUserContext } from '../context/auth';
import { useContext } from 'react';

export default function IndexPage() {
  const { userData, logoutUser, userDataLoaded } = useContext(CurrentUserContext);

  if (!userDataLoaded) {
    return (
      <div>Loading...</div>
    );
  }

  return (
    <div>
      <Layout>
        <Head>
          <title>Tempcheck</title>
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
                <a href="/home" className="w-30 mt-2 mb-5 btn btn-md btn-light" type={'submit'}>Login</a>
              )}

              {userData.username && (
                // if already logged in, just show links to other pages
                <div>
                  <Link href="/modules">Modules</Link>
                  <p></p>
                  <button className="w-30 mt-2 mb-5 btn btn-md btn-light" type={'submit'} onClick={logoutUser}>Log Out</button>  
                </div>
              )}
            </div>
          </div>
        </div>
      </Layout>
    </div>
  );
}
