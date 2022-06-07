DROP TABLE IF EXISTS accounts cascade;
DROP TABLE IF EXISTS posts cascade;
-- DROP TABLE IF EXISTS comments cascade;
-- DROP TABLE IF EXISTS tsohits cascade;
-- DROP TABLE IF EXISTS votes cascade;

CREATE TABLE accounts (
  id SERIAL PRIMARY KEY,
  username VARCHAR(30) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL
);

CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  author_id INTEGER REFERENCES accounts (id) NOT NULL,
  creation_date TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc'),
  title VARCHAR(300) NOT NULL,
  body TEXT NOT NULL
);

-- comments are a tree
-- definitely inefficient, but it doesn't matter now
-- CREATE TABLE comments (
--   id SERIAL PRIMARY KEY,
--   author_id INTEGER REFERENCES accounts (id) NOT NULL,
--   parent_id INTEGER REFERENCES comments (id),
--   post_id INTEGER REFERENCES posts (id) NOT NULL,
--   creation_date TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc'),
--   body TEXT NOT NULL
-- );

-- CREATE TABLE subtsohits (
--   id SERIAL PRIMARY KEY,
--   sub_name VARCHAR(30) UNIQUE NOT NULL
-- );

-- CREATE TABLE votes (
--   id SERIAL PRIMARY KEY,
--   post_id INTEGER REFERENCES posts (id),
--   comment_id INTEGER REFERENCES comments (id),
--   vote_value INTEGER NOT NULL CHECK (vote_value IN (1, -1))  -- 1 or -1
-- );