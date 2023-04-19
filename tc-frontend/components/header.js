import Image from 'next/image';
import Link from 'next/link';

export default function Header() {
    const name = "Tempcheck";
    const imageURL = "/images/gradient-fully-saturated.jpg"

    return (
        <div>
            <div>
                <a id="index-header" href="/modules">
                    {/* https://stackoverflow.com/questions/14678154/centre-align-text-that-has-extra-letter-spacing-applied */}
                    TEMPCHECK
                </a>
            </div>

            <div>
                <Image id="header-img"
                    priority
                    src={imageURL}
                    height={20}
                    width={1800}
                    alt="temperature gradient from green to red"
                />
            </div>
        </div>
    );
}
