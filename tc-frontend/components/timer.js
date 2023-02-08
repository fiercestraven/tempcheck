import { useEffect, useState } from "react";

export default function Timer() {
    const [minutes, setMinutes] = useState(2);
    const [seconds, setSeconds] = useState(0);

    useEffect(() => {
        let interval = setInterval(() => {
            if (seconds > 0) {
                setSeconds(seconds - 1);
            }

            // if the seconds timer shows zero, don't go negative, and also reset minutes
            if (seconds === 0) {
                if (minutes === 0) {
                    clearInterval(interval);
                    console.log("Clearing interval:", interval);
                } else {
                    setMinutes(minutes - 1);
                    setSeconds(59);
                }
            }
        }, 1000);
    }, []);
        

    return (
        <div>
            {/* use ternary to show seconds as two digits */}
            {minutes === 0 && seconds === 0
                ? <p></p>
                : <p className="user-message">Thanks for submitting a ping! You may ping again in: {minutes}:{seconds < 10 ? `0${seconds}` : seconds}</p>
            }
        </div>
    )

}