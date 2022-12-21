import { createContext, useEffect, useState } from 'react';

export const CurrentUserContext = createContext(null);

export function CurrentUserContextWrapper({ children }) {
    // fv - consider adding [userData] as second parameter for useEffect function in order to optimize calls to local storage
    const [userData, setUserData] = useState({});
    useEffect(() => {
        const data = JSON.parse(localStorage.getItem('userData'));
        setUserData(data || {});
        console.debug('Got user data.', data);
    }, []);

    const loginUser = (data) => {
        console.debug('Trying to log person in...', data);
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
            loginUser, 
            logoutUser, 
            }}
        >
            {children}
        </CurrentUserContext.Provider>
    );
}