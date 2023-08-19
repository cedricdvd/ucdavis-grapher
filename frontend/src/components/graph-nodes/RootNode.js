import { Handle, Position } from 'reactflow';
import '../styles/CourseNode.css';

function RootNode({ data }) {

    return (
        <div className="root-node">
            <div className="root-label">{data.label}</div>
            <Handle type="source" position={Position.Bottom} />
        </div>
    )
};

export default RootNode;
