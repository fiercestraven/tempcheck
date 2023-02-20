import Head from 'next/head';
import Layout from '../components/layout';
import Header from '../components/header';
import Link from 'next/link';
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
            {/* fv - make this a link */}
            <Image id="banner-img"
              priority
              src={imageURL}
              height={400}
              width={1800}
              alt=""
            />

            <div id="index-header">
              {/* fv - make this a link (to modules?) */}
              {/* https://stackoverflow.com/questions/14678154/centre-align-text-that-has-extra-letter-spacing-applied */}
              TEMPCHECK
            </div>
          </div>

{/* fv - make these tied in to the tempcheck name (make it a button?) and the image, so they act as login buttons */}
          <div className="row">
            <div className="col-5"></div>
            <div className="col-2">
              {!userData.username && (
                <div>
                  <a href="/modules" className="w-30 mt-2 mb-5 btn btn-large btn-outline-light" type={'submit'}>Start</a>
                </div>
              )}

              {userData.username && (
                // if already logged in, just show links to other pages
                <div>
                  <button className="w-30 mt-2 mb-5 btn btn-large btn-light" type={'submit'} onClick={logoutUser}>Log Out</button>
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
