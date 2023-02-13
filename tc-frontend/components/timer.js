import { useEffect, useState } from "react";
import useInterval from '../lib/useInterval.js';

export default function Timer({onComplete}) {
    const [minutes, setMinutes] = useState(2);
    const [seconds, setSeconds] = useState(0);
    const [delay, setDelay] = useState(1000);

    useInterval(() => {
        if (seconds > 0) {
            setSeconds(seconds - 1);
        }

        // if the seconds timer shows zero, don't go negative, and also reset minutes
        if (seconds === 0) {
            if (minutes === 0) {
                setDelay(null);
                setMinutes(2);
                setSeconds(0);
                onComplete && onComplete();
            } else {
                setMinutes(minutes - 1);
                setSeconds(59);
            }
        }
    }, delay);

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