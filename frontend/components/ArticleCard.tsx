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

interface ArticleCardProps {
  article: Article
}

export default function ArticleCard({ article }: ArticleCardProps) {
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
      const now = new Date()
      const diffTime = Math.abs(now.getTime() - date.getTime())
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))

      if (diffDays === 0) return '오늘'
      if (diffDays === 1) return '어제'
      if (diffDays < 7) return `${diffDays}일 전`

      return dateString
    } catch {
      return dateString
    }
  }

  return (
    <a
      href={`/article/${article.id}`}
      className="card block overflow-hidden group"
    >
      {/* 썸네일 */}
      {article.thumbnail && (
        <div className="relative h-48 bg-gray-100 overflow-hidden">
          <img
            src={article.thumbnail}
            alt={article.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            onError={(e) => {
              e.currentTarget.style.display = 'none'
            }}
          />
        </div>
      )}

      {/* 내용 */}
      <div className="p-5">
        {/* 언론사 뱃지 */}
        <div className="flex items-center justify-between mb-3">
          <span className={`badge ${getSourceColor(article.source)}`}>
            {article.source}
          </span>
          <span className="text-xs text-gray-400">
            {formatDate(article.published_date)}
          </span>
        </div>

        {/* 제목 */}
        <h3 className="font-semibold text-lg text-gray-900 mb-2 line-clamp-2 group-hover:text-primary transition-colors">
          {article.title}
        </h3>

        {/* 내용 미리보기 */}
        {article.content && (
          <p className="text-sm text-gray-600 line-clamp-3">
            {article.content}
          </p>
        )}

        {/* 읽기 링크 */}
        <div className="mt-4 flex items-center text-primary text-sm font-medium group-hover:gap-2 transition-all">
          <span>자세히 보기</span>
          <svg
            className="w-4 h-4 group-hover:translate-x-1 transition-transform"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5l7 7-7 7"
            />
          </svg>
        </div>
      </div>
    </a>
  )
}
