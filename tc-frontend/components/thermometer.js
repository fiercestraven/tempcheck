import Image from 'next/image';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect, useState } from 'react';

// pass in lecture name when Thermometer function called in lecture_name.js
// https://beta.reactjs.org/learn/passing-props-to-a-component
export default function Thermometer({lectureName}) {
    const { userData, userDataLoaded } = useContext(CurrentUserContext);
    const [imageURL, setImageURL] = useState("/images/thermometerGreen.png");

    useEffect(() => {
        let interval;
        async function getLectureTemp() {
            interval = setInterval(async () => {
                const res = await fetch(`http://localhost:8000/tcapp/api/lectures/${lectureName}/temperature`, {
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
            }, 2000);
        }

        if (userDataLoaded && userData.username) {
            getLectureTemp();
        }

        return () => {
            clearInterval(interval);
            console.log("Clearing interval:", interval);
        };

    }, [userData, lectureName]);

    if (!userDataLoaded) {
        return (
            <div>Loading...</div>
        );
    }

    return (
        <div>
            <Image className="header-img"
                priority
                src={imageURL}
                height={220}
                width={250}
                alt=""
            />
        </div>
    );
}
