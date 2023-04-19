import Head from 'next/head';
import Link from 'next/link';
import Layout from '../../../components/layout';
import Header from '../../../components/header';
import Thermometer from '../../../components/thermometer';
import Timer from '../../../components/timer';
import { CurrentUserContext } from '../../../context/auth';
import { useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { useForm } from "react-hook-form";

export default function Lecture() {
    const { register, handleSubmit, formState: { errors } } = useForm();
    const [lectureData, setLectureData] = useState();
    const [profileData, setProfileData] = useState();
    const { userData, logoutUser, userDataLoaded } = useContext(CurrentUserContext);
    // variables to show state of ping and reset buttons
    const [pingComplete, setPingComplete] = useState(false);
    const [resetComplete, setResetComplete] = useState(false);
    const [userMessage, setUserMessage] = useState(false);
    const router = useRouter();
    const { lecture_name } = router.query;

    useEffect(() => {
        async function getLectureData() {
            const res = await fetch(`http://localhost:8000/tcapp/api/lectures/${lecture_name}/`, {
                headers: {
                    'Authorization': `Bearer ${userData.access_token}`,
                },
            });
            // if student/instructor not associated with lecture, re-route to user's modules page
            if (res.status == 404) {
                router.push("/modules");
            }
            else {
                const data = await res.json();
                setLectureData(data);
            }
        }

        async function getProfileData() {
            const res = await fetch(`http://localhost:8000/tcapp/api/profile/`, {
                headers: {
                    'Authorization': `Bearer ${userData.access_token}`,
                },
            });
            const data = await res.json();
            setProfileData(data);
        }

        if (userDataLoaded && userData) {
            getProfileData();
        }

        // only get lecture data after the lecture name is resolved
        if (router.query.lecture_name) {
            getLectureData();
        }
    }, [userData, router.query]);

    if (!userDataLoaded) {
        return (
            <div>Loading....</div>
        );
    }

    if (!userData.username) {
        router.push("/");
    }

    function handleTimerComplete() {
        // Re-enable ping button after set time and remove timer
        setPingComplete(false);
    }

    async function onSubmit(data) {
        console.log(data);
        try {
            console.log('fetching');
            let url = profileData.is_staff ? `http://localhost:8000/tcapp/api/lectures/${lecture_name}/resets/` : `http://localhost:8000/tcapp/api/lectures/${lecture_name}/pings/`
            let res = await fetch(url, {
                method: 'POST',
                credentials: 'omit',
                headers: {
                    'Authorization': `Bearer ${userData.access_token}`,
                    // what mime type I'm sending & accepting
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                // no body necessary as date/time, lecture and student/instructor info is all set on the back end
            });
            console.log('checking status');
            if (res.status == 400) {
                throw new Error("An error occurred with the submission");
            }
            else if (res.status == 429) {
                setUserMessage(true);
                throw new Error("Too many submissions. One ping is allowed every two minutes.");
            }
            const result = await res.json();
            console.log(result);

            // Disable the button and timer for pings
            if (!profileData.is_staff) {
                setPingComplete(true);
            }

            // Show success message for reset
            if (profileData.is_staff) {
                setResetComplete(true);
            }

            // remove user message after set time
            setTimeout(function () {
                setResetComplete(false)
            }, 10000) // ten seconds in milliseconds
        } catch (e) {
            console.error("Submission failed: ", e.message);
        }
    }

    return (
        <Layout>
            <Head>
                <title>{lectureData?.lecture_name || "Lecture Details"}</title>
            </Head>

            <header>
                <Header />
            </header>

            <div className="container content">
                <div className="row">
                    <div className="col-6 logo">
                        {/* call Thermometer component and pass in the lecture name so it knows the correct api address */}
                        <Thermometer lectureName={lecture_name} />
                    </div>

                    {lectureData?.lecture_name &&
                        <div className="col-6">
                            <h2>{lectureData.module.module_name}</h2>
                            <h3>Lecture: {lectureData.lecture_name}</h3>
                            <p>{lectureData.lecture_date}: {lectureData.lecture_description}</p>

                            {/* show success message if reset complete */}
                            {resetComplete &&
                                <p className="user-message">You have successfully reset to the baseline temperature.</p>
                            }

                            <form onSubmit={handleSubmit(onSubmit)}>
                                <div>
                                    <input
                                        value={lectureData.lecture_name}
                                        type="hidden"
                                        id="lecture_name"
                                        name="lecture_name"
                                        {...register("lecture_name", { required: true, maxLength: 50 })}
                                    />
                                </div>
                                {errors.lecture_name && <p>Invalid lecture name submitted.</p>}

                                {/* show different buttons based on staff status */}
                                {profileData?.is_staff &&
                                    <button className="w-30 mt-2 mb-3 btn btn-md btn-light" id="ping_btn" type="submit">Reset Temp</button>
                                }

                                {/* https://sebhastian.com/react-disable-button/ */}
                                {!profileData?.is_staff &&
                                    <button className="w-30 mt-2 mb-3 btn btn-md btn-light" id="ping_btn" type="submit" disabled={pingComplete}>Ping</button>
                                }

                                {/* timer here */}
                                {pingComplete && < Timer onComplete={handleTimerComplete} />}

                                {userMessage &&
                                    <p className="user-message">Too many submissions. One ping allowed every two mintues.</p>
                                }

                            </form>
                            <p></p>
                            <Link href={`/modules/${lectureData.module.module_shortname}`}>← Back to Module</Link>
                            <p></p>
                            <button className="w-30 mt-2 mb-1 btn btn-md btn-light" type={'submit'} onClick={logoutUser}>Log Out</button>
                        </div>
                    }
                </div>
            </div>

        </Layout>
    );
}
