import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';

import './styles/course.css';

function Course() {
    const [courseObj, setCourseObj] = useState({});
    const [prerequisites, setPrerequisites] = useState([]);
    const [successors, setSuccessors] = useState([]);
    const [isLoading, setLoading] = useState(true);
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
            setLoading(false);
        })
        .catch(error => {
            console.log(error)
            setLoading(false);
        });
    }, [courseCode]);

    if (isLoading) {
        return (
            <div className="course-page">
                <h1>Loading...</h1>
            </div>
        );
    }

    return (
        <div className="course-page">
            <h1>{`${courseObj.code} - ${courseObj.title}`}</h1>
            <p>{`${courseObj.description}${(prerequisites.length) ? ` ${courseObj.prerequisites}.` : ''}`}</p>
            <h2>{prerequisites.length ? 'Prerequisites' : null }</h2>
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
            <h2>{successors.length ? 'Needed By' : null }</h2>
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
