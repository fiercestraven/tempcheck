import Image from 'next/image';
import Link from 'next/link';

export default function Header() {
    const name = "Tempcheck";
    const image = "/images/thermometerGreen.png";

    return (
        <div>
            <Link href="/">
                <Image id="header-img"
                    priority
                    src={image}
                    height={220}
                    width={250}
                    alt=""
                />
            </Link>
            <h2 className="heading2Xl">
                <Link id="header-link" href="/">{name}</Link>
            </h2>
        </div>
    );
}
