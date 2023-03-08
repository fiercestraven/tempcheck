import Link from 'next/link';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/router';

function Copyright() {
    return (
        <div>
            {/* {'©'} */}
            <a href="https://github.com/fiercestraven/tempcheck/">Frances Veit </a>
            <>| {new Date().getFullYear()}</>
        </div>
    );
}

export default function Footer() {
    const [profileData, setProfileData] = useState();
    const { userData, userDataLoaded } = useContext(CurrentUserContext);
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
            {profileData && profileData.is_staff &&
                <div>
                    <Link href="/">Stats</Link>
                </div>
            }

            <p></p>
            <Link href="http://localhost:8000/admin">Admin</Link>
            <p></p>

            <div>
                <Copyright />
            </div>
        </div>
    );
}
