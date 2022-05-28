DROP TABLE IF EXISTS accounts cascade;
DROP TABLE IF EXISTS posts cascade;

CREATE TABLE accounts (
  id SERIAL PRIMARY KEY,
  username VARCHAR(30) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL
);

CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  author_id INTEGER REFERENCES accounts (id),
  creation_date TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc'),
  title VARCHAR(300) NOT NULL,
  body TEXT NOT NULL
  );
