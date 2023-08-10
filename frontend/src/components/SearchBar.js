import React, { useState } from 'react';
// import axios from 'axios';
import { useNavigate } from 'react-router-dom';

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
        <div className="input-wrapper">
            <input placeholder="Type to search..."
                value={input}
                onChange={(e) => handleChange(e)}
                onKeyDown={(e) => handleKeyDown(e)}
            />
        </div>
    )
}

export default SearchBar;
