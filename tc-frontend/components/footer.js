
function Copyright() {
    return (
        <div>

            <a className="fancy-link" href="https://github.com/fiercestraven/tempcheck/">Frances Veit </a>
            <>|{' ©'} {new Date().getFullYear()}</>
        </div>
    );
}

export default function Footer() {
    return (
        <div className="mb-4 copyright footer-header-info">
            <Copyright />
        </div>

    );
}