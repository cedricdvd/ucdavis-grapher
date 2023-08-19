import React, { useRef, useEffect, useState, useMemo } from 'react';
import RootNode from './graph-nodes/RootNode.js';
import PrerequisiteNode from './graph-nodes/PrerequisiteNode.js';
import ReactFlow, { Background, Controls } from 'reactflow';
import 'reactflow/dist/style.css';
import './styles/CourseGraph.css';


function CourseGraph({ root_course, prerequisite_arr }) {
    const [ width, setWidth ] = useState(0);
    const [ xShift, setXShift ] = useState(0);
    const ref = useRef(null);

    useEffect(() => {
        setWidth(ref.current.clientWidth);
        setXShift(Math.floor(prerequisite_arr.length / 2) - (prerequisite_arr.length % 2 === 0 ? 0.5 : 0));
    }, [prerequisite_arr]);

    const nodeTypes = useMemo(() => ({ rootNode : RootNode, prerequisiteNode: PrerequisiteNode }), []);

    let initialNodes = [{
        id: '0',
        data: {label : root_course.code },
        position: {x: Math.floor(width / 2), y: 50},
        type: 'rootNode',
    }];

    let initialEdges = []

    let group_num = 0;
    prerequisite_arr.forEach((group_arr) => {
        initialNodes.push(
            {
                id: `${group_num + 1}`,
                data: {group : group_arr },
                position: {x: Math.floor(width / 2) + (200 * (group_num - xShift)), y: 150},
                type: 'prerequisiteNode'
            }
        );
        initialEdges.push(
            {id: `0-${group_num + 1}$`, source: '0', target: `${group_num + 1}`}
        )
        group_num++;
    })


    return (
        <div ref={ref} className="prerequisite-map">
            <ReactFlow nodes={initialNodes} edges={initialEdges} nodeTypes={nodeTypes} >
                <Background />
                <Controls />
            </ReactFlow>
        </div>

    );
};

export default CourseGraph;
