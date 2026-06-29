-- Runs once on first container start (Postgres docker-entrypoint-initdb.d).
-- Creates a separate database used by the automated test suite so tests never
-- touch development data.
CREATE DATABASE student_tasks_test;
