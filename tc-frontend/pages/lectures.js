import Head from 'next/head';
import Link from 'next/link';
import Layout from '../components/layout';

export default function LectureList() {
    // async function getLectureData() {
    //     const res = await fetch('http://localhost:8000/tcapp/api/lectures/');
    //     console.log(res);
    //     return res.json();
    //   }
    
    // useEffect(() => {
    // getLectureData()
    // }, [])

    return (
        <Layout>
            <Head>
                <title>Lecture List</title>
            </Head>
            <h2>Lectures</h2>
          <ul>
            {/* fv - fix urls to go to correct ones, not api ones - REACT ROUTER - or use event listener which will call a component to create a lecture page */}
            {Array.prototype.map.call(Lectures, (item, i) => {
              return <li key={i}><a href={item.url}>{item.lecture_name}</a></li>
            })}
          </ul>
            <h3>
                <Link href="/modules">Modules</Link>
            </h3>
        </Layout>
    );
  }
  