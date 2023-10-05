import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useSearchParams, Link } from 'react-router-dom';
import './styles/search.css';
import SearchBar from '../components/SearchBar'


function Search() {
    const [searchParams] = useSearchParams();
    const [isLoading, setLoading] = useState(true);
    const courseQuery = searchParams.get('q');

    const [ details, setDetails ] = useState([]);

    useEffect(() => {
        axios.get(`http://127.0.0.1:8000/api/search-courses/${courseQuery}`)
        .then(results => {
            setDetails(results.data);
            setLoading(false);
        })
        .catch(err => {
            console.log(err);
            setLoading(false);
        });
    }, [courseQuery]);

    if (isLoading) {
        return (
            <div className="search-page">
            <h1>Search Results</h1>
            <p>{`This page contains search results for ${courseQuery}.`}</p>
            <SearchBar />
            <h2>Loading results...</h2>
        </div>
        );
    }

    return (
        <div className="search-page">
            <h1>Search Results</h1>
            <p>{`This page contains search results for ${courseQuery}.`}</p>
            <SearchBar />
            <h2>{`${details.length} result${details.length !== 1 ? 's' : '' }`}</h2>
            <div className="search-list">
                {details.map(result => (
                    <li key={result.id}>
                        <Link to={`/course/${result.code}`}>{result.code} - {result.title}</Link>
                    </li>
                ))}
            </div>
        </div>
    );
}

export default Search;
