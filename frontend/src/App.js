import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import NavBar from './components/NavBar';
import Footer from './components/Footer';

import Home from './pages/index';
import Course from './pages/course';
import Department from './pages/departments'
import Search from './pages/search'

import './App.css';

function App() {
      return (
        <Router>
            <NavBar />
            <main>
                <Routes>
                    <Route path='/' element={<Home />} />
                    <Route path='/departments' element={<Department />} />
                    <Route path='/course/:courseCode' element={<Course />} />
                    <Route path='/search' element={<Search />} />
                </Routes>
            </main>
            <Footer />
        </Router>
      );
}

export default App;
