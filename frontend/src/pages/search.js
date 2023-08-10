import React, { useState, useEffect } from 'react';
import axios from 'axios';

import { useSearchParams } from 'react-router-dom';

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
                <li key={result.id}>{result.code}</li>
            ))}
        </div>
    );
}

export default Search;
