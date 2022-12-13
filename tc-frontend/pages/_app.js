
// add bootstrap css 
import 'bootstrap/dist/css/bootstrap.css'
// add own css
import '../styles/global.css';
import { useEffect } from "react";

function App({ Component, pageProps }) {
  useEffect(() => {
    import('bootstrap/dist/js/bootstrap');
  }, []);
  
  return <Component {...pageProps} />;
  }

export default App
  