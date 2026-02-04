interface FilterBarProps {
  selectedSource: string
  setSelectedSource: (source: string) => void
  searchQuery: string
  setSearchQuery: (query: string) => void
}

export default function FilterBar({
  selectedSource,
  setSelectedSource,
  searchQuery,
  setSearchQuery,
}: FilterBarProps) {
  const sources = ['전체', '치의신보', '치과신문', '덴탈아리랑']

  return (
    <div className="mb-8 space-y-4">
      {/* 언론사 필터 */}
      <div className="flex flex-wrap gap-3">
        {sources.map(source => (
          <button
            key={source}
            onClick={() => setSelectedSource(source)}
            className={`
              px-5 py-2.5 rounded-lg font-medium transition-all duration-200
              ${
                selectedSource === source
                  ? 'bg-primary text-white shadow-md scale-105'
                  : 'bg-white text-gray-700 hover:bg-gray-100 shadow-sm'
              }
            `}
          >
            {source}
          </button>
        ))}
      </div>

      {/* 검색 바 */}
      <div className="relative">
        <input
          type="text"
          placeholder="기사 제목이나 내용으로 검색..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full px-5 py-3.5 pl-12 bg-white rounded-lg shadow-sm border border-gray-200 focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-all"
        />
        <svg
          className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
      </div>
    </div>
  )
}
