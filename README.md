# Mind Map AI - Complete Full-Stack Application

A complete AI-powered mind mapping application with a FastAPI backend and Next.js frontend. Transform raw text into structured, interactive mind maps using Hugging Face AI models.

## 🎯 Overview

This project provides a complete full-stack solution for AI-powered mind map creation and management:

- **Backend**: FastAPI with SQLModel, Hugging Face AI integration
- **Frontend**: Next.js 14 with ReactFlow visualization
- **AI Pipeline**: Text processing, embeddings, clustering, and classification
- **Database**: SQLite with persistent storage
- **Real-time**: React Query for efficient data management

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

### 1. Clone and Setup

```bash
git clone <repository-url>
cd "Mind map Ai mvp"
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Start the backend server
python3 start_server.py
```

The backend will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at:
- **Application**: http://localhost:3000

### 4. Integration Test

```bash
# Run the complete integration test
python3 test_integration.py
```

## 📁 Project Structure

```
Mind map Ai mvp/
├── backend/                    # FastAPI backend
│   ├── main.py                # FastAPI application
│   ├── models/                # Database models
│   ├── services/              # Business logic
│   ├── config.py              # Configuration
│   └── requirements.txt       # Python dependencies
├── frontend/                   # Next.js frontend
│   ├── src/
│   │   ├── app/              # App Router pages
│   │   ├── components/       # React components
│   │   └── lib/              # Utilities and API client
│   ├── package.json          # Node dependencies
│   └── README.md             # Frontend documentation
├── test_integration.py        # Integration tests
└── README.md                  # This file
```

## 🎨 Features

### Backend Features
- ✅ **Complete CRUD API** for mind map nodes
- ✅ **AI Integration** with Hugging Face models
- ✅ **Database Persistence** with SQLModel
- ✅ **CORS Support** for frontend integration
- ✅ **Error Handling** and validation
- ✅ **API Documentation** with Swagger UI

### Frontend Features
- ✅ **Modern UI** with Tailwind CSS and shadcn/ui
- ✅ **Interactive Mind Maps** with ReactFlow
- ✅ **Real-time Updates** with React Query
- ✅ **Responsive Design** for all devices
- ✅ **Node Management** with full CRUD operations
- ✅ **AI Generation** from text input
- ✅ **Settings & Configuration**

### AI Pipeline Features
- ✅ **Text Preprocessing** and sentence splitting
- ✅ **Semantic Embeddings** with sentence-transformers
- ✅ **Concept Clustering** with scikit-learn
- ✅ **Zero-shot Classification** with BART
- ✅ **Text Summarization** for node labels
- ✅ **Named Entity Recognition** for enrichment

## 🔧 API Endpoints

### Node Management
- `GET /nodes` - List all nodes
- `POST /nodes` - Create a new node
- `GET /nodes/{id}` - Get specific node
- `PUT /nodes/{id}` - Update node
- `DELETE /nodes/{id}` - Delete node

### AI Features
- `POST /ai/generate-mindmap` - Generate mind map from text
- `GET /ai/status` - Check AI service status

### Utilities
- `GET /health` - Health check
- `GET /export/mindmap` - Export mind map data

## 🎯 Usage Examples

### 1. Create a Mind Map

**Frontend**: Navigate to http://localhost:3000/create
- Paste your text
- Click "Generate Mindmap"
- View the interactive result

**API**: 
```bash
curl -X POST "http://localhost:8000/ai/generate-mindmap" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here..."}'
```

### 2. View Mind Maps

**Frontend**: Navigate to http://localhost:3000/mindmaps
- Browse all created mind maps
- Click to view interactive visualization
- Edit nodes and relationships

### 3. Manage Nodes

**API**:
```bash
# Create a node
curl -X POST "http://localhost:8000/nodes" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Node",
    "content": "Node description",
    "node_type": "leaf",
    "color": "#3B82F6"
  }'

# Update a node
curl -X PUT "http://localhost:8000/nodes/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}'
```

## 🛠️ Development

### Backend Development

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests
python3 test_api.py
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

### Database Management

The backend uses SQLite by default. Database file: `mindmap.db`

```bash
# Reset database (if needed)
rm mindmap.db
python3 start_server.py  # Will recreate tables
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=sqlite:///./mindmap.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# Hugging Face (Optional)
HF_TOKEN=your_huggingface_token_here

# CORS
CORS_ORIGINS=["http://localhost:3000"]
```

### Frontend Configuration

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🧪 Testing

### Backend Tests
```bash
# Run API tests
python3 test_api.py

# Run comprehensive tests
python3 test_api.py
```

### Frontend Tests
```bash
cd frontend
npm run build  # Tests build process
```

### Integration Tests
```bash
# Run complete integration test
python3 test_integration.py
```

## 🚀 Deployment

### Backend Deployment

**Production Server**:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Docker**:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Deployment

**Vercel** (Recommended):
```bash
cd frontend
vercel --prod
```

**Docker**:
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 📊 Performance

### Backend Performance
- **Database**: SQLite for development, PostgreSQL for production
- **Caching**: Ready for Redis integration
- **Rate Limiting**: Configurable AI API limits
- **Async**: FastAPI async/await support

### Frontend Performance
- **Next.js**: Automatic optimizations
- **React Query**: Efficient caching
- **Code Splitting**: Automatic bundle optimization
- **Image Optimization**: Next.js built-in features

## 🔮 Future Enhancements

### Planned Features
- **Real-time Collaboration**: WebSocket support
- **User Authentication**: Multi-user system
- **Advanced AI**: More sophisticated models
- **Mobile App**: React Native version
- **Offline Support**: PWA capabilities
- **Advanced Export**: PDF, SVG, PNG formats
- **Templates**: Pre-built mind map templates

### Technical Improvements
- **Database Migration**: Alembic support
- **Monitoring**: Application metrics
- **Logging**: Structured logging
- **Testing**: Comprehensive test suite
- **CI/CD**: Automated deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Guidelines
- Follow TypeScript best practices
- Use proper error handling
- Write comprehensive tests
- Update documentation
- Follow code style guidelines

## 📄 License

This project is part of the Mind Map AI platform.

## 🆘 Support

### Common Issues

**Backend not starting**:
- Check Python version (3.8+)
- Install dependencies: `pip3 install -r requirements.txt`
- Check port 8000 is available

**Frontend not starting**:
- Check Node.js version (18+)
- Install dependencies: `npm install`
- Check port 3000 is available

**AI generation failing**:
- Check internet connection
- Verify Hugging Face API access
- Check backend logs for errors

### Getting Help

1. Check the documentation
2. Run integration tests
3. Check logs for errors
4. Open an issue with details

## 🎉 Success!

You now have a complete, production-ready AI-powered mind mapping application! 

**Next Steps**:
1. Explore the frontend at http://localhost:3000
2. Try creating mind maps with different text inputs
3. Customize the AI models and settings
4. Deploy to production when ready

Happy mind mapping! 🧠✨