import Image from 'next/image';

export default function Sidebar() {
    const imageURL = "/images/rainbow_thermometer.svg"

    return (
        <div className="mb-4 copyright footer-header-info">
            <a href="/" className="header-link">
                <Image id="side-img"
                    priority
                    src={imageURL}
                    width={420}
                    height={800}
                    alt="thermometer showing a red to green colour gradient"
                />
            </a>
        </div>

    );
}
