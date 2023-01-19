import Image from 'next/image';
import Link from 'next/link';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect, useState } from 'react';

export default function Header() {
    const name = 'Tempcheck';
    const { userData, userDataLoaded } = useContext(CurrentUserContext);
    const [threshold, setThreshold] = useState('0');
    const [imageURL, setImageURL] = useState("/images/thermometerGreen.png");

    useEffect(() => {
        // fetch and set threshold info
        async function getLectureTemp() {
            let res = await fetch('http://localhost:8000/tcapp/api/lecture_temp', {
                headers: {
                    'Authorization': `Bearer ${userData.access_token}`,
                },
            });
            let data = await res.json();
            setThreshold(data);
            console.log(data);

            switch (threshold) {
                case '0':
                    setImageURL("/images/thermometerGreen.png");
                case '1':
                    setImageURL("/images/thermometerYellow.png");
                case '2':
                    setImageURL("/images/thermometerOrange.png");
                case '3':
                    setImageURL("/images/thermometerRed.png");
            }
        }

        if (userDataLoaded && userData.username) {
            getLectureTemp();
        }
    }, [userData]);

    // fv ask Dan - omit this check? We want the defaults to show if no user logged in. Took out auto-re-route to login page already
    if (!userDataLoaded) {
        return (
            <div>Loading...</div>
        );
    }

    return (
        <div>
            {/* fv - could omit the imageURL check && here since there's a default one given */}
            {imageURL &&
                <div>
                    <Link href="/">
                        <Image className="header-img"
                            priority
                            src={imageURL}
                            height={220}
                            width={250}
                            alt=""
                        />
                    </Link>
                    <h2 className="heading2XL">
                        <Link href="/">{name}</Link>
                    </h2>
                </div>
            }
        </div>
    );
}
