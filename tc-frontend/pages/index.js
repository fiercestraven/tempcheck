import Link from 'next/link';
import Layout from '../components/layout';
import Login from './login';

// function Header({ userName }) {
//   return (
//     <h2 className="mt-4 fw-normal">Welcome, {userName ? userName : 'Visitor'}!</h2>
//   );
// }

export default function HomePage() {

  return (
    <div>
      <Layout home>
        <Login />
        <Link href="/modules">Modules</Link>
        <p></p>
        <Link href="http://localhost:8000/admin">Admin</Link>
      </Layout>
    </div>
  );
}
