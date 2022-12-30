import Head from 'next/head';
import Link from 'next/link';
import Layout from '../../../components/layout';
import { CurrentUserContext } from '../../../context/auth';
import { useContext } from 'react';

export default function Lecture({ lecture_detail }) {
    const { logoutUser } = useContext(CurrentUserContext);

    return (
        <Layout>
            <Head>
                <title>{lecture_detail.lecture_name}</title>
            </Head>
            <h2>{lecture_detail.module.module_name}</h2>
            <h3>Lecture: {lecture_detail.lecture_name}</h3>
            <p>{lecture_detail.lecture_date}: {lecture_detail.lecture_description}</p>

            {/* fv - do error handling on this form */}
            <form action="http://localhost:8000/tcapp/api/pings/" method="post">
                <input type="submit" name="ping" id="ping" value="Ping"></input>
                {/* fv - update below after auth/login finished */}
                <input type="number" name="student" value="16"></input>
                <input type="text" name="lecture_name" value={lecture_detail.lecture_name}></input>
            </form>

            <p></p>
            <Link href={`/modules/${lecture_detail.module.module_shortname}`}>← Back to Module</Link>
            <p></p>
            <Link href="/">← Home</Link>
            <p></p>
            <button className="w-30 mt-2 mb-5 btn btn-md btn-primary" type={'submit'} onClick={logoutUser}>Log Out</button>

        </Layout>
    );
}

Lecture.getInitialProps = async (ctx) => {
    const { lecture_name } = ctx.query;
    const res = await fetch(`http://localhost:8000/tcapp/api/lectures/${lecture_name}/`);
    const lecture_detail = await res.json()
    return { lecture_detail: lecture_detail }
}