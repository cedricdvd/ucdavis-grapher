import React from 'react';
import { Link } from 'react-router-dom';
import './styles/NavBar.css';

function NavBar() {
    return (
        <header>
            <div className="nav-title">
                <Link to="/" className="nav-title-link">CoGA</Link>
            </div>
            <div className="nav-links">
                <Link to="/" className="nav-link">Home</Link>
                <Link to="/departments" className="nav-link">Departments</Link>
            </div>
        </header>
    );
};

export default NavBar;
