// https://nextjs.org/learn/basics/assets-metadata-css/layout-component
import Head from 'next/head';
import Image from 'next/image';
import styles from './layout.module.css';
import utilStyles from '../styles/utils.module.css';
import Link from 'next/link';

const name = 'Tempcheck';
export const userName = '';

export default function Layout({ children, home }) {
  return (
    <div className={styles.container}>
      <Head>
        <link rel="icon" href="/favicon.ico" />
        <meta
          name="Tempcheck"
          content="Check the mood of a group of students"
        />
        <meta name="og:userName" content={userName} />
        <meta name="twitter:card" content="summary_large_image" />
      </Head>
      <header className={styles.header}>
        <>
          <Link href="/">
            <Image
              priority
              src="/images/thermometerColor.png"
              className={utilStyles.borderCircle}
              height={144}
              width={144}
              alt=""
            />
          </Link>
          <h2 className={utilStyles.heading2Xl}>
            <Link href="/" className={utilStyles.colorInherit}>
              {name}
            </Link>
          </h2>
        </>
      </header>
      <main>{children}</main>
    </div>
  );
}

