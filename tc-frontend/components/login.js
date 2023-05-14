import React, { useContext, useState } from 'react';
import { CurrentUserContext } from '../context/auth';
import { useForm } from "react-hook-form";

export default function Login() {
    // set up for react-hook-form form and error handling
    const { register, handleSubmit, formState: { errors } } = useForm();
    const [userMsg, setUserMsg] = useState(null);
    // get user management functions from context
    const { userData, loginUser } = useContext(CurrentUserContext);

    async function onSubmit(data) {
        try {
            await loginUser(data.username, data.password);
        } catch (e) {
            console.error("Login failed: ", e.message);
            // print message to user
            setUserMsg("Invalid login credentials");
        }
    }

    return (
        <div className="container content">
            <form onSubmit={handleSubmit(onSubmit)}>
                <div>
                    <div className="mr-2 form=label"><label htmlFor="username">Username:</label></div>
                    <input
                        className="input-box"
                        // placeholder="Enter your username"
                        value={userData.username}
                        type="text"
                        id="username"
                        name="username"
                        {...register("username", { required: true, minLength: 5, maxLength: 50 })}
                    />
                </div>
                {errors.username && <p>Username is required and must be between 5-50 characters.</p>}
                <div>
                    <div className="mr-2 mt-2 mb-0 form-label"><label htmlFor="password">Password:</label></div>
                    <input
                        className="input-box"
                        // placeholder="Enter your password"
                        value={userData.password}
                        type="password"
                        id="password"
                        name="password"
                        {...register("password", { required: true, })}
                    />
                </div>
                {errors.password && errors.password.type === "required" && (
                    <div className="error">Password required</div>
                )}
                {errors.password && errors.password.type === "minLength" && (
                    <div className="error">Your password should be between 8-20 characters and contain at least one number and one uppercase letter.</div>
                )}
                {/* possible error message */}
                {userMsg && (<p className="user-message">{userMsg}</p>)}
                <button className="w-30 mt-4 mb-5 btn btn-md" type="submit">Login</button>
            </form>
        </div>
    );
}