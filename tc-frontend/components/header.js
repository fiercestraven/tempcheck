import Image from 'next/image';
import Link from 'next/link';
import { useState, useEffect } from 'react';

export default function Header() {
    const name = 'Tempcheck';
    const [threshold, setThreshold] = useState(0);
    const [imageURL, setImageURL] = useState("/images/thermometerGreen.png");
    
    function setTemp() {
        // fetch and set threshold info
        setThreshold(0);

        switch(threshold) {
            case 0:
                setImageURL("/images/thermometerGreen.png");
            case 1:
                setImageURL("/images/thermometerYellow.png");
            case 2:
                setImageURL("/images/thermometerOrange.png");
            case 3:
                setImageURL("/images/thermometerRed.png");
        }
    }
    
    return (
        <>
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
        </>
    );
}
