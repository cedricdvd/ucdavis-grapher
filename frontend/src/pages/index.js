import React from "react";
import SearchBar from '../components/SearchBar';
import './styles/index.css'

function Home() {
    return (
        <div className="home-page">
            <h1 className="title">CoGA: The UC Davis Course Grapher Application</h1>
            <p className="description">
                This web application is designed to help students plan their
                course schedules by providing a visual representation of the
                prerequisites.
            </p>
            <SearchBar />
            <h2>How To Use</h2>
            <p>
                To use this application, type a course code into the search bar.
                A list of courses beginning with the query will appear. Click on
                the course you want to view.
            </p>
            <h2>Notes</h2>
            <p>
                This application is still in development. If you find any bugs,
                please report them to the GitHub repository.
            </p>
        </div>
    );
}

export default Home;
