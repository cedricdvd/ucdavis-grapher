import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function Department() {

    const [ departments, setDepartments ] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:8000/api/get-subjects')
        .then(response => {
            setDepartments(response.data);
        })
        .catch(error => {
            console.log(error)
        });
    }, []);


    return (
        <div>
            <header>
                Data Generated from Course Details
            </header>
            <hr></hr>
            {departments.map((detail) => (
                <li key={detail.id}>
                    <Link to={`https://catalog.ucdavis.edu/courses-subject-code/${detail.code.toLowerCase()}`}>
                        {detail.name} ({detail.code})
                    </Link>
                </li>
            ))}
        </div>
    );

}

export default Department;
