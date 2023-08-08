import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Home from './pages/index';
import Course from './pages/course';

class App extends React.Component{

  render() {
      return (
        <Router>
            <Routes>
                <Route path='/' element={<Home />} />
                <Route path='/course' element={<Course />} />
            </Routes>
        </Router>
      );
  }
}

export default App;
