// https://nextjs.org/learn/basics/assets-metadata-css/layout-component
import Head from 'next/head';
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

      <div>
        <main>{children}</main>
      </div>

      <footer>
          <Footer />
      </footer>
    </>
  );
}
