import Head from 'next/head';
import Link from 'next/link';
import Layout from '../components/layout';

export default function ModuleList() {
    return (
        <Layout>
            <Head>
                <title>Module List</title>
            </Head>
            <h1>
                List of modules
            </h1>
        </Layout>
    );
  }