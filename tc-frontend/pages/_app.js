
import { useEffect } from "react";
// add bootstrap css 
import 'bootstrap/dist/css/bootstrap.css'// own css files here
// add own css
import '../styles/global.css';

function App({ Component, pageProps }) {
  useEffect(() => {
    import('bootstrap/dist/js/bootstrap');
  }, []);
  
  return <Component {...pageProps} />;
  }

export default App
  