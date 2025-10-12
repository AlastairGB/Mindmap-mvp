'use client';

import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useQuery } from '@tanstack/react-query';
import { nodeApi, healthApi } from '@/lib/api';
import { 
  Brain, 
  Plus, 
  Eye, 
  TrendingUp,
  Clock,
  Zap,
  Activity
} from 'lucide-react';
import Link from 'next/link';

export default function Dashboard() {
  const { data: nodes = [], isLoading: nodesLoading } = useQuery({
    queryKey: ['nodes'],
    queryFn: () => nodeApi.getNodes(),
  });

  const { data: health } = useQuery({
    queryKey: ['health'],
    queryFn: () => healthApi.checkHealth(),
  });

  const stats = {
    totalNodes: nodes.length,
    rootNodes: nodes.filter(node => node.node_type === 'root').length,
    branchNodes: nodes.filter(node => node.node_type === 'branch').length,
    leafNodes: nodes.filter(node => node.node_type === 'leaf').length,
  };

  const recentNodes = nodes
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 5);

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-600">Welcome to your AI-powered mind mapping workspace</p>
          </div>
          <div className="flex items-center space-x-2">
            <Badge 
              variant={health?.status === 'healthy' ? 'default' : 'destructive'}
              className="bg-green-100 text-green-800"
            >
              <Activity className="h-3 w-3 mr-1" />
              {health?.status === 'healthy' ? 'System Online' : 'System Offline'}
            </Badge>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="hover:shadow-md transition-shadow cursor-pointer">
            <Link href="/create">
              <CardHeader className="pb-3">
                <div className="flex items-center space-x-2">
                  <Plus className="h-5 w-5 text-blue-600" />
                  <CardTitle className="text-lg">Create Mindmap</CardTitle>
                </div>
                <CardDescription>
                  Generate a new mind map from text using AI
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full">
                  <Brain className="h-4 w-4 mr-2" />
                  Start Creating
                </Button>
              </CardContent>
            </Link>
          </Card>

          <Card className="hover:shadow-md transition-shadow cursor-pointer">
            <Link href="/mindmaps">
              <CardHeader className="pb-3">
                <div className="flex items-center space-x-2">
                  <Eye className="h-5 w-5 text-green-600" />
                  <CardTitle className="text-lg">View Mindmaps</CardTitle>
                </div>
                <CardDescription>
                  Browse and manage your existing mind maps
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button variant="outline" className="w-full">
                  <Eye className="h-4 w-4 mr-2" />
                  View All
                </Button>
              </CardContent>
            </Link>
          </Card>

          <Card className="hover:shadow-md transition-shadow cursor-pointer">
            <Link href="/settings">
              <CardHeader className="pb-3">
                <div className="flex items-center space-x-2">
                  <Zap className="h-5 w-5 text-purple-600" />
                  <CardTitle className="text-lg">AI Settings</CardTitle>
                </div>
                <CardDescription>
                  Configure AI models and preferences
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button variant="outline" className="w-full">
                  <Zap className="h-4 w-4 mr-2" />
                  Configure
                </Button>
              </CardContent>
            </Link>
          </Card>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Nodes</CardTitle>
              <Brain className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.totalNodes}</div>
              <p className="text-xs text-muted-foreground">
                All mind map nodes
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Root Nodes</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.rootNodes}</div>
              <p className="text-xs text-muted-foreground">
                Main mind map topics
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Branch Nodes</CardTitle>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.branchNodes}</div>
              <p className="text-xs text-muted-foreground">
                Category nodes
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Leaf Nodes</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.leafNodes}</div>
              <p className="text-xs text-muted-foreground">
                Detail nodes
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Recent Nodes</CardTitle>
              <CardDescription>
                Your most recently created mind map nodes
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {nodesLoading ? (
                  <div className="text-center py-4">Loading...</div>
                ) : recentNodes.length === 0 ? (
                  <div className="text-center py-4 text-gray-500">
                    No nodes created yet
                  </div>
                ) : (
                  recentNodes.map((node) => (
                    <div key={node.id} className="flex items-center space-x-3">
                      <div 
                        className="w-3 h-3 rounded-full"
                        style={{ backgroundColor: node.color || '#3B82F6' }}
                      />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 truncate">
                          {node.title}
                        </p>
                        <p className="text-xs text-gray-500">
                          {new Date(node.created_at).toLocaleDateString()}
                        </p>
                      </div>
                      <Badge variant="outline" className="text-xs">
                        {node.node_type}
                      </Badge>
                    </div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>AI Status</CardTitle>
              <CardDescription>
                Current status of AI services
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Embeddings</span>
                  <Badge variant="outline" className="bg-green-100 text-green-800">
                    Online
                  </Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Classification</span>
                  <Badge variant="outline" className="bg-green-100 text-green-800">
                    Online
                  </Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Summarization</span>
                  <Badge variant="outline" className="bg-green-100 text-green-800">
                    Online
                  </Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">NER</span>
                  <Badge variant="outline" className="bg-green-100 text-green-800">
                    Online
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}