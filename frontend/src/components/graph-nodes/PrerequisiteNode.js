import { Handle, Position } from 'reactflow'; 
import '../styles/CourseNode.css';

function PrerequisiteNode ({ data }) {
    return ( 
        <div className="prerequisite-node">
            <Handle type="target" position={Position.Top} />
            {
                data.group.map((course, idx) => {
                    return <button className={"course-button" + (course.id ? '' : ' disabled')} key={idx}>{course.code}</button>;
                })
            }
            <Handle type="source" position={Position.Bottom} />
        </div>
    )
}

export default PrerequisiteNode;
