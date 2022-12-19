import { createContext, useContext, useState } from 'react';

const CurrentUserContext = createContext(null);

export function AppWrapper({ children }) {
    // will hold properties of access_token, username, token_expiry
    const [currentUser, setCurrentUser] = useState({});

    return (
        <CurrentUserContext.Provider value={{
            currentUser,
            setCurrentUser,
            }}
        >
        { children }
        </CurrentUserContext.Provider>
    );
}

export function useCurrentUserContext() {
    return useContext(CurrentUserContext);
}