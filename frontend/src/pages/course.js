import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';
import CourseGraph from '../components/CourseGraph';
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
            let groups = [];
            let group = [];
            let groupNum = 0;

            for (let i = 0; i < results.data.length; i++) {
                if (results.data[i].group_num === groupNum) {
                    group.push({
                        'code': results.data[i].prerequisite_code,
                        'id': results.data[i].prerequisite_id
                    });
                }
                else {
                    groups.push(group);
                    group = [{
                        'code': results.data[i].prerequisite_code,
                        'id': results.data[i].prerequisite_id
                    }];
                    groupNum = results.data[i].group_num;
                }
            }

            if (group.length > 0) {
                groups.push(group);
            }

            setPrerequisites(groups);
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
                {prerequisites.map((group, group_num) => {
                    return (
                        <div className="group-list" key={group_num}>
                            <h3>Group {group_num}</h3>
                            {
                                group.map((course, course_idx) => {
                                    return (
                                        <li key={course_idx} className={'prerequisite-course' + (course.id ? '' : ' disabled')}>
                                            <Link to={(course.id ? `/course/${course.code}` : null)}>
                                                {course.code}
                                            </Link>
                                        </li>
                                    );
                                })
                            }
                        </div>
                    );
                })}
            </div>
            <h2>Prerequisite Map</h2>
            <CourseGraph root_course={courseObj} prerequisite_arr={prerequisites} />
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
