import React, { useState } from 'react';

function Login() {
    const [resp, changeResponse] = useState(null);
    const [username, changeUsername] = useState('');
    const [password, changePassword] = useState('');

    function onSubmit(e) {
        e.preventDefault();
        return fetch('http://localhost:8000/tcapp/dj-rest-auth/login/', {
            method: 'POST',
            credentials: 'omit',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({ username, password })
        }).then(resp => resp.json()).then(data => {
            changeResponse(data)
        }).catch(error => console.log('error ->', error))
    }

    return (
        <div className="App">
            <header className="App-header">
                <p className="mt-4 mb-1 font-italic">Please sign in</p>
                <div>
                    {resp &&
                        <div className={'response'}>
                            <code>
                                {JSON.stringify(resp)}
                            </code>
                        </div>
                    }
                </div>
                <div>
                    <form onSubmit={onSubmit}>
                        <div>
                            <label for="username" className="form-label">Username:</label>
                            <input
                                onChange={(e) => changeUsername(e.target.value)}
                                value={username}
                                type={'input'}
                                name={'username'} />
                        </div>
                        <div>
                            <label for="password" className="form-label">Password:</label>
                            <input
                                onChange={(e) => changePassword(e.target.value)}
                                value={password}
                                type={'password'}
                                name={'password'} />
                        </div>
                        <button className="w-30 mt-2 mb-5 btn btn-lg btn-primary" type={'submit'}>Log In</button>
                    </form>
                </div>
            </header>
        </div>
    );
}

export default Login;