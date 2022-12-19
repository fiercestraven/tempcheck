import { createContext, useState } from 'react';

export const CurrentUserContext = createContext(null);

export default function CurrentUserContextProvider({ children }) {
    const currentUser = JSON.parse(localStorage.getItem('userData')) || {};
    const [userData, setUserData] = useState(currentUser);

    const loginUser = (data) => {
        // Save the user object in local storage
        localStorage.setItem('userData', JSON.stringify({
            access_token: data.access_token,
            username: data.username,
        }));
        // Set user data   
        setUserData({
            access_token: data.access_token,
            username: data.username,
        });
    };

    const logoutUser = () => {
        localStorage.removeItem('userData');
        // Empty user data state
        setUserData({});
        // fv - add user message here
    };

            // Set user data 
            setUserData({
                access_token: localUser.access_token,
                username: localUser.username,
            });  


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