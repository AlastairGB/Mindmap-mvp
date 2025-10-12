'use client';

import { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { Badge } from '@/components/ui/badge';
import { Node as MindMapNode } from '@/lib/api';

interface CustomNodeData extends MindMapNode {
  onClick?: () => void;
  onUpdate?: (updates: Partial<MindMapNode>) => void;
}

export const CustomNode = memo(({ data }: NodeProps<CustomNodeData>) => {
  const getNodeTypeColor = (type: string) => {
    switch (type) {
      case 'root':
        return 'bg-blue-600';
      case 'branch':
        return 'bg-green-600';
      case 'leaf':
        return 'bg-purple-600';
      default:
        return 'bg-gray-600';
    }
  };

  const getNodeTypeIcon = (type: string) => {
    switch (type) {
      case 'root':
        return '🏠';
      case 'branch':
        return '🌿';
      case 'leaf':
        return '🍃';
      default:
        return '📄';
    }
  };

  return (
    <div
      className={`px-4 py-2 rounded-lg shadow-lg border-2 border-white min-w-[120px] max-w-[200px] cursor-pointer hover:shadow-xl transition-shadow ${getNodeTypeColor(data.node_type)}`}
      onClick={data.onClick}
      style={{ backgroundColor: data.color || undefined }}
    >
      <Handle
        type="target"
        position={Position.Top}
        className="w-3 h-3 bg-white border-2 border-gray-400"
      />
      
      <div className="text-center">
        <div className="flex items-center justify-center mb-1">
          <span className="text-lg mr-1">{getNodeTypeIcon(data.node_type)}</span>
          <Badge 
            variant="secondary" 
            className="text-xs bg-white/20 text-white border-white/30"
          >
            {data.node_type}
          </Badge>
        </div>
        
        <div className="text-white font-semibold text-sm leading-tight">
          {data.title}
        </div>
        
        {data.content && (
          <div className="text-white/80 text-xs mt-1 line-clamp-2">
            {data.content}
          </div>
        )}
        
        {data.tags && data.tags.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-2">
            {data.tags.slice(0, 2).map((tag, index) => (
              <span
                key={index}
                className="text-xs bg-white/20 text-white px-1 py-0.5 rounded"
              >
                {tag}
              </span>
            ))}
            {data.tags.length > 2 && (
              <span className="text-xs text-white/60">
                +{data.tags.length - 2}
              </span>
            )}
          </div>
        )}
        
        <div className="flex items-center justify-between mt-2 text-xs text-white/60">
          <span>{data.children_count} children</span>
          <span>{data.connections_count} links</span>
        </div>
      </div>
      
      <Handle
        type="source"
        position={Position.Bottom}
        className="w-3 h-3 bg-white border-2 border-gray-400"
      />
    </div>
  );
});

CustomNode.displayName = 'CustomNode';
