CREATE TABLE IF NOT EXISTS website_likes (
  visitor_id TEXT PRIMARY KEY
    CHECK (length(visitor_id) BETWEEN 20 AND 80),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
