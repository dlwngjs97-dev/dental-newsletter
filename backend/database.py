import sqlite3
import json
from datetime import datetime
from pathlib import Path

class Database:
    def __init__(self, db_path='../data/articles.db'):
        self.db_path = Path(__file__).parent / db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """데이터베이스 테이블 생성"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                thumbnail TEXT,
                content TEXT,
                author TEXT,
                published_date TEXT,
                crawled_date TEXT NOT NULL,
                category TEXT
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_published_date
            ON articles(published_date DESC)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_source
            ON articles(source)
        ''')

        conn.commit()
        conn.close()

    def insert_article(self, article):
        """기사 저장 (중복 체크)"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO articles
                (source, title, url, thumbnail, content, author, published_date, crawled_date, category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                article['source'],
                article['title'],
                article['url'],
                article.get('thumbnail', ''),
                article.get('content', ''),
                article.get('author', ''),
                article.get('published_date', ''),
                datetime.now().isoformat(),
                article.get('category', '')
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # 이미 존재하는 URL
            return False
        finally:
            conn.close()

    def get_recent_articles(self, limit=50):
        """최근 기사 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, source, title, url, thumbnail, content, author, published_date, category
            FROM articles
            ORDER BY published_date DESC, id DESC
            LIMIT ?
        ''', (limit,))

        columns = ['id', 'source', 'title', 'url', 'thumbnail', 'content', 'author', 'published_date', 'category']
        articles = []

        for row in cursor.fetchall():
            article = dict(zip(columns, row))
            articles.append(article)

        conn.close()
        return articles

    def get_articles_by_source(self, source, limit=20):
        """언론사별 기사 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, source, title, url, thumbnail, content, author, published_date, category
            FROM articles
            WHERE source = ?
            ORDER BY published_date DESC, id DESC
            LIMIT ?
        ''', (source, limit))

        columns = ['id', 'source', 'title', 'url', 'thumbnail', 'content', 'author', 'published_date', 'category']
        articles = []

        for row in cursor.fetchall():
            article = dict(zip(columns, row))
            articles.append(article)

        conn.close()
        return articles

    def export_to_json(self, output_path='../data/articles.json'):
        """JSON으로 내보내기 (프론트엔드용)"""
        articles = self.get_recent_articles(limit=100)
        output_file = Path(__file__).parent / output_path

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)

        return len(articles)
