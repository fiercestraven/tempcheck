import Image from 'next/image';
import Link from 'next/link';

export default function Header() {
    const name = 'Tempcheck';

    return (
        <>
            <Link href="/">
                <Image
                    priority
                    src="/images/thermometerColor.png"
                    height={144}
                    width={144}
                    alt=""
                />
            </Link>
            <h2 className="heading2XL">
                <Link href="/"
                // className={utilStyles.colorInherit}
                >
                    {name}
                </Link>
            </h2>
        </>
    );
}
