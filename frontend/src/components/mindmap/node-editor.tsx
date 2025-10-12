'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { nodeApi, Node } from '@/lib/api';
import { 
  Save, 
  Trash2, 
  X, 
  Edit3,
  Tag,
  Palette,
  Link as LinkIcon,
  Calendar,
  User
} from 'lucide-react';

interface NodeEditorProps {
  node: Node;
  onUpdate: (updates: Partial<Node>) => void;
  onClose: () => void;
}

export function NodeEditor({ node, onUpdate, onClose }: NodeEditorProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    title: node.title,
    content: node.content || '',
    node_type: node.node_type,
    color: node.color || '#3B82F6',
    tags: node.tags || [],
  });
  const [newTag, setNewTag] = useState('');

  const queryClient = useQueryClient();

  const updateMutation = useMutation({
    mutationFn: ({ nodeId, updates }: { nodeId: number; updates: Partial<Node> }) =>
      nodeApi.updateNode(nodeId, updates),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['nodes'] });
      setIsEditing(false);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (nodeId: number) => nodeApi.deleteNode(nodeId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['nodes'] });
      onClose();
    },
  });

  const handleSave = () => {
    updateMutation.mutate({
      nodeId: node.id,
      updates: formData,
    });
  };

  const handleDelete = () => {
    if (confirm('Are you sure you want to delete this node? This action cannot be undone.')) {
      deleteMutation.mutate(node.id);
    }
  };

  const addTag = () => {
    if (newTag.trim() && !formData.tags.includes(newTag.trim())) {
      setFormData(prev => ({
        ...prev,
        tags: [...prev.tags, newTag.trim()]
      }));
      setNewTag('');
    }
  };

  const removeTag = (tagToRemove: string) => {
    setFormData(prev => ({
      ...prev,
      tags: prev.tags.filter(tag => tag !== tagToRemove)
    }));
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      addTag();
    }
  };

  return (
    <Card className="h-fit">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">Node Details</CardTitle>
          <div className="flex items-center space-x-2">
            {isEditing ? (
              <>
                <Button
                  size="sm"
                  onClick={handleSave}
                  disabled={updateMutation.isPending}
                >
                  <Save className="h-4 w-4 mr-1" />
                  Save
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => setIsEditing(false)}
                >
                  <X className="h-4 w-4" />
                </Button>
              </>
            ) : (
              <>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => setIsEditing(true)}
                >
                  <Edit3 className="h-4 w-4" />
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={onClose}
                >
                  <X className="h-4 w-4" />
                </Button>
              </>
            )}
          </div>
        </div>
        <CardDescription>
          {isEditing ? 'Edit node properties' : 'View and manage node details'}
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Node Type Badge */}
        <div className="flex items-center space-x-2">
          <Badge 
            variant="outline"
            style={{ backgroundColor: node.color + '20', borderColor: node.color }}
          >
            {node.node_type}
          </Badge>
          <span className="text-sm text-gray-500">ID: {node.id}</span>
        </div>

        {/* Title */}
        <div>
          <label className="text-sm font-medium text-gray-700 mb-1 block">
            Title
          </label>
          {isEditing ? (
            <Input
              value={formData.title}
              onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
              placeholder="Node title"
            />
          ) : (
            <p className="text-sm text-gray-900">{node.title}</p>
          )}
        </div>

        {/* Content */}
        <div>
          <label className="text-sm font-medium text-gray-700 mb-1 block">
            Content
          </label>
          {isEditing ? (
            <Textarea
              value={formData.content}
              onChange={(e) => setFormData(prev => ({ ...prev, content: e.target.value }))}
              placeholder="Node description"
              rows={3}
            />
          ) : (
            <p className="text-sm text-gray-900">
              {node.content || 'No content'}
            </p>
          )}
        </div>

        {/* Node Type */}
        {isEditing && (
          <div>
            <label className="text-sm font-medium text-gray-700 mb-1 block">
              Node Type
            </label>
            <Select
              value={formData.node_type}
              onValueChange={(value: 'root' | 'branch' | 'leaf') =>
                setFormData(prev => ({ ...prev, node_type: value }))
              }
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="root">Root</SelectItem>
                <SelectItem value="branch">Branch</SelectItem>
                <SelectItem value="leaf">Leaf</SelectItem>
              </SelectContent>
            </Select>
          </div>
        )}

        {/* Color */}
        {isEditing && (
          <div>
            <label className="text-sm font-medium text-gray-700 mb-1 block">
              Color
            </label>
            <div className="flex items-center space-x-2">
              <input
                type="color"
                value={formData.color}
                onChange={(e) => setFormData(prev => ({ ...prev, color: e.target.value }))}
                className="w-8 h-8 rounded border border-gray-300"
              />
              <Input
                value={formData.color}
                onChange={(e) => setFormData(prev => ({ ...prev, color: e.target.value }))}
                placeholder="#3B82F6"
                className="flex-1"
              />
            </div>
          </div>
        )}

        {/* Tags */}
        <div>
          <label className="text-sm font-medium text-gray-700 mb-1 block">
            Tags
          </label>
          {isEditing ? (
            <div className="space-y-2">
              <div className="flex space-x-2">
                <Input
                  value={newTag}
                  onChange={(e) => setNewTag(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Add tag"
                />
                <Button size="sm" onClick={addTag}>
                  <Tag className="h-4 w-4" />
                </Button>
              </div>
              <div className="flex flex-wrap gap-1">
                {formData.tags.map((tag, index) => (
                  <Badge
                    key={index}
                    variant="secondary"
                    className="text-xs cursor-pointer hover:bg-red-100"
                    onClick={() => removeTag(tag)}
                  >
                    {tag} ×
                  </Badge>
                ))}
              </div>
            </div>
          ) : (
            <div className="flex flex-wrap gap-1">
              {node.tags && node.tags.length > 0 ? (
                node.tags.map((tag, index) => (
                  <Badge key={index} variant="secondary" className="text-xs">
                    {tag}
                  </Badge>
                ))
              ) : (
                <span className="text-sm text-gray-500">No tags</span>
              )}
            </div>
          )}
        </div>

        {/* Metadata */}
        <div className="pt-4 border-t">
          <div className="space-y-2 text-sm text-gray-600">
            <div className="flex items-center space-x-2">
              <Calendar className="h-4 w-4" />
              <span>Created: {new Date(node.created_at).toLocaleDateString()}</span>
            </div>
            <div className="flex items-center space-x-2">
              <Calendar className="h-4 w-4" />
              <span>Updated: {new Date(node.updated_at).toLocaleDateString()}</span>
            </div>
            <div className="flex items-center space-x-2">
              <LinkIcon className="h-4 w-4" />
              <span>{node.children_count} children, {node.connections_count} connections</span>
            </div>
          </div>
        </div>

        {/* Actions */}
        {!isEditing && (
          <div className="pt-4 border-t">
            <Button
              variant="destructive"
              size="sm"
              onClick={handleDelete}
              disabled={deleteMutation.isPending}
              className="w-full"
            >
              <Trash2 className="h-4 w-4 mr-2" />
              Delete Node
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
