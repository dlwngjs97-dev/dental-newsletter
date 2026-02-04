'use client'

import { useState, useEffect } from 'react'
import Header from '@/components/Header'
import ArticleCard from '@/components/ArticleCard'
import FilterBar from '@/components/FilterBar'

interface Article {
  id: number
  source: string
  title: string
  url: string
  thumbnail: string
  content: string
  author: string
  published_date: string
  category: string
}

export default function Home() {
  const [articles, setArticles] = useState<Article[]>([])
  const [filteredArticles, setFilteredArticles] = useState<Article[]>([])
  const [selectedSource, setSelectedSource] = useState<string>('전체')
  const [searchQuery, setSearchQuery] = useState<string>('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchArticles()
  }, [])

  useEffect(() => {
    filterArticles()
  }, [selectedSource, searchQuery, articles])

  const fetchArticles = async () => {
    try {
      // 실제 환경에서는 API 엔드포인트 또는 정적 JSON 파일에서 가져옴
      const response = await fetch('/data/articles.json')
      if (response.ok) {
        const data = await response.json()
        setArticles(data)
      } else {
        // 데이터 없을 경우 샘플 데이터
        setArticles(getSampleArticles())
      }
    } catch (error) {
      console.error('기사 불러오기 실패:', error)
      setArticles(getSampleArticles())
    } finally {
      setLoading(false)
    }
  }

  const filterArticles = () => {
    let filtered = articles

    // 언론사 필터
    if (selectedSource !== '전체') {
      filtered = filtered.filter(article => article.source === selectedSource)
    }

    // 검색 필터
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(article =>
        article.title.toLowerCase().includes(query) ||
        article.content.toLowerCase().includes(query)
      )
    }

    setFilteredArticles(filtered)
  }

  const getSampleArticles = (): Article[] => {
    return [
      {
        id: 1,
        source: '치의신보',
        title: '치과 뉴스레터 서비스를 시작합니다',
        url: '#',
        thumbnail: '',
        content: '치과 업계의 주요 뉴스를 한곳에서 확인할 수 있는 서비스입니다.',
        author: '',
        published_date: new Date().toISOString().split('T')[0],
        category: '치과'
      }
    ]
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      <Header />

      <main className="container-custom py-8">
        <FilterBar
          selectedSource={selectedSource}
          setSelectedSource={setSelectedSource}
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
        />

        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        ) : (
          <>
            <div className="mb-6 text-gray-600">
              총 <span className="font-semibold text-primary">{filteredArticles.length}</span>개의 기사
            </div>

            {filteredArticles.length === 0 ? (
              <div className="text-center py-20">
                <div className="text-gray-400 text-lg mb-2">📰</div>
                <p className="text-gray-500">검색 결과가 없습니다</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredArticles.map(article => (
                  <ArticleCard key={article.id} article={article} />
                ))}
              </div>
            )}
          </>
        )}
      </main>

      <footer className="bg-white border-t mt-20 py-8">
        <div className="container-custom text-center text-gray-500 text-sm">
          <p>치과 뉴스레터 - 치과 업계 뉴스 한눈에</p>
          <p className="mt-2">치의신보 · 치과신문 · 덴탈아리랑</p>
        </div>
      </footer>
    </div>
  )
}
