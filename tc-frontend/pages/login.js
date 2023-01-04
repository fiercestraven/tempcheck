import React, { useState, useContext } from 'react';
import { CurrentUserContext } from '../context/auth';
import { useForm } from "react-hook-form";

function Login() {
    const { register, handleSubmit, formState: { errors } } = useForm();
    const [rawProfile, changeRawProfile] = useState(null);
    // const [loginError, setLoginError] = useState('');
    // const [currentUser, setCurrentUser] = CurrentUserContext();
    // const [username, changeUsername] = useState('');
    // const [password, changePassword] = useState('');
    let [loading, setLoading] = useState(false);
    // let [formError, setFormError] = useState(false);
    // get user management functions from context
    const { userData, loginUser } = useContext(CurrentUserContext);
    // const { register, handleSubmit, errors, setError, clearError } = useForm();


    async function onSubmit(e) {
        e.preventDefault();
        setLoading(true);
        console.debug(e);
        // setFormError(false);
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

            let userData = await res.json();

            // update user
            loginUser(userData);


            // show access token in console
            console.info(userData.access_token);

            // fv - will also need to put api back behind authentication. Then every request will need to include auth by accessing that same Context.
        } catch (error) {
            const { userData } = error.response;
            console.error('error ->', error);
            console.log(userData);
            userData.username && setError("username", "", userData.username);
            userData.password && setError("password", "", userData.password);
            // setFormError(true);
        }
        setLoading(false);
    }

    return (
        <div>
            <header>
                <h4 className="mt-4 mb-3">Welcome! Please sign in</h4>
                <div>
                    {/* fv - what is this next bit doing? Checking if someone is already logged in? */}
                    {rawProfile &&
                        <div className={'response'}>
                            <code>
                                {JSON.stringify(rawProfile)}
                            </code>
                        </div>
                    }
                </div>
                <div>
                    {/* fv - tried taking out curly braces for things with static strings - just curious */}
                    <form onSubmit={handleSubmit(onSubmit)}>
                        <div>
                            <div className="mr-2"><label htmlFor="username" className="form-label">Username:</label></div>
                            <input
                            // ***fv - change these onChange functions to update userData instead.... but how? should be able to use loginUser and pass the data, but where?
                                onChange={(e) => changeUsername(e.target.value)}
                                placeholder="Enter your username"
                                value={userData.username}
                                type="text"
                                name="username"
                                {...register("username", { required: true, maxLength: 50 })}
                            />
                        </div>
                        {errors.username && <p>Please check your username</p>}
                        <div>
                            <div className="mr-2"><label htmlFor="password" className="form-label">Password:</label></div>
                            <input
                                onChange={(e) => changePassword(e.target.value)}
                                placeholder="Enter your password"
                                value={userData.password}
                                type="password"
                                name="password"
                                {...register("pasword", { 
                                    required: true, 
                                    // add pattern to require 1 digit, 1 uppercase, 1 lowercase, and between 8-20 characters
                                    pattern: /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,20}$/
                                })} 
                            />
                        </div>
                        {errors.password && <p>Please check your password. It should be between 8-20 characters and contain at least one number, one uppercase letter and one lowercase letter.</p>}
                        <button className="w-30 mt-2 mb-5 btn btn-md btn-primary" type={'submit'}>Log In</button>
                    </form>
                </div>
            </header>
        </div>
    );
}

export default Login;