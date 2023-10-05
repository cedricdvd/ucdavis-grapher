import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './styles/departments.css'

function Department() {

    const [ departments, setDepartments ] = useState([]);
    const [ isLoading, setLoading ] = useState(true);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/get-subjects')
        .then(response => {
            setDepartments(response.data);
            setLoading(false);
        })
        .catch(error => {
            console.log(error)
            setLoading(false);
        });
    }, []);

    if (isLoading) {
        return (
            <div className="departments">
                <h1>Departments</h1>
                <p>
                    This page contains links to each department's respective course catalog. The page to the original catalog can be found at
                    <a href='https://catalog.ucdavis.edu/'>https://catalog.ucdavis.edu</a>
                </p>
                <h2>Loading...</h2>
            </div>
        );
    }

    return (
        <div className="departments">
            <h1>Departments</h1>
            <p>
                This page contains links to each department's respective course catalog. The page to the original catalog can be found at
                <a href='https://catalog.ucdavis.edu/'>https://catalog.ucdavis.edu</a>
            </p>
            
            <div className="departments-list">
                {departments.map((detail) => (
                    <li key={detail.id} className="department-link">
                        <a href={`https://catalog.ucdavis.edu/courses-subject-code/${detail.code.toLowerCase()}`}>
                            {`${detail.name} (${detail.code})`}
                        </a>
                    </li>
                ))}
            </div>
        </div>
    );

}

export default Department;
