'use client';

import { useCallback, useMemo } from 'react';
import ReactFlow, {
  Node,
  Edge,
  addEdge,
  Connection,
  useNodesState,
  useEdgesState,
  Controls,
  Background,
  BackgroundVariant,
  NodeTypes,
  EdgeTypes,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Node as MindMapNode } from '@/lib/api';
import { CustomNode } from './custom-node';
import { CustomEdge } from './custom-edge';

interface MindMapFlowProps {
  nodes: MindMapNode[];
  onNodeClick?: (node: MindMapNode) => void;
  onNodeUpdate?: (nodeId: number, updates: Partial<MindMapNode>) => void;
}

const nodeTypes: NodeTypes = {
  custom: CustomNode,
};

const edgeTypes: EdgeTypes = {
  custom: CustomEdge,
};

export function MindMapFlow({ nodes, onNodeClick, onNodeUpdate }: MindMapFlowProps) {
  const [reactFlowNodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  // Convert API nodes to ReactFlow nodes
  const flowNodes: Node[] = useMemo(() => {
    return nodes.map((node) => ({
      id: node.id.toString(),
      type: 'custom',
      position: {
        x: node.position_x || Math.random() * 400,
        y: node.position_y || Math.random() * 400,
      },
      data: {
        ...node,
        onClick: () => onNodeClick?.(node),
        onUpdate: (updates: Partial<MindMapNode>) => onNodeUpdate?.(node.id, updates),
      },
      style: {
        backgroundColor: node.color || '#3B82F6',
        border: '2px solid #1E40AF',
        borderRadius: '8px',
        color: 'white',
        fontSize: '14px',
        fontWeight: '600',
      },
    }));
  }, [nodes, onNodeClick, onNodeUpdate]);

  // Generate edges based on parent-child relationships
  const flowEdges: Edge[] = useMemo(() => {
    const edges: Edge[] = [];
    
    nodes.forEach((node) => {
      if (node.parent_id) {
        edges.push({
          id: `${node.parent_id}-${node.id}`,
          source: node.parent_id.toString(),
          target: node.id.toString(),
          type: 'custom',
          style: {
            stroke: '#6B7280',
            strokeWidth: 2,
          },
        });
      }
    });
    
    return edges;
  }, [nodes]);

  // Update ReactFlow nodes when props change
  useMemo(() => {
    setNodes(flowNodes);
  }, [flowNodes, setNodes]);

  // Update ReactFlow edges when props change
  useMemo(() => {
    setEdges(flowEdges);
  }, [flowEdges, setEdges]);

  const onConnect = useCallback(
    (params: Connection) => {
      setEdges((eds) => addEdge(params, eds));
    },
    [setEdges]
  );

  return (
    <div className="w-full h-full">
      <ReactFlow
        nodes={reactFlowNodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        fitView
        attributionPosition="bottom-left"
      >
        <Controls />
        <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
      </ReactFlow>
    </div>
  );
}
