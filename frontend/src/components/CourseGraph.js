import React, { useRef, useEffect, useState, useMemo } from 'react';
import RootNode from './graph-nodes/RootNode.js';
import PrerequisiteNode from './graph-nodes/PrerequisiteNode.js';
import ReactFlow, { Controls } from 'reactflow';
import 'reactflow/dist/style.css';
import './styles/CourseGraph.css';


function CourseGraph({ root_course, prerequisite_arr }) {
    const ref = useRef(null);
    const [ nodes, setNodes ] = useState([]);
    const [ edges, setEdges ] = useState([]);
    const nodeTypes = useMemo(
        () => ({ rootNode : RootNode, prerequisiteNode : PrerequisiteNode }),
        []
    );


    function getData(details) {
        console.log(`Child deatils: ${details}`);
    }

    useEffect(() => {
        const width = ref.current.clientWidth;
        const xShift = Math.floor(prerequisite_arr.length / 2) - (prerequisite_arr.length % 2 === 0 ? 0.5 : 0);
        const prerequisite_nodes = prerequisite_arr.map(
            (group_arr, group_idx) => (
                {
                    id: `${group_idx + 1}`,
                    data: { group : group_arr, sendData : getData },
                    position: {x : Math.floor(width / 2) + 200 * (group_idx - xShift), y: 150 },
                    type: 'prerequisiteNode'
                }
            )
        );
        const prerequisite_edges = prerequisite_arr.map(
            (group_arr, group_idx) => (
                {
                    id: `0-${group_idx + 1}`,
                    source: '0',
                    target: `${group_idx + 1}`,
                }
            )
        );

        setNodes([
            {
                id: '0',
                data: { label : root_course.code },
                position: { x : Math.floor(width / 2), y : 50 },
                type: 'rootNode'
            },
            ...prerequisite_nodes
        ]);

        setEdges(prerequisite_edges);
    }, [ref, prerequisite_arr, root_course]);

    function addLevel() {
        return;
    };

    function removeLevel() {
        return;
    };


    return (
        <div ref={ref} className="prerequisite-map">
            <ReactFlow
                nodes={nodes}
                edges={edges}
                nodeTypes={nodeTypes}
            >
                <Controls />
            </ReactFlow>
        </div>
    );
};

export default CourseGraph;
