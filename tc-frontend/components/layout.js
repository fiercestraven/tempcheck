// https://nextjs.org/learn/basics/assets-metadata-css/layout-component
import Head from 'next/head';
// import styles from './layout.module.css';
// import utilStyles from '../styles/utils.module.css';
import Footer from './footer';

export default function Layout({ children }) {
  return (
    <>
      <Head>
        <meta
          name="Tempcheck"
          content="Check the mood of a group of students"
        />
      </Head>

      <div id="__next">
        <main>{children}</main>
        <footer>
          <Footer />
        </footer>
      </div>
    </>
  );
}
