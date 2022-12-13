import Link from 'next/link';
import Layout from '../components/layout';
import Login from './login';

function Header({ userName }) {
  return (
    <h2 className="mt-4 fw-normal">Welcome, {userName ? userName : 'Visitor'}!</h2>
  );
}

export default function HomePage() {

  return (
    <div>
      <Layout home>
        <Header />
        <Login />
        {/* login info */}
        {/* <form action="http://localhost:8000/tcapp/dj-rest-auth/login/" method="post">
          <p className="mt-4 mb-1 font-italic">Please sign in</p>
          <div className="form-floating">
            <label for="username" className="form-label">Username</label>
            <input type="text" className="form-control" id="username" placeholder="Username" name="username" />
          </div>
          <div className="form-floating">
            <label for="password" className="form-label">Password</label>
            <input type="password" className="form-control" id="password" placeholder="Password" name="password" />
          </div>
          <button className="w-30 mt-2 mb-5 btn btn-lg btn-primary" type="submit">Log In</button>
        </form> */}
        {/* fv - make below an 'if logged in' display, and if not, display login link/button */}
        <Link href="/modules">Modules</Link>
        <p></p>
        <Link href="http://localhost:8000/admin">Admin</Link>
      </Layout>
    </div>
  );
}
