import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: '치과 뉴스레터 - 치과 업계 뉴스 한눈에',
  description: '치의신보, 치과신문, 덴탈아리랑의 최신 뉴스를 한곳에서 확인하세요',
  keywords: '치과, 치과뉴스, 치의신보, 치과신문, 덴탈아리랑, 치과업계',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ko">
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
}
