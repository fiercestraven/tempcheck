import Head from 'next/head';
import Layout from '../components/layout';
import Image from 'next/image';
import { CurrentUserContext } from '../context/auth';
import { useContext } from 'react';

export default function IndexPage() {
  const { userData, logoutUser, userDataLoaded } = useContext(CurrentUserContext);
  const imageURL = "/images/gradient-fully-saturated.jpg"

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

        <div>
          <div className="row">
            <a href="/modules">
              <Image id="banner-img"
                priority
                src={imageURL}
                height={500}
                width={1800}
                alt="temperature gradient from green to red"
              />
            </a>

            <a id="index-header" href="/modules">
              {/* https://stackoverflow.com/questions/14678154/centre-align-text-that-has-extra-letter-spacing-applied */}
              TEMPCHECK
            </a>
          </div>

          <div className="row">
            <div className="col-5"></div>
            <div className="col-2">
              {!userData.username && (
                <div>
                  <a href="/modules" className="w-30 mt-2 mb-5 btn btn-outline-light btn-start" type={'submit'}>Start</a>
                </div>
              )}

              {userData.username && (
                // if already logged in, just show links to other pages
                <div>
                  <button className="w-30 mt-3 mb-5 btn btn-outline-light btn-start" type={'submit'} onClick={logoutUser}>Log Out</button>
                </div>
              )}
            </div>
            <div className="col-5"></div>
          </div>

        </div>
      </Layout>
    </div>
  );
}
