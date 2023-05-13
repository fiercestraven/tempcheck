import Image from 'next/image';
import { CurrentUserContext } from '../context/auth';
import { useContext, useEffect, useState } from 'react';

// pass in lecture name when Thermometer function called in lecture_name.js
// https://beta.reactjs.org/learn/passing-props-to-a-component
export default function Thermometer({ lectureShortName }) {
    const { userData, userDataLoaded } = useContext(CurrentUserContext);
    const [imageURL, setImageURL] = useState("/images/thermometerGreen.png");
    const [altText, setAltText] = useState("thermometer reflecting the current mood temperature of the group");

    useEffect(() => {
        let interval;
        async function getLectureTemp() {
            interval = setInterval(async () => {
                const res = await fetch(`http://localhost:8000/tcapp/api/lectures/${lectureShortName}/temperature`, {
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
                        setAltText("Thermometer showing a green colour to represent a low level of pinging");
                        break;
                    case '1':
                        setImageURL("/images/thermometerYellow.png");
                        setAltText("Thermometer showing a yellow colour to represent the first threshold level of pinging");
                        break;
                    case '2':
                        setImageURL("/images/thermometerOrange.png");
                        setAltText("Thermometer showing an orange colour to represent the second threshold level of pinging");
                        break;
                    case '3':
                        setImageURL("/images/thermometerRed.png");
                        setAltText("Thermometer showing a red colour to represent the highest level of pinging");
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

    }, [userData, lectureShortName]);

    if (!userDataLoaded) {
        return (
            <div>Loading...</div>
        );
    }

    return (
        <Image id="thermometer-img"
            priority
            src={imageURL}
            width={280}
            height={700}
            alt={altText}
        />
    );
}
