import React, { useContext, useState } from 'react';
import { CurrentUserContext } from '../context/auth';
import { useForm } from "react-hook-form";

export default function Login() {
    const { register, handleSubmit, formState: { errors } } = useForm();
    const [userMsg, setUserMsg] = useState(null);
    // get user management functions from context
    const { userData, loginUser } = useContext(CurrentUserContext);

    async function onSubmit(data) {
        try {
            await loginUser(data.username, data.password);
            console.log("Login complete!");
        } catch (e) {
            console.error("Login failed: ", e.message);
            // print message to user
            setUserMsg("Invalid login credentials");
        }
    }

    return (
        <div>
            <form onSubmit={handleSubmit(onSubmit)}>
                <div>
                    <div className="mr-2 form=label"><label htmlFor="username">Username:</label></div>
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
                    <div className="mr-2 mt-2 mb-0 form-label"><label htmlFor="password">Password:</label></div>
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
                {errors.password && errors.password.type === "required" && (
                    <div className="error">Password required</div>
                )}
                {errors.password && errors.password.type === "minLength" && (
                    <div className="error">Your password should be between 8-20 characters and contain at least one number and one uppercase letter.</div>
                )}
                {/* possible error message */}
                {userMsg && (<p className="user-message">{userMsg}</p>)}
                <button className="w-30 mt-4 mb-5 btn btn-md btn-light" type="submit">Login</button>
            </form>
        </div>
    );
}