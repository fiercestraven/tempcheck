import { createContext, useEffect, useState } from 'react';

export const CurrentUserContext = createContext(null);

export function CurrentUserContextWrapper({ children }) {
    // fv - consider adding [userData] as second parameter for useEffect function in order to optimize calls to local storage
    const [userData, setUserData] = useState({});
    const [userDataLoaded, setUserDataLoaded] = useState(false);

    useEffect(() => {
        const data = JSON.parse(localStorage.getItem('userData'));
        setUserData(data || {});
        setUserDataLoaded(true);
        console.debug('Got user data.', data);
    }, []);

    async function loginUser(username, password) {
        console.debug('Attempting a login...');
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
        }));

        // Set user data   
        setUserData({
            access_token: data.access_token,
            username: data.user.username,
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