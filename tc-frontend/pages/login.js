import React, { useState, useContext } from 'react';
import { CurrentUserContext } from '../context/auth';
import { useForm } from "react-hook-form";

function Login() {
    const { register, handleSubmit, formState: { errors } } = useForm();
    const [rawProfile, changeRawProfile] = useState(null);
    // let [formError, setFormError] = useState(false);
    let [loading, setLoading] = useState(false);
    // get user management functions from context
    const { userData, loginUser } = useContext(CurrentUserContext);

    // arguments are from react-hook-form handleSubmit; first is the data, second is the event
    async function onSubmit(formData, e) {
        e.preventDefault();
        setLoading(true);
        // setFormError(false);
        try {
            const username = formData.username;
            const password = formData.password;
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
// *fv - check below against new form validation....
        } catch (error) {
            console.error('error ->', error);
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
                                // onChange={(e) => userData.username(e.target.value)}
                                placeholder="Enter your username"
                                value={userData.username}
                                type="text"
                                id="username"
                                name="username"
                                {...register("username", { required: true, maxLength: 50 })}
                            />
                        </div>
                        {errors.username && <p>Username is required and must be 50 characters or less.</p>}
                        <div>
                            <div className="mr-2"><label htmlFor="password" className="form-label">Password:</label></div>
                            <input
                                // onChange={(e) => userData.password(e.target.value)}
                                placeholder="Enter your password"
                                value={userData.password}
                                type="password"
                                id="password"
                                name="password"
                                {...register("password", { 
                                    required: true, 
                                    // add pattern to require 1 digit, 1 uppercase, 1 lowercase, and between 8-20 characters
                                    pattern: /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,20}$/
                                })} 
                            />
                        </div>
                        {errors.password && <p>Password required. Your password should be between 8-20 characters and contain at least one number, one uppercase letter and one lowercase letter.</p>}
                        <button className="w-30 mt-2 mb-5 btn btn-md btn-primary" type='submit'>Log In</button>
                    </form>
                </div>
            </header>
        </div>
    );
}

export default Login;