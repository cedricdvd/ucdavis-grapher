import React, { useState, useEffect } from 'react';
import axios from 'axios';

import { useSearchParams, Link } from 'react-router-dom';

function Search() {
    const [searchParams] = useSearchParams();
    const courseQuery = searchParams.get('q');

    const [ details, setDetails ] = useState([]);

    useEffect(() => {
        axios.get(`http://localhost:8000/api/search-courses/${courseQuery}`)
        .then(results => {
            setDetails(results.data);
        })
        .catch(err => {
            console.log(err);
        });
    }, [courseQuery]);

    return (
        <div>
            {details.map(result => (
                <li key={result.id}>
                    <Link to={`/course/${result.code}`}>{result.code} - {result.title}</Link>
                </li>
            ))}
        </div>
    );
}

export default Search;
