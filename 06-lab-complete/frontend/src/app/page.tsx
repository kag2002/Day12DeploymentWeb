'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    router.replace('/chat');
  }, [router]);

  return (
    <div className="flex items-center justify-center min-h-screen bg-[#080b13] text-slate-400">
      <div className="flex flex-col items-center gap-2">
        <div className="w-5 h-5 rounded-full border-2 border-violet-500 border-t-transparent animate-spin"></div>
        <span className="text-xs">Đang chuyển hướng...</span>
      </div>
    </div>
  );
}
