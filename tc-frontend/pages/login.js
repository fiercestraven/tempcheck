import React, { useState } from 'react';

function Login() {
    const [resp, changeResponse] = useState(null);
    const [username, changeUsername] = useState('');
    const [password, changePassword] = useState('');

    async function onSubmit(e) {
        e.preventDefault();
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
                throw new Error(`Something went wrong! HTTP Status: ${res.status}`);
            }
            let data = await res.json();
            changeResponse(data);
            // show access token in console
            console.info(data.access_token);
            // FV START HERE store access token - use React Context to stash it. Will go away when refreshing page or navigating to new page. Initalize to put into local storage to persist it?
            // if successful, 'redirect' - change to modules page (make modules & other pages auth restricted)
            // fv - will also need to put api back behind authentication. Then every request will need to include auth by accessing that same Context.
        } catch (error) {
            console.error('error ->', error);
        }

    }

    return (
        <div>
            <header>
                <h4 className="mt-4 mb-3">Welcome! Please sign in</h4>
                <div>
                    {/* fv - here put possible messages (error)*/}
                    {resp &&
                        <div className={'response'}>
                            <code>
                                {JSON.stringify(resp)}
                            </code>
                        </div>
                    }
                    {/* fv - do similar to above, but instead of 'resp &&' do 'if error message &&' and show a different message */}
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