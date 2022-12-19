
// add bootstrap css 
import 'bootstrap/dist/css/bootstrap.css'
// add own css
import '../styles/global.css';
import { useEffect, useContext } from "react";
import { CurrentUserContextProvider } from '../context/auth';

function App({ Component, pageProps }) {
  useEffect(() => {
    import('bootstrap/dist/js/bootstrap');
  }, []);
  
  return (
    <CurrentUserContextProvider>
      <Component {...pageProps} />
    </CurrentUserContextProvider>
  );
  }

export default App
  