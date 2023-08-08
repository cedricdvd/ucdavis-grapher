import React from 'react';
import axios from 'axios';

class Course extends React.Component {

    state = { details : []}

    componentDidMount() {
        axios.get("http://localhost:8000/api/course-details/EAE 143A")
        .then(response => {
            this.setState({ details : response.data })
        })
        .catch(error => {
            console.log(error)
        })
    }

    render() {
        return (
            <div>
                <header>
                    Data Generated from Course Details
                </header>
                <hr></hr>
                <h1>{this.state.details.code}</h1>
                <h2>{this.state.details.title}</h2>
                <p>{this.state.details.description}</p>
                <p>{this.state.details.prerequisites}</p>
            </div>
        )
    }

}

export default Course;
