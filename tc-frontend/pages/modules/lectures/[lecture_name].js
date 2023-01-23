import Head from 'next/head';
import Link from 'next/link';
import Layout from '../../../components/layout';
import Thermometer from '../../../components/thermometer';
import { CurrentUserContext } from '../../../context/auth';
import { useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { useForm } from "react-hook-form";

export default function Lecture() {
    const { register, handleSubmit, formState: { errors } } = useForm();
    const [lectureData, setLectureData] = useState();
    const [submittedText, setSubmittedText] = useState(null);
    const { userData, logoutUser, userDataLoaded } = useContext(CurrentUserContext);
    const [disable, setDisable] = useState(false);
    const router = useRouter();
    const { lecture_name } = router.query;

    useEffect(() => {
        async function getLectureData() {
            const res = await fetch(`http://localhost:8000/tcapp/api/lectures/${lecture_name}/`, {
                headers: {
                    'Authorization': `Bearer ${userData.access_token}`,
                },});
            const data = await res.json();
            setLectureData(data);
        }

        if (userDataLoaded && userData) {
            getLectureData();
        }
    }, [userData, router.query]);

    if (!userDataLoaded) {
        return (
            <div>Loading....</div>
        );
    }

    if (!userData.username) {
        router.push('/');
    }

    async function onSubmit(data) {
        console.log(data);
        try {
            console.log('fetching');
            let res = await fetch('http://localhost:8000/tcapp/api/pings/', {
                method: 'POST',
                credentials: 'omit',
                headers: {
                    'Authorization': `Bearer ${userData.access_token}`,
                    // what mime type I'm sending & accepting
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                body: JSON.stringify({
                    // student and date/time are completely handled in Django, but lecture_name must be included so Django knows which object to pull
                    lecture_name: data.lecture_name,
                })
            });
            console.log('checking status');
            if (res.status == 400) {
                throw new Error("An error occurred with the Ping submission");
            }    
            // fv - omit later?
            const result = await res.json();
            console.log(result);
            setSubmittedText("Ping successfully submitted! You may ping again in two minutes.");

            // Disable the button
            setDisable(true);

            setTimeout(function () {
                // Re-enable ping button after set time
                setDisable(false)
            }, 120000) // two minutes in milliseconds
        } catch (e) {
            console.error("Ping submission failed: ", e.message);
        }
    }

    return (
        <Layout>
            <Head>
                <title>{lectureData?.lecture_name || "Lecture Details"}</title>
            </Head>

            <div>
                <Thermometer />
            </div>

            {lectureData?.lecture_name &&
                <div className="container">
                    <h2>{lectureData.module.module_name}</h2>
                    <h3>Lecture: {lectureData.lecture_name}</h3>
                    <p>{lectureData.lecture_date}: {lectureData.lecture_description}</p>

                    {submittedText && (<p className="user-message">{submittedText}</p>)}
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

                        <button className="w-30 mt-2 mb-5 btn btn-md btn-primary" id="ping_btn" type="submit" disabled={disable}>Ping</button>
                    </form>
                    <p></p>
                    <Link href={`/modules/${lectureData.module.module_shortname}`}>← Back to Module</Link>
                    <p></p>
                    <Link href="/">← Home</Link>
                    <p></p>
                    <button className="w-30 mt-2 mb-5 btn btn-md btn-primary" type={'submit'} onClick={logoutUser}>Log Out</button>
                </div>
            }
        </Layout>
    );
}
