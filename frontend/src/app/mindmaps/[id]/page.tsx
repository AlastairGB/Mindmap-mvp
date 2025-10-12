'use client';

import { useState } from 'react';
import { useParams } from 'next/navigation';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useQuery } from '@tanstack/react-query';
import { nodeApi, Node } from '@/lib/api';
import { MindMapFlow } from '@/components/mindmap/mindmap-flow';
import { NodeEditor } from '@/components/mindmap/node-editor';
import { 
  ArrowLeft, 
  Edit, 
  Download,
  Share,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  Maximize2
} from 'lucide-react';
import Link from 'next/link';

export default function MindMapDetailPage() {
  const params = useParams();
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [isFullscreen, setIsFullscreen] = useState(false);

  const nodeId = parseInt(params.id as string);

  const { data: nodes = [], isLoading } = useQuery({
    queryKey: ['nodes'],
    queryFn: () => nodeApi.getNodes(),
  });

  const { data: rootNode, isLoading: rootLoading } = useQuery({
    queryKey: ['node', nodeId],
    queryFn: () => nodeApi.getNode(nodeId),
    enabled: !!nodeId,
  });

  // Get all nodes for this mind map (root + children)
  const mindMapNodes = nodes.filter(node => 
    node.id === nodeId || node.parent_id === nodeId
  );

  const handleNodeClick = (node: Node) => {
    setSelectedNode(node);
  };

  const handleNodeUpdate = async (nodeId: number, updates: Partial<Node>) => {
    try {
      await nodeApi.updateNode(nodeId, updates);
      // The query will automatically refetch due to invalidation
    } catch (error) {
      console.error('Failed to update node:', error);
    }
  };

  if (isLoading || rootLoading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading mind map...</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  if (!rootNode) {
    return (
      <DashboardLayout>
        <div className="text-center py-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Mind Map Not Found</h2>
          <p className="text-gray-600 mb-6">The mind map you&apos;re looking for doesn&apos;t exist.</p>
          <Link href="/mindmaps">
            <Button>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Mind Maps
            </Button>
          </Link>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className={`space-y-6 ${isFullscreen ? 'fixed inset-0 z-50 bg-white p-6' : ''}`}>
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Link href="/mindmaps">
              <Button variant="ghost" size="sm">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back
              </Button>
            </Link>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{rootNode.title}</h1>
              <p className="text-gray-600">
                {mindMapNodes.length} nodes • Created {new Date(rootNode.created_at).toLocaleDateString()}
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setIsFullscreen(!isFullscreen)}
            >
              <Maximize2 className="h-4 w-4 mr-2" />
              {isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}
            </Button>
            <Button variant="outline" size="sm">
              <Share className="h-4 w-4 mr-2" />
              Share
            </Button>
            <Button variant="outline" size="sm">
              <Download className="h-4 w-4 mr-2" />
              Export
            </Button>
          </div>
        </div>

        {/* Mind Map Info */}
        <Card>
          <CardContent className="py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-6">
                <div className="flex items-center space-x-2">
                  <Badge 
                    variant="outline"
                    style={{ backgroundColor: rootNode.color + '20', borderColor: rootNode.color }}
                  >
                    {rootNode.node_type}
                  </Badge>
                  <span className="text-sm text-gray-600">
                    {mindMapNodes.filter(n => n.node_type === 'branch').length} branches
                  </span>
                  <span className="text-sm text-gray-600">
                    {mindMapNodes.filter(n => n.node_type === 'leaf').length} leaves
                  </span>
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                <Button variant="outline" size="sm">
                  <ZoomIn className="h-4 w-4" />
                </Button>
                <Button variant="outline" size="sm">
                  <ZoomOut className="h-4 w-4" />
                </Button>
                <Button variant="outline" size="sm">
                  <RotateCcw className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Mind Map Visualization */}
          <div className="lg:col-span-3">
            <Card className="h-[600px]">
              <CardContent className="p-0 h-full">
                <MindMapFlow
                  nodes={mindMapNodes}
                  onNodeClick={handleNodeClick}
                  onNodeUpdate={handleNodeUpdate}
                />
              </CardContent>
            </Card>
          </div>

          {/* Node Editor Sidebar */}
          <div className="lg:col-span-1">
            {selectedNode ? (
              <NodeEditor
                node={selectedNode}
                onUpdate={(updates) => handleNodeUpdate(selectedNode.id, updates)}
                onClose={() => setSelectedNode(null)}
              />
            ) : (
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Node Details</CardTitle>
                  <CardDescription>
                    Click on a node to view and edit its details
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-8 text-gray-500">
                    <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
                      <Edit className="h-8 w-8" />
                    </div>
                    <p>Select a node to edit</p>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>

        {/* Node List */}
        <Card>
          <CardHeader>
            <CardTitle>All Nodes</CardTitle>
            <CardDescription>
              Complete list of nodes in this mind map
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {mindMapNodes.map((node) => (
                <div
                  key={node.id}
                  className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                    selectedNode?.id === node.id 
                      ? 'border-blue-500 bg-blue-50' 
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => setSelectedNode(node)}
                >
                  <div className="flex items-start justify-between mb-2">
                    <h4 className="font-medium text-sm">{node.title}</h4>
                    <Badge 
                      variant="outline" 
                      className="text-xs"
                      style={{ backgroundColor: node.color + '20', borderColor: node.color }}
                    >
                      {node.node_type}
                    </Badge>
                  </div>
                  {node.content && (
                    <p className="text-xs text-gray-600 line-clamp-2 mb-2">
                      {node.content}
                    </p>
                  )}
                  <div className="flex items-center justify-between text-xs text-gray-500">
                    <span>{node.children_count} children</span>
                    <span>{node.connections_count} links</span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
