import { useContext } from 'react';
import Link from 'next/link';
import Layout from '../components/layout';
import Login from './login';
import { CurrentUserContext } from '../context/auth';

export default function HomePage() {
  const { userData, logoutUser, userDataLoaded } = useContext(CurrentUserContext);

  if (!userDataLoaded) {
    return (
      <div>Loading...</div>
    );
  }
  
  return (
    <div>
      <Layout home>
        {!userData.username && (
          <Login />
        )}
        {userData.username && (
          <div class="container">
            <Link href="/modules">Modules</Link>
            <p></p>
            <button className="w-30 mt-2 mb-5 btn btn-md btn-primary" type={'submit'} onClick={logoutUser}>Log Out</button>
          </div>
        )}
      </Layout>
    </div>
  );
}
