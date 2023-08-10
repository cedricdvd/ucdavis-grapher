import React from 'react';
import axios from 'axios';

class Department extends React.Component {

    state = { details : []}

    componentDidMount() {
        axios.get("http://localhost:8000/api/get-subjects")
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
                {this.state.details.map((detail) => (
                    <li key={detail.id}>
                        {detail.name} ({detail.code})
                    </li>
                ))}
            </div>
        )
    }

}

export default Department;
