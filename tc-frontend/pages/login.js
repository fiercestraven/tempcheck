import React, { useState, useContext } from 'react';
import { CurrentUserContext } from '../context/auth';

function Login() {
    const [rawProfile, changeRawProfile] = useState(null);
    // const [loginError, setLoginError] = useState('');
    // const [currentUser, setCurrentUser] = CurrentUserContext();
    const [username, changeUsername] = useState('');
    const [password, changePassword] = useState('');
    let [loading, setLoading] = useState(false);
    let [formError, setFormError] = useState(false);
    // get user management functions from context
    const { userData, loginUser } = useContext(CurrentUserContext);
    // const { register, handleSubmit, errors, setError, clearError } = useForm();


    async function onSubmit(e) {
        e.preventDefault();
        setLoading(true);
        setFormError(false);
        // clearError();
        try {
            let res = await fetch('http://localhost:8000/tcapp/dj-rest-auth/login/', {
                method: 'POST',
                credentials: 'omit',
                headers: {
                    // what mime type I'm sending
                    'Content-Type': 'application/json',
                    // what mime type I'm accepting back
                    'Accept': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });

            if (!res.ok) {
                // fv - could set up error message state variable and change depending on situation
                // prompt for better inputs
                setError(`Something went wrong! HTTP Status: ${res.status}`);
            }

            let data = await res.json();

            // update user
            loginUser(data);
            
            // fv - add message to user here

            // show access token in console
            console.info(data.access_token);

            // fv - will also need to put api back behind authentication. Then every request will need to include auth by accessing that same Context.
        } catch (error) {
            const { data } = error.response;
            console.error('error ->', error);
            console.log(data);
            data.username && setError("username", "", data.username);
            data.password && setError("password", "", data.password);
            setFormError(true);
        }
        setLoading(false);
    }

    return (
        <div>
            <header>
                <h4 className="mt-4 mb-3">Welcome! Please sign in</h4>
                <div>
                    {/* fv - here put possible messages (error) - see:? https://dev.to/mgranados/how-to-build-a-simple-login-with-nextjs-and-react-hooks-255*/}
                    {rawProfile &&
                        <div className={'response'}>
                            <code>
                                {JSON.stringify(rawProfile)}
                            </code>
                        </div>
                    }
                    {/* fv - do similar to above, but instead of 'rawProfile &&' do 'if error message &&' and show a different message */}
                </div>
                <div>
                    {/* fv - if time, try taking out curly braces for things with static strings - just curious */}
                    <form onSubmit={onSubmit}>
                        <div>
                            <div className="mr-2"><label htmlFor="username" className="form-label">Username:</label></div>
                            <input
                                onChange={(e) => changeUsername(e.target.value)}
                                value={username}
                                type={'input'}
                                name={'username'} />
                        </div>
                        <div>
                            <div className="mr-2"><label htmlFor="password" className="form-label">Password:</label></div>
                            <input
                                onChange={(e) => changePassword(e.target.value)}
                                value={password}
                                type={'password'}
                                name={'password'} />
                        </div>
                        <button className="w-30 mt-2 mb-5 btn btn-md btn-primary" type={'submit'}>Log In</button>
                    </form>
                </div>
            </header>
        </div>
    );
}

export default Login;