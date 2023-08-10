import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

function Course() {
    const [courseObj, setCourseObj] = useState({});
    const [prerequisites, setPrerequisites] = useState([]);
    const { courseCode } = useParams();
    useEffect(() => {
        axios.get(`http://localhost:8000/api/get-course/${courseCode}`)
        .then(results => {
            setCourseObj(results.data);
        })
        .catch(error => {
            console.log(error)
        });

        axios.get(`http://localhost:8000/api/prerequisite-details/${courseCode}`)
        .then(results => {
            setPrerequisites(results.data);
        })
        .catch(error => {
            console.log(error)
        });

    }, [courseCode]);

    return (
        <div>
            <header>Data Generated from Course Details</header>
            <hr></hr>
            <h1>{courseObj.code}</h1>
            <h2>{courseObj.title}</h2>
            <p>{courseObj.description}</p>
            <p>{courseObj.prerequisites}</p>
            <div className="prerequisite">
                {prerequisites.map((course, idx) => {
                    return <li key={idx}>{course.prerequisite_code}</li>;
                })}
            </div>
        </div>
    );
};


export default Course;
