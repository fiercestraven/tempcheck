import { createContext, useEffect, useState } from 'react';

export const CurrentUserContext = createContext(null);

export function CurrentUserContextWrapper({ children }) {
    const [userData, setUserData] = useState({});
    const [userDataLoaded, setUserDataLoaded] = useState(false);

    useEffect(() => {
        const data = JSON.parse(localStorage.getItem('userData'));
        setUserData(data || {});
        setUserDataLoaded(true);
        // fv - consider adding [userData] as a dependency for useEffect function in order to optimize calls to local storage
    }, []);

    async function loginUser(username, password) {
        let res = await fetch('http://localhost:8000/tcapp/dj-rest-auth/login/', {
            method: 'POST',
            credentials: 'omit',
            headers: {
                // what mime type I'm sending & accepting
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });

        if (res.status == 400) {
            throw new Error("Incorrect username or password");
        }

        let data = await res.json();

        // Save the user object in local storage
        localStorage.setItem('userData', JSON.stringify({
            access_token: data.access_token,
            username: data.user.username,
            first_name: data.user.first_name,
        }));

        // Set user data   
        setUserData({
            access_token: data.access_token,
            username: data.user.username,
            first_name: data.user.first_name,
        });
    };

    const logoutUser = () => {
        localStorage.removeItem('userData');
        // Empty user data state
        setUserData({});
        // fv - add user message here
    };

    return (
        <CurrentUserContext.Provider value={{
            userData,
            userDataLoaded,
            loginUser,
            logoutUser,
        }}
        >
            {children}
        </CurrentUserContext.Provider>
    );
}