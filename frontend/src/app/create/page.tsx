'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { aiApi } from '@/lib/api';
import { 
  Brain, 
  Loader2, 
  Sparkles,
  FileText,
  Zap,
  ArrowLeft
} from 'lucide-react';
import Link from 'next/link';

export default function CreateMindmap() {
  const [text, setText] = useState('');
  const router = useRouter();
  const queryClient = useQueryClient();

  const generateMutation = useMutation({
    mutationFn: aiApi.generateMindMap,
    onSuccess: (data) => {
      // Invalidate and refetch nodes
      queryClient.invalidateQueries({ queryKey: ['nodes'] });
      
      // Show success message and redirect
      alert(`Successfully created mind map with ${data.nodes_created} nodes!`);
      router.push('/mindmaps');
    },
    onError: (error) => {
      console.error('Error generating mind map:', error);
      alert('Failed to generate mind map. Please try again.');
    },
  });

  const handleGenerate = () => {
    if (!text.trim()) {
      alert('Please enter some text to generate a mind map.');
      return;
    }
    generateMutation.mutate(text);
  };

  const sampleTexts = [
    {
      title: "Marketing Strategy",
      text: "I need to plan my marketing strategy for the new product launch. We should focus on social media marketing, especially TikTok and Instagram. The budget needs to be allocated between paid ads and influencer partnerships. I also want to consider email marketing campaigns and SEO optimization. The target audience is millennials and Gen Z consumers."
    },
    {
      title: "Project Planning",
      text: "Planning a new software project. We need to consider the technical architecture, database design, frontend development, backend APIs, testing strategies, deployment pipeline, and user experience. The team consists of 5 developers, 2 designers, and 1 project manager. Timeline is 6 months with weekly sprints."
    },
    {
      title: "Learning Goals",
      text: "My learning goals for this year include mastering React and Next.js, learning TypeScript, understanding machine learning basics, improving my design skills with Figma, and building a portfolio of projects. I also want to contribute to open source projects and attend tech conferences."
    }
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Link href="/">
              <Button variant="ghost" size="sm">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to Dashboard
              </Button>
            </Link>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Create Mindmap</h1>
              <p className="text-gray-600">Generate an AI-powered mind map from your text</p>
            </div>
          </div>
          <Badge variant="outline" className="bg-blue-100 text-blue-800">
            <Zap className="h-3 w-3 mr-1" />
            AI Powered
          </Badge>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Input Area */}
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <FileText className="h-5 w-5" />
                  <span>Input Text</span>
                </CardTitle>
                <CardDescription>
                  Paste or type your text here. The AI will analyze it and create a structured mind map.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Textarea
                  placeholder="Enter your text here... For example: 'I need to plan my marketing strategy for the new product launch. We should focus on social media marketing, especially TikTok and Instagram...'"
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  className="min-h-[300px] resize-none"
                />
                
                <div className="flex items-center justify-between">
                  <div className="text-sm text-gray-500">
                    {text.length} characters
                  </div>
                  <div className="flex space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setText('')}
                      disabled={generateMutation.isPending}
                    >
                      Clear
                    </Button>
                    <Button
                      onClick={handleGenerate}
                      disabled={generateMutation.isPending || !text.trim()}
                      className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                    >
                      {generateMutation.isPending ? (
                        <>
                          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                          Generating...
                        </>
                      ) : (
                        <>
                          <Sparkles className="h-4 w-4 mr-2" />
                          Generate Mindmap
                        </>
                      )}
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* AI Process Info */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Brain className="h-5 w-5" />
                  <span>AI Processing Steps</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <div className="w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center">
                      <span className="text-xs font-medium text-blue-600">1</span>
                    </div>
                    <span className="text-sm">Text preprocessing and sentence splitting</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center">
                      <span className="text-xs font-medium text-blue-600">2</span>
                    </div>
                    <span className="text-sm">Semantic embedding generation</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center">
                      <span className="text-xs font-medium text-blue-600">3</span>
                    </div>
                    <span className="text-sm">Concept clustering and classification</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center">
                      <span className="text-xs font-medium text-blue-600">4</span>
                    </div>
                    <span className="text-sm">Mind map structure generation</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Sample Texts */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Sample Texts</CardTitle>
                <CardDescription>
                  Try these examples to see how the AI works
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {sampleTexts.map((sample, index) => (
                  <div
                    key={index}
                    className="p-3 border rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
                    onClick={() => setText(sample.text)}
                  >
                    <h4 className="font-medium text-sm mb-1">{sample.title}</h4>
                    <p className="text-xs text-gray-600 line-clamp-2">
                      {sample.text.substring(0, 100)}...
                    </p>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Tips */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Tips for Better Results</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="text-sm space-y-2">
                  <div className="flex items-start space-x-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-2"></div>
                    <span>Use clear, descriptive sentences</span>
                  </div>
                  <div className="flex items-start space-x-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-2"></div>
                    <span>Include multiple related topics</span>
                  </div>
                  <div className="flex items-start space-x-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-2"></div>
                    <span>Mention specific details and examples</span>
                  </div>
                  <div className="flex items-start space-x-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-2"></div>
                    <span>Keep text between 100-2000 characters</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Status */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">AI Status</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Embeddings</span>
                    <Badge variant="outline" className="bg-green-100 text-green-800 text-xs">
                      Online
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Classification</span>
                    <Badge variant="outline" className="bg-green-100 text-green-800 text-xs">
                      Online
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Summarization</span>
                    <Badge variant="outline" className="bg-green-100 text-green-800 text-xs">
                      Online
                    </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
