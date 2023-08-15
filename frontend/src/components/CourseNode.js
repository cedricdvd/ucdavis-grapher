import React from 'react';
import './styles/CourseNode.css';

function CourseNode({group_arr, group_idx}) {

    return (
        <div className="course-node">
            {group_arr.map((course, idx) => {
               return (
                   <button className={"course-button" + (course.id ? "" : " disabled")}>{course.code}</button>
               );
            })}
        </div>
    )
}

export default CourseNode;
