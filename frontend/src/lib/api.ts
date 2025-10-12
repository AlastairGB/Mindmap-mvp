import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types for API responses
export interface Node {
  id: number;
  title: string;
  content?: string;
  node_type: 'root' | 'branch' | 'leaf';
  parent_id?: number;
  position_x?: number;
  position_y?: number;
  color?: string;
  tags?: string[];
  metadata?: Record<string, unknown>;
  created_at: string;
  updated_at: string;
  children_count: number;
  connections_count: number;
}

export interface NodeCreate {
  title: string;
  content?: string;
  node_type: 'root' | 'branch' | 'leaf';
  parent_id?: number;
  position_x?: number;
  position_y?: number;
  color?: string;
  tags?: string[];
  metadata?: Record<string, unknown>;
}

export interface NodeUpdate {
  title?: string;
  content?: string;
  node_type?: 'root' | 'branch' | 'leaf';
  parent_id?: number;
  position_x?: number;
  position_y?: number;
  color?: string;
  tags?: string[];
  metadata?: Record<string, unknown>;
}

export interface NodeConnection {
  id: number;
  target_node?: {
    id: number;
    title: string;
    node_type: string;
  };
  source_node?: {
    id: number;
    title: string;
    node_type: string;
  };
  direction: 'incoming' | 'outgoing';
  connection_type: string;
  weight?: number;
}

export interface MindMapExport {
  root: string;
  children: Array<{
    id: number;
    title: string;
    content?: string;
    node_type: string;
    position?: { x: number; y: number };
    color?: string;
    children: unknown[];
  }>;
  total_nodes: number;
  exported_at: string;
}

export interface AIGenerationResponse {
  message: string;
  nodes_created: number;
  mindmap_data: {
    root: string;
    children: Array<{
      node: string;
      children: string[];
    }>;
    generated_at: string;
    source_text_length: number;
    ai_processed: boolean;
  };
}

// API functions
export const nodeApi = {
  // Get all nodes
  getNodes: async (skip = 0, limit = 100): Promise<Node[]> => {
    const response = await api.get(`/nodes?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  // Get single node
  getNode: async (id: number): Promise<Node> => {
    const response = await api.get(`/nodes/${id}`);
    return response.data;
  },

  // Create node
  createNode: async (node: NodeCreate): Promise<Node> => {
    const response = await api.post('/nodes', node);
    return response.data;
  },

  // Update node
  updateNode: async (id: number, node: NodeUpdate): Promise<Node> => {
    const response = await api.put(`/nodes/${id}`, node);
    return response.data;
  },

  // Delete node
  deleteNode: async (id: number): Promise<void> => {
    await api.delete(`/nodes/${id}`);
  },

  // Link nodes
  linkNodes: async (sourceId: number, targetId: number): Promise<void> => {
    await api.post(`/nodes/${sourceId}/link/${targetId}`);
  },

  // Unlink nodes
  unlinkNodes: async (sourceId: number, targetId: number): Promise<void> => {
    await api.delete(`/nodes/${sourceId}/unlink/${targetId}`);
  },

  // Get node connections
  getNodeConnections: async (id: number): Promise<{ connections: NodeConnection[] }> => {
    const response = await api.get(`/nodes/${id}/connections`);
    return response.data;
  },
};

export const aiApi = {
  // Generate mind map from text
  generateMindMap: async (text: string): Promise<AIGenerationResponse> => {
    const response = await api.post('/ai/generate-mindmap', { text });
    return response.data;
  },

  // Get AI status
  getStatus: async (): Promise<{ status: string; models: Record<string, string> }> => {
    const response = await api.get('/ai/status');
    return response.data;
  },
};

export const exportApi = {
  // Export mind map
  exportMindMap: async (): Promise<MindMapExport> => {
    const response = await api.get('/export/mindmap');
    return response.data;
  },
};

export const healthApi = {
  // Health check
  checkHealth: async (): Promise<{ status: string; message: string }> => {
    const response = await api.get('/health');
    return response.data;
  },
};
