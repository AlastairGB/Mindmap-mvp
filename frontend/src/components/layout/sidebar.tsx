'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { 
  Brain, 
  Plus, 
  Eye, 
  Settings, 
  Home,
  Zap
} from 'lucide-react';

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Create Mindmap', href: '/create', icon: Plus },
  { name: 'View Mindmaps', href: '/mindmaps', icon: Eye },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="flex h-full w-64 flex-col bg-gray-900">
      <div className="flex h-16 shrink-0 items-center px-6">
        <div className="flex items-center space-x-2">
          <Brain className="h-8 w-8 text-blue-500" />
          <span className="text-xl font-bold text-white">Mind Map AI</span>
        </div>
      </div>
      
      <nav className="flex flex-1 flex-col px-3 py-4">
        <ul role="list" className="flex flex-1 flex-col gap-y-2">
          {navigation.map((item) => {
            const isActive = pathname === item.href;
            return (
              <li key={item.name}>
                <Link
                  href={item.href}
                  className={cn(
                    'group flex gap-x-3 rounded-md p-3 text-sm font-semibold leading-6 transition-colors',
                    isActive
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                  )}
                >
                  <item.icon
                    className={cn(
                      'h-6 w-6 shrink-0',
                      isActive ? 'text-white' : 'text-gray-400 group-hover:text-white'
                    )}
                    aria-hidden="true"
                  />
                  {item.name}
                </Link>
              </li>
            );
          })}
        </ul>
        
        <div className="mt-auto p-3">
          <div className="flex items-center space-x-2 rounded-md bg-gray-800 p-3">
            <Zap className="h-5 w-5 text-yellow-500" />
            <div className="flex-1">
              <p className="text-xs font-medium text-gray-300">AI Status</p>
              <p className="text-xs text-green-400">Operational</p>
            </div>
          </div>
        </div>
      </nav>
    </div>
  );
}
