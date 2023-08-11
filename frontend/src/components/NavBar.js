import React from 'react';
import { Link } from 'react-router-dom';
import './styles/NavBar.css';

function NavBar() {
    return (
        <div className="NavBar">
            <header>
                <Link to="/">Home</Link>
                <Link to="/departments">Departments</Link>
            </header>
        </div>
    );
};

export default NavBar;
