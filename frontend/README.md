# Mind Map AI Frontend

A modern Next.js 14 frontend application for the Mind Map AI platform. Built with TypeScript, Tailwind CSS, shadcn/ui, and React Query for seamless integration with the FastAPI backend.

## 🚀 Features

- **Modern UI**: Built with Next.js 14, Tailwind CSS, and shadcn/ui components
- **Interactive Mind Maps**: ReactFlow-powered visualization with zoom, pan, and node interactions
- **AI Integration**: Seamless connection to Hugging Face APIs for mind map generation
- **Real-time Updates**: React Query for efficient data fetching and caching
- **Responsive Design**: Mobile-first design that works on all devices
- **Node Management**: Full CRUD operations for mind map nodes
- **Settings & Configuration**: Customizable themes and AI model settings

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui + Radix UI
- **State Management**: TanStack Query (React Query)
- **HTTP Client**: Axios
- **Visualization**: ReactFlow
- **Icons**: Lucide React

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── page.tsx           # Dashboard
│   │   ├── create/            # Mind map creator
│   │   ├── mindmaps/          # Mind map viewer
│   │   └── settings/          # Settings page
│   ├── components/            # Reusable components
│   │   ├── layout/           # Layout components
│   │   ├── mindmap/          # Mind map specific components
│   │   └── ui/               # shadcn/ui components
│   └── lib/                  # Utilities and API client
├── public/                   # Static assets
└── package.json
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Running FastAPI backend (http://localhost:8000)

### Installation

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

4. **Open in browser:**
   ```
   http://localhost:3000
   ```

## 📱 Pages & Features

### Dashboard (`/`)
- Overview of all mind maps
- Quick stats and recent activity
- AI status monitoring
- Quick action buttons

### Create Mindmap (`/create`)
- Text input for AI processing
- Sample texts for testing
- Real-time AI processing steps
- Progress indicators

### View Mindmaps (`/mindmaps`)
- Grid/list view of all mind maps
- Search and filter functionality
- Mind map cards with metadata
- Quick access to individual maps

### Mind Map Detail (`/mindmaps/[id]`)
- Interactive ReactFlow visualization
- Node editor sidebar
- Zoom, pan, and navigation controls
- Fullscreen mode
- Export functionality

### Settings (`/settings`)
- AI configuration (Hugging Face token)
- Theme selection (light/dark/system)
- Notification preferences
- System information
- Data management tools

## 🎨 UI Components

### Layout Components
- `DashboardLayout`: Main layout with sidebar and header
- `Sidebar`: Navigation sidebar with menu items
- `Header`: Top header with search and user actions

### Mind Map Components
- `MindMapFlow`: ReactFlow wrapper for visualization
- `CustomNode`: Custom node component with styling
- `CustomEdge`: Custom edge component
- `NodeEditor`: Sidebar panel for node editing

### UI Components
- All shadcn/ui components (Button, Card, Input, etc.)
- Custom components built on top of Radix UI primitives

## 🔌 API Integration

### API Client (`src/lib/api.ts`)
- Axios-based HTTP client
- TypeScript interfaces for all API responses
- Organized API functions by feature

### React Query Integration
- Automatic caching and background updates
- Optimistic updates for better UX
- Error handling and retry logic
- DevTools for debugging

### API Endpoints Used
- `GET /health` - Health check
- `GET /nodes` - List all nodes
- `POST /nodes` - Create node
- `PUT /nodes/{id}` - Update node
- `DELETE /nodes/{id}` - Delete node
- `POST /ai/generate-mindmap` - Generate mind map
- `GET /export/mindmap` - Export data

## 🎯 Key Features

### Interactive Mind Maps
- **ReactFlow Integration**: Professional mind map visualization
- **Node Interactions**: Click to edit, drag to reposition
- **Custom Styling**: Color-coded nodes by type
- **Responsive Design**: Works on desktop and mobile

### AI-Powered Generation
- **Text Processing**: Paste any text to generate mind maps
- **Real-time Feedback**: Progress indicators during AI processing
- **Sample Texts**: Built-in examples for testing
- **Error Handling**: Graceful fallbacks when AI services are unavailable

### Node Management
- **Full CRUD**: Create, read, update, delete nodes
- **Rich Metadata**: Tags, colors, positions, content
- **Relationships**: Parent-child connections
- **Bulk Operations**: Export and import functionality

### Modern UX
- **Loading States**: Skeleton loaders and spinners
- **Error Boundaries**: Graceful error handling
- **Optimistic Updates**: Immediate UI feedback
- **Keyboard Shortcuts**: Power user features

## 🔧 Configuration

### Environment Variables
Create a `.env.local` file:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Tailwind Configuration
- Custom color palette
- Responsive breakpoints
- Component-specific styles

### TypeScript Configuration
- Strict type checking
- Path aliases (@/*)
- Next.js optimizations

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

### Start Production Server
```bash
npm start
```

### Docker Deployment
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

## 🧪 Testing

### Manual Testing
1. Start the FastAPI backend: `python3 start_server.py`
2. Start the frontend: `npm run dev`
3. Test all features:
   - Create mind maps
   - View and edit nodes
   - Navigate between pages
   - Test responsive design

### Integration Testing
- API connectivity
- Data persistence
- Error handling
- Performance optimization

## 🎨 Customization

### Themes
- Light/dark mode support
- Custom color schemes
- Component theming

### Styling
- Tailwind CSS classes
- Custom CSS variables
- Component variants

### Functionality
- Add new pages
- Extend API integration
- Custom node types
- Additional AI models

## 📊 Performance

### Optimization Features
- Next.js automatic optimizations
- React Query caching
- Image optimization
- Code splitting
- Lazy loading

### Monitoring
- React Query DevTools
- Next.js analytics
- Performance metrics
- Error tracking

## 🔮 Future Enhancements

- **Real-time Collaboration**: WebSocket integration
- **Advanced AI**: More sophisticated models
- **Mobile App**: React Native version
- **Offline Support**: PWA capabilities
- **Advanced Export**: PDF, SVG, PNG formats
- **User Authentication**: Multi-user support
- **Templates**: Pre-built mind map templates
- **Analytics**: Usage tracking and insights

## 📝 Development Notes

### Code Style
- TypeScript strict mode
- ESLint configuration
- Prettier formatting
- Component composition

### Best Practices
- Server components where possible
- Client components for interactivity
- Proper error boundaries
- Accessibility compliance

### Performance Tips
- Use React.memo for expensive components
- Implement proper loading states
- Optimize bundle size
- Monitor Core Web Vitals

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the Mind Map AI platform.