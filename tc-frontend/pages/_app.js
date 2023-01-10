
// add bootstrap css 
import 'bootstrap/dist/css/bootstrap.css'
// add own css
import '../styles/global.css';
import { useEffect } from "react";
import { CurrentUserContextWrapper } from '../context/auth';

function App({ Component, pageProps }) {
  useEffect(() => {
    import('bootstrap/dist/js/bootstrap');
  }, []);
  
  return (
    <CurrentUserContextWrapper>
      <Component {...pageProps} />
    </CurrentUserContextWrapper>
  );
  }

export default App;
  