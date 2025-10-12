'use client';

import { useState } from 'react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { useQuery } from '@tanstack/react-query';
import { nodeApi, Node as MindMapNode } from '@/lib/api';
import { 
  Eye, 
  Plus, 
  Search,
  Calendar,
  Brain,
  ArrowRight,
  Grid,
  List
} from 'lucide-react';
import Link from 'next/link';

export default function MindmapsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  const { data: nodes = [], isLoading } = useQuery({
    queryKey: ['nodes'],
    queryFn: () => nodeApi.getNodes(),
  });

  // Group nodes by root nodes (mind maps)
  const mindMaps = nodes.reduce((acc, node) => {
    if (node.node_type === 'root') {
      acc[node.id] = {
        root: node,
        children: nodes.filter(n => n.parent_id === node.id),
        totalNodes: 1 + nodes.filter(n => n.parent_id === node.id).length,
      };
    }
    return acc;
  }, {} as Record<number, { root: MindMapNode; children: MindMapNode[]; totalNodes: number }>);

  const filteredMindMaps = Object.values(mindMaps).filter(mindMap =>
    mindMap.root.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    mindMap.root.content?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (isLoading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading mind maps...</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Mind Maps</h1>
            <p className="text-gray-600">Browse and manage your AI-generated mind maps</p>
          </div>
          <Link href="/create">
            <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
              <Plus className="h-4 w-4 mr-2" />
              Create New
            </Button>
          </Link>
        </div>

        {/* Search and Filters */}
        <div className="flex items-center space-x-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <Input
              placeholder="Search mind maps..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
          <div className="flex items-center space-x-2">
            <Button
              variant={viewMode === 'grid' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setViewMode('grid')}
            >
              <Grid className="h-4 w-4" />
            </Button>
            <Button
              variant={viewMode === 'list' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setViewMode('list')}
            >
              <List className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Mind Maps Grid/List */}
        {filteredMindMaps.length === 0 ? (
          <Card>
            <CardContent className="text-center py-12">
              <Brain className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {searchTerm ? 'No mind maps found' : 'No mind maps yet'}
              </h3>
              <p className="text-gray-600 mb-6">
                {searchTerm 
                  ? 'Try adjusting your search terms'
                  : 'Create your first AI-powered mind map to get started'
                }
              </p>
              {!searchTerm && (
                <Link href="/create">
                  <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                    <Plus className="h-4 w-4 mr-2" />
                    Create Your First Mind Map
                  </Button>
                </Link>
              )}
            </CardContent>
          </Card>
        ) : (
          <div className={
            viewMode === 'grid' 
              ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'
              : 'space-y-4'
          }>
            {filteredMindMaps.map((mindMap) => (
              <Card 
                key={mindMap.root.id} 
                className="hover:shadow-lg transition-shadow cursor-pointer group"
              >
                <Link href={`/mindmaps/${mindMap.root.id}`}>
                  <CardHeader className="pb-3">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <CardTitle className="text-lg group-hover:text-blue-600 transition-colors">
                          {mindMap.root.title}
                        </CardTitle>
                        <CardDescription className="mt-1">
                          {mindMap.root.content || 'AI-generated mind map'}
                        </CardDescription>
                      </div>
                      <Badge 
                        variant="outline" 
                        className="ml-2"
                        style={{ backgroundColor: mindMap.root.color + '20', borderColor: mindMap.root.color }}
                      >
                        {mindMap.root.node_type}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {/* Stats */}
                      <div className="flex items-center justify-between text-sm text-gray-600">
                        <div className="flex items-center space-x-4">
                          <span className="flex items-center">
                            <Brain className="h-4 w-4 mr-1" />
                            {mindMap.totalNodes} nodes
                          </span>
                          <span className="flex items-center">
                            <Calendar className="h-4 w-4 mr-1" />
                            {new Date(mindMap.root.created_at).toLocaleDateString()}
                          </span>
                        </div>
                      </div>

                      {/* Tags */}
                      {mindMap.root.tags && mindMap.root.tags.length > 0 && (
                        <div className="flex flex-wrap gap-1">
                          {mindMap.root.tags.slice(0, 3).map((tag: string, index: number) => (
                            <Badge key={index} variant="secondary" className="text-xs">
                              {tag}
                            </Badge>
                          ))}
                          {mindMap.root.tags.length > 3 && (
                            <Badge variant="secondary" className="text-xs">
                              +{mindMap.root.tags.length - 3}
                            </Badge>
                          )}
                        </div>
                      )}

                      {/* Action Button */}
                      <div className="flex items-center justify-between pt-2">
                        <div className="text-xs text-gray-500">
                          Last updated: {new Date(mindMap.root.updated_at).toLocaleDateString()}
                        </div>
                        <Button 
                          variant="ghost" 
                          size="sm" 
                          className="group-hover:bg-blue-50 group-hover:text-blue-600"
                        >
                          <Eye className="h-4 w-4 mr-1" />
                          View
                          <ArrowRight className="h-3 w-3 ml-1 group-hover:translate-x-1 transition-transform" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Link>
              </Card>
            ))}
          </div>
        )}

        {/* Stats Summary */}
        {filteredMindMaps.length > 0 && (
          <Card>
            <CardContent className="py-4">
              <div className="flex items-center justify-between text-sm text-gray-600">
                <span>
                  Showing {filteredMindMaps.length} of {Object.keys(mindMaps).length} mind maps
                </span>
                <span>
                  Total nodes: {nodes.length}
                </span>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </DashboardLayout>
  );
}
