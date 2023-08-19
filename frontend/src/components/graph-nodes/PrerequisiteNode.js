import React, { useState } from 'react';
import { Handle, Position } from 'reactflow'; 
import '../styles/CourseNode.css';
import axios from 'axios';

function PrerequisiteNode ({ data }) {
    const [ prerequisiteId, setPrerequisiteId ] = useState(-1);

    function handleClick(courseObj, idx) {
        if (courseObj.id === null) {
            return;
        }

        if (prerequisiteId === idx) {
            setPrerequisiteId(-1);
            return;
        }
        setPrerequisiteId(idx);

        axios.get(`http://localhost:8000/api/get-prerequisites/${courseObj.code}`)
        .then(results => {

            let groups = [];
            let group = [];
            let groupNum = 0;

            for (let i = 0; i < results.data.length; i++) {
                if (results.data[i].group_num === groupNum) {
                    group.push({
                        'code': results.data[i].prerequisite_code,
                        'id': results.data[i].prerequisite_id
                    });
                }
                else {
                    groups.push(group);
                    group = [{
                        'code': results.data[i].prerequisite_code,
                        'id': results.data[i].prerequisite_id
                    }];
                    groupNum = results.data[i].group_num;
                }
            }

            if (group.length > 0) {
                groups.push(group);
            }

            data.sendData(groups);
        })
        .catch(error => {
            console.log(error);
        });

    }

    return ( 
        <div className="prerequisite-node">
            <Handle type="target" position={Position.Top} />
            {
                data.group.map((course, idx) => {
                    return <button className={"course-button" + (course.id ? '' : ' disabled')} key={idx} onClick={() => handleClick(course, idx)}>{course.code}</button>;
                })
            }
            <Handle type="source" position={Position.Bottom} />
        </div>
    )
}

export default PrerequisiteNode;
