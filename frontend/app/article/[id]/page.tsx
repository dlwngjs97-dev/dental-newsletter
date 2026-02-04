'use client'

import { useParams, useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
import Header from '@/components/Header'

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

export default function ArticleDetail() {
  const params = useParams()
  const router = useRouter()
  const [article, setArticle] = useState<Article | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchArticle()
  }, [params.id])

  const fetchArticle = async () => {
    try {
      const response = await fetch('/data/articles.json')
      if (response.ok) {
        const data = await response.json()
        const found = data.find((a: Article) => a.id === parseInt(params.id as string))
        setArticle(found || null)
      }
    } catch (error) {
      console.error('기사 불러오기 실패:', error)
    } finally {
      setLoading(false)
    }
  }

  const getSourceColor = (source: string) => {
    switch (source) {
      case '치의신보':
        return 'bg-blue-100 text-blue-700'
      case '치과신문':
        return 'bg-green-100 text-green-700'
      case '덴탈아리랑':
        return 'bg-purple-100 text-purple-700'
      default:
        return 'bg-gray-100 text-gray-700'
    }
  }

  const formatDate = (dateString: string) => {
    if (!dateString) return ''
    try {
      const date = new Date(dateString)
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    } catch {
      return dateString
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
        <Header />
        <div className="container-custom py-20 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
        </div>
      </div>
    )
  }

  if (!article) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
        <Header />
        <div className="container-custom py-20 text-center">
          <div className="text-gray-400 text-6xl mb-4">📰</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-4">기사를 찾을 수 없습니다</h2>
          <button
            onClick={() => router.push('/')}
            className="btn-primary"
          >
            홈으로 돌아가기
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      <Header />

      <main className="container-custom py-8">
        {/* 뒤로 가기 */}
        <button
          onClick={() => router.push('/')}
          className="flex items-center gap-2 text-gray-600 hover:text-primary mb-6 transition-colors"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          <span>목록으로</span>
        </button>

        {/* 기사 컨테이너 */}
        <article className="bg-white rounded-2xl shadow-lg overflow-hidden max-w-4xl mx-auto">
          {/* 썸네일 */}
          {article.thumbnail && (
            <div className="relative h-96 bg-gray-100">
              <img
                src={article.thumbnail}
                alt={article.title}
                className="w-full h-full object-cover"
                onError={(e) => {
                  e.currentTarget.style.display = 'none'
                }}
              />
            </div>
          )}

          {/* 내용 */}
          <div className="p-8 md:p-12">
            {/* 메타 정보 */}
            <div className="flex items-center gap-4 mb-6">
              <span className={`badge ${getSourceColor(article.source)}`}>
                {article.source}
              </span>
              <span className="text-sm text-gray-500">
                {formatDate(article.published_date)}
              </span>
            </div>

            {/* 제목 */}
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6 leading-tight">
              {article.title}
            </h1>

            {/* 구분선 */}
            <div className="border-t border-gray-200 my-8"></div>

            {/* 본문 */}
            <div className="prose prose-lg max-w-none">
              <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                {article.content}
              </p>
            </div>

            {/* 원문 보기 버튼 */}
            <div className="mt-12 pt-8 border-t border-gray-200">
              <a
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-600 to-cyan-600 text-white px-8 py-4 rounded-xl font-semibold hover:from-blue-700 hover:to-cyan-700 transition-all duration-200 shadow-lg hover:shadow-xl"
              >
                <span>원문 보기</span>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </a>
              <p className="text-sm text-gray-500 mt-4">
                {article.source} 웹사이트에서 전체 기사를 확인할 수 있습니다.
              </p>
            </div>
          </div>
        </article>

        {/* 목록으로 버튼 */}
        <div className="text-center mt-8">
          <button
            onClick={() => router.push('/')}
            className="text-gray-600 hover:text-primary font-medium transition-colors"
          >
            ← 다른 기사 보기
          </button>
        </div>
      </main>
    </div>
  )
}
