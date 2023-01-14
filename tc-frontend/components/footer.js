import Link from 'next/link';

function Copyright() {
    return (
        <div>
            {/* {'©'} */}
            <a href="https://github.com/fiercestraven/tempcheck/">Frances Veit </a>
            <>| { new Date().getFullYear() }</>
        </div>
    );
}

export default function Footer() {
    return (
        <div>
            <p></p>
            <Link href="http://localhost:8000/admin">Admin</Link>
            <p></p>

            <div>
                <Copyright />
            </div>
        </div>
    );
}
