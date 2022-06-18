DROP TABLE IF EXISTS accounts cascade;
DROP TABLE IF EXISTS posts cascade;
-- DROP TABLE IF EXISTS comments cascade;
DROP TABLE IF EXISTS subtsohits cascade;
-- DROP TABLE IF EXISTS votes cascade;

CREATE TABLE accounts (
  account_id SERIAL PRIMARY KEY,
  username VARCHAR(30) UNIQUE NOT NULL CHECK (username ~ '^[A-Za-z0-9_-]{3,30}$'),
  password_hash TEXT NOT NULL
);

CREATE TABLE subtsohits (
  sub_id SERIAL PRIMARY KEY,
  sub_name VARCHAR(30) UNIQUE NOT NULL CHECK (sub_name ~ '^[A-Za-z0-9_-]{3,30}$'),
  sub_title VARCHAR(60) NOT NULL,
  creator_id INTEGER REFERENCES accounts (account_id) NOT NULL
);

CREATE TABLE posts (
  post_id SERIAL PRIMARY KEY,
  author_id INTEGER REFERENCES accounts (account_id) NOT NULL,
  parent_sub_id INTEGER REFERENCES subtsohits (sub_id) NOT NULL,
  creation_date TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc'),
  title VARCHAR(300) NOT NULL,
  body TEXT NOT NULL
);

-- comments are a tree
-- definitely inefficient, but it probably doesn't matter now
CREATE TABLE comments (
  comment_id SERIAL PRIMARY KEY,
  author_id INTEGER REFERENCES accounts (account_id) NOT NULL,
  parent_id INTEGER REFERENCES comments (comment_id),
  post_id INTEGER REFERENCES posts (post_id) NOT NULL,
  creation_date TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc'),
  body TEXT NOT NULL
);

-- CREATE TABLE votes (
--   id SERIAL PRIMARY KEY,
--   post_id INTEGER REFERENCES posts (post_id),
--   comment_id INTEGER REFERENCES comments (comment_id),
--   vote_value INTEGER NOT NULL CHECK (vote_value IN (1, -1))  -- 1 or -1
-- );