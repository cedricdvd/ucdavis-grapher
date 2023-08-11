import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';

import './styles/course.css';

function Course() {
    const [courseObj, setCourseObj] = useState({});
    const [prerequisites, setPrerequisites] = useState([]);
    const [successors, setSuccessors] = useState([]);
    const { courseCode } = useParams();

    useEffect(() => {
        axios.get(`http://localhost:8000/api/get-course/${courseCode}`)
        .then(results => {
            setCourseObj(results.data);
        })
        .catch(error => {
            console.log(error)
        });

        axios.get(`http://localhost:8000/api/get-prerequisites/${courseCode}`)
        .then(results => {
            setPrerequisites(results.data);
        })
        .catch(error => {
            console.log(error)
        });

        axios.get(`http://localhost:8000/api/get-successors/${courseCode}`)
        .then(results => {
            setSuccessors(results.data);
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
            <h2>Prerequisites</h2>
            <div className="prerequisite-list">
                {prerequisites.map((course, idx) => {
                    return (
                        <li key={idx} className={'prerequisite-course' + (course.prerequisite_id ? '' : ' disabled')}>
                            <Link to={`/course/${course.prerequisite_code}`}>
                                {course.prerequisite_code}
                            </Link>
                        </li>
                    );
                })}
            </div>
            <h2>Needed By</h2>
            <div className="successor-list">
                {successors.map((course, idx) => {
                    return (
                        <li key={idx} className={'successor-course'}>
                            <Link to={`/course/${course.course_code}`}>
                                {course.course_code}
                            </Link>
                        </li>
                    );
                })}
            </div>
        </div>
    );
};


export default Course;
