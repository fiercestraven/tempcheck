import Link from 'next/link';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/router';

export default function Header() {
    const [profileData, setProfileData] = useState();
    const { userData, logoutUser, userDataLoaded } = useContext(CurrentUserContext);
    const router = useRouter();

    useEffect(() => {
        async function getProfileData() {
            try {
                const res = await fetch(`http://localhost:8000/tcapp/api/profile/`, {
                    headers: {
                        'Authorization': `Bearer ${userData.access_token}`,
                    },
                });
                const data = await res.json();
                setProfileData(data);
            } catch {
                pass;
            }
        }

        if (userDataLoaded && userData) {
            getProfileData();
        }
    }, [userData, router.query]);

    if (!userDataLoaded) {
        return (
            <div>Loading....</div>
        );
    }


    return (
        <div>
            <div className="footer-header-info">
                <nav className="main-nav">
                    {/* for students, nav menu only shows home link */}
                    {profileData && !profileData.is_staff &&
                        <ul>
                            <li className="index-collection active-link">
                                <Link className="nav-link" href="/">Home</Link>
                            </li>
                            <li className="page-collection logout" type={'submit'} onClick={logoutUser}>Log Out</li>
                        </ul>
                    }
                    {/* for staff, nav menu shows home, stats, and admin links */}
                    {profileData && profileData.is_staff &&
                        <ul>
                            <li className="index-collection active-link">
                                <Link className="nav-link" href="/">Home</Link>
                            </li>

                            <li className="page-collection">
                                <Link className="nav-link" href="/stats">Stats</Link>
                            </li>

                            <li className="page-collection">
                                <Link className="nav-link" href="http://localhost:8000/admin">Admin</Link>
                            </li>
                            <li className="page-collection logout nav-link" type={'submit'} onClick={logoutUser}>Log Out</li>
                        </ul>
                    }

                </nav>
            </div>

            <a className="header-link index-header" href="/">
                {/* https://stackoverflow.com/questions/14678154/centre-align-text-that-has-extra-letter-spacing-applied */}
                TEMPCHECK
            </a>

        </div >
    );
}
