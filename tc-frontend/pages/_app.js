
// add bootstrap css 
import 'bootstrap/dist/css/bootstrap.css'
// add own css
import '../styles/global.css';
import { useEffect, useContext } from "react";
import { AppWrapper } from '../context/auth';

function App({ Component, pageProps }) {
  useEffect(() => {
    import('bootstrap/dist/js/bootstrap');
  }, []);
  
  return (
    <AppWrapper>
      <Component {...pageProps} />
    </AppWrapper>
  );
  }

export default App
  