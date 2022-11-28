import Head from 'next/head';
import Link from 'next/link';
import Image from 'next/image';
import Layout from '../../components/layout';

export default function FirstPost() {
    const ThermometerIcon = () => (
        <Image
          src="public/images/thermometerColor.png" 
          height={144} // Desired size with correct aspect ratio
          width={144} // Desired size with correct aspect ratio
          alt="A thermometer filled nearly to the top"
        />
      );

    return (
        <Layout>
            <Head>
                <title>Tempcheck: First Post</title>
            </Head>
            <img src={<ThermometerIcon />} />
            <h1>
                First Post
            </h1>
            <h2>
                <Link href="/">Back to home</Link>
            </h2>
        </Layout>
    );
  }
  