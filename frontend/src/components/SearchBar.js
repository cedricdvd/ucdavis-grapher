import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './styles/SearchBar.css';

function SearchBar() {
    const [input, setInput] = useState('');
    const navigate = useNavigate();

    function handleChange(event) {
        setInput(event.target.value);
    };

    function handleKeyDown(event) {
        if (event.key === 'Enter') {
            console.log(input);
            let query = input.trim()
            if (query.length > 0) {
                navigate(`/search?q=${encodeURIComponent(query)}`);
            }
        }
    }

    return (
        <div className="search-bar">
            <input placeholder="Search for a course..."
                value={input}
                onChange={(e) => handleChange(e)}
                onKeyDown={(e) => handleKeyDown(e)}
            />
        </div>
    )
}

export default SearchBar;
