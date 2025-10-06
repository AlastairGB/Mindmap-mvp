# Mind Map AI Backend API

A complete FastAPI backend service for AI-powered mind map creation and management. This backend provides RESTful APIs for node management, AI-powered mind map generation, and database persistence.

## 🚀 Features

- **Complete CRUD Operations**: Create, read, update, and delete mind map nodes
- **AI-Powered Generation**: Generate mind maps from raw text using Hugging Face APIs
- **Node Relationships**: Link and manage connections between nodes
- **Database Persistence**: SQLite database with SQLModel for data management
- **CORS Support**: Ready for frontend integration (React, Next.js, etc.)
- **RESTful API**: Clean JSON responses with proper HTTP status codes
- **Comprehensive Testing**: Full test suite for all endpoints

## 📁 Project Structure

```
mindmap-ai-backend/
├── main.py                 # FastAPI application entry point
├── start_server.py         # Server startup script
├── config.py              # Configuration management
├── env.example            # Environment variables template
├── requirements.txt       # Python dependencies
├── test_api.py           # API test client
├── models/
│   ├── __init__.py
│   ├── database.py       # Database models and connection
│   └── node.py          # Pydantic models for API
├── services/
│   ├── __init__.py
│   ├── mindmap.py       # Mind map business logic
│   └── ai_pipeline.py   # AI pipeline integration
└── mindmap_pipeline.py  # Original AI pipeline (standalone)
```

## 🛠️ Installation

1. **Clone and navigate to the project:**
   ```bash
   cd "Mind map Ai mvp"
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Set up environment variables (optional):**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Start the server:**
   ```bash
   python3 start_server.py
   ```

The API will be available at:
- **API Base**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📚 API Endpoints

### Health & Status
- `GET /health` - Health check
- `GET /ai/status` - AI pipeline status

### Node Management
- `POST /nodes` - Create a new node
- `GET /nodes/{id}` - Get a specific node
- `GET /nodes` - List all nodes (with pagination)
- `PUT /nodes/{id}` - Update a node
- `DELETE /nodes/{id}` - Delete a node

### Node Relationships
- `POST /nodes/{id}/link/{target_id}` - Link two nodes
- `DELETE /nodes/{id}/unlink/{target_id}` - Unlink nodes
- `GET /nodes/{id}/connections` - Get node connections

### AI Features
- `POST /ai/generate-mindmap` - Generate mind map from text
- `GET /export/mindmap` - Export entire mind map

## 🔧 Usage Examples

### 1. Create a Node
```bash
curl -X POST "http://localhost:8000/nodes" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Idea",
    "content": "This is a great idea",
    "node_type": "leaf",
    "color": "#FF6B6B"
  }'
```

### 2. Generate AI Mind Map
```bash
curl -X POST "http://localhost:8000/ai/generate-mindmap" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I need to plan my marketing strategy. Focus on social media, email campaigns, and SEO optimization."
  }'
```

### 3. List All Nodes
```bash
curl -X GET "http://localhost:8000/nodes"
```

### 4. Link Nodes
```bash
curl -X POST "http://localhost:8000/nodes/1/link/2"
```

## 🧪 Testing

### Run Quick Test
```bash
python3 test_api.py quick
```

### Run Comprehensive Test
```bash
python3 test_api.py
```

### Test Results
The test suite validates:
- ✅ Health check and server status
- ✅ Node CRUD operations
- ✅ Node linking and relationships
- ✅ AI mind map generation
- ✅ Data export functionality

## 🗄️ Database

The backend uses SQLite by default with the following tables:

### Node Table
- `id` (Primary Key)
- `title` (Node title)
- `content` (Node description)
- `node_type` (root/branch/leaf)
- `parent_id` (Parent node reference)
- `position_x`, `position_y` (Visual positioning)
- `color` (Node color)
- `tags` (JSON array of tags)
- `node_metadata` (JSON metadata)
- `created_at`, `updated_at` (Timestamps)

### NodeConnection Table
- `id` (Primary Key)
- `source_node_id` (Source node)
- `target_node_id` (Target node)
- `connection_type` (Relationship type)
- `weight` (Connection strength)
- `created_at` (Timestamp)

## 🤖 AI Integration

The backend integrates with Hugging Face APIs for:
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
- **Classification**: `facebook/bart-large-mnli`
- **Summarization**: `facebook/bart-large-cnn`
- **NER**: `dslim/bert-base-NER`

### AI Pipeline Process
1. **Text Preprocessing**: Split text into sentences/phrases
2. **Embeddings**: Generate semantic embeddings
3. **Clustering**: Group similar concepts using KMeans
4. **Classification**: Label clusters with zero-shot classification
5. **Summarization**: Shorten long labels
6. **NER**: Extract named entities
7. **JSON Generation**: Create hierarchical mind map structure

## 🔒 Security & Configuration

### Environment Variables
- `DATABASE_URL`: Database connection string
- `HF_TOKEN`: Hugging Face API token (optional)
- `DEBUG`: Enable debug mode
- `CORS_ORIGINS`: Allowed CORS origins
- `SECRET_KEY`: Application secret key

### CORS Configuration
The API is configured to accept requests from:
- `http://localhost:3000` (React dev server)
- `http://localhost:3001` (Alternative frontend)
- Configurable via environment variables

## 🚀 Frontend Integration

This backend is ready for frontend integration with:

### React/Next.js
```javascript
// Example API call
const response = await fetch('http://localhost:8000/nodes', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    title: 'New Node',
    content: 'Node description',
    node_type: 'leaf'
  })
});
```

### Vue.js
```javascript
// Using axios
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000'
});

// Create node
const createNode = async (nodeData) => {
  const response = await api.post('/nodes', nodeData);
  return response.data;
};
```

## 📊 Performance

- **Database**: SQLite for development, easily upgradeable to PostgreSQL/MySQL
- **Caching**: Ready for Redis integration
- **Rate Limiting**: Configurable AI API rate limits
- **Pagination**: Built-in pagination for large datasets

## 🔄 Deployment

### Development
```bash
python3 start_server.py
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker (Optional)
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "start_server.py"]
```

## 📈 Monitoring

- **Health Check**: `/health` endpoint
- **API Documentation**: Auto-generated with FastAPI
- **Database**: SQLite file for easy inspection
- **Logging**: Structured logging with uvicorn

## 🎯 Next Steps

1. **Frontend Development**: Connect React/Next.js frontend
2. **Authentication**: Add user authentication and authorization
3. **Real-time Updates**: Implement WebSocket support
4. **File Uploads**: Add support for document uploads
5. **Advanced AI**: Integrate more sophisticated AI models
6. **Collaboration**: Add multi-user support

## 📝 API Documentation

Full interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

The API follows RESTful conventions with proper HTTP status codes and JSON responses.
