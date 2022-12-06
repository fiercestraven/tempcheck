import Head from 'next/head';
import Link from 'next/link';
import Layout from '../../../components/layout';

export default function Lecture({ lecture_detail }) {
  return (
    <Layout>
        <Head>
            <title>{lecture_detail.lecture_name}</title>
        </Head>
        <h2>{lecture_detail.module.module_name}</h2>
        <h3>Lecture: {lecture_detail.lecture_name}</h3>
        <p>{lecture_detail.lecture_date}: {lecture_detail.lecture_description}</p>

        <form action="http://localhost:8000/tcapp/api/pings/" method="post">
            <input type="submit" name="ping" id="ping" value="Ping" />
            <input type="text" name="date" value="2022-12-05T12:20:00"></input>
            <input type="number" name="student" value="16"></input>
            {/* fv - plug in page info below here */}
            <input type="number" name="lecture" value="11"></input>
        </form>

        {/* <form action="{% url 'tcapp:submit' module_name=module.module_name lecture_name=lecture.lecture_name %}" method="post">
            {% csrf_token %}
            {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
            <input type="submit" name="ping" id="ping" value="Ping">
        </form> */}

        <p></p>
        <Link href={`/modules/${lecture_detail.module.module_shortname}`}>← Back to Module</Link>
    </Layout>
);
}

Lecture.getInitialProps = async (ctx) => {
    const { lecture_name } = ctx.query;
    const res = await fetch(`http://localhost:8000/tcapp/api/lectures/${lecture_name}/`);
    const lecture_detail = await res.json()
    return { lecture_detail: lecture_detail }
  }