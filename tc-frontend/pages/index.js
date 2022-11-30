import Link from 'next/link';
import Layout from '../components/layout';

function Header({userName}) {
  return (
    <h2>Welcome, {userName ? userName : 'Visitor'}!</h2>
  );
}

export default function HomePage() {
  // const names = ['Ada Lovelace', 'Grace Hopper', 'Margaret Hamilton'];
  // const [likes, setLikes] = useState(0);

  // function handleClick() {
  //   setLikes(likes + 1);
  // }

  return (
    <div>
      <Layout home>
        <Header />
        {/* <ul>
          {names.map((name) => (
            <li key={name}>{name}</li>
          ))}
        </ul>
        <button onClick={handleClick}>Like ({likes})</button> */}
        <h3>
          <Link href="/modules">Modules</Link>
        </h3>
        <break />
        <h3>
          <Link href="http://localhost:8000/admin">Admin</Link>
        </h3>
      </Layout>
    </div>
  );
}
