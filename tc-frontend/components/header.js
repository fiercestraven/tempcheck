import Image from 'next/image';
import Link from 'next/link';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect, useState } from 'react';
// fv - ultimate plan here is to create a header component NOT included in the layout and use it on every page except lecture_name.js, where this current code will get repurposed

export default function Header() {
    const name = 'Tempcheck';
    const { userData, userDataLoaded } = useContext(CurrentUserContext);
    const [imageURL, setImageURL] = useState("/images/thermometerGreen.png");

    // fv - move this into lecture_name.js and put different header image here....
    useEffect(() => {
        async function getLectureTemp() {
            let res = await fetch('http://localhost:8000/tcapp/api/lectures/CS270_W1_L1/temperature', {
                headers: {
                    'Authorization': `Bearer ${userData.access_token}`,
                },
            });
            // use res.text() since output of this api is a single digit and not json
            // https://developer.mozilla.org/en-US/docs/Web/API/Response/text
            let data = await res.text();
            console.log(data);

            switch (data) {
                case '0':
                    setImageURL("/images/thermometerGreen.png");
                    break;
                case '1':
                    setImageURL("/images/thermometerYellow.png");
                    break;
                case '2':
                    setImageURL("/images/thermometerOrange.png");
                    break;
                case '3':
                    setImageURL("/images/thermometerRed.png");
                    break;
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
            <Link href="/">
                <Image className="header-img"
                    priority
                    src={imageURL}
                    height={220}
                    width={250}
                    alt=""
                />
            </Link>
            <h2 className="heading2Xl">
                <Link href="/">{name}</Link>
            </h2>
        </div>
    );
}
