import { useState, useEffect, useContext } from 'react';
import Link from 'next/link';
import Layout from '../components/layout';
import Login from './login';
import { CurrentUserContext } from '../context/auth';

export default function HomePage() {
  const { userData, logoutUser } = useContext(CurrentUserContext);
  
  return (
    <div>
      <Layout home>
        {!userData.username && (
          <Login />
        )}
        {userData.username && (
          <div>
            <Link href="/modules">Modules</Link>
            <p></p>
            <Link href="http://localhost:8000/admin">Admin</Link>
            <button onClick={logoutUser}>Log Out</button>
          </div>
        )}
      </Layout>
    </div>
  );
}
