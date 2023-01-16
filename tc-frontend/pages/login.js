import React, { useContext } from 'react';
import { CurrentUserContext } from '../context/auth';
import { useForm } from "react-hook-form";

export default function Login() {
    const { register, handleSubmit, formState: { errors } } = useForm();
    // get user management functions from context
    const { userData, loginUser } = useContext(CurrentUserContext);

    async function onSubmit(data) {
        try {
            await loginUser(data.username, data.password);
            console.log("Login complete!");
        } catch (e) {
            console.error("Login failed: ", e.message);
        }
    }

    return (
        <div>
            <header>
                {/* <h4 className="mt-4 mb-3" style={{fontStyle: 'italic'}}>Welcome! Please sign in:</h4> */}
            </header>

            <form onSubmit={handleSubmit(onSubmit)}>
                <div>
                    <div className="mr-2"><label htmlFor="username" className="form-label">Username:</label></div>
                    <input
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
                        placeholder="Enter your password"
                        value={userData.password}
                        type="password"
                        id="password"
                        name="password"
                        {...register("password", {
                            required: true,
                            // pattern to require 1 digit, 1 uppercase letter, and between 8-20 characters
                            pattern: /^(?=.*\d)(?=.*[A-Z]).{8,20}$/
                        })}
                    />
                </div>
                {errors.password && <p>Password required. Your password should be between 8-20 characters and contain at least one number and one uppercase letter.</p>}
                <button className="w-30 mt-2 mb-5 btn btn-md btn-primary" type='submit'>Login</button>
            </form>
        </div>
    );
}