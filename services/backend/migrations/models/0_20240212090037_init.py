from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "budget" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "amount" DECIMAL(10,2) NOT NULL,
    "created_at" DATE NOT NULL,
    "source_one" VARCHAR(225) NOT NULL UNIQUE,
    "source_two" VARCHAR(225) NOT NULL UNIQUE,
    "source_three" VARCHAR(225) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "periods" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "nr" INT NOT NULL UNIQUE,
    "start_date" DATE NOT NULL UNIQUE,
    "end_date" DATE NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "full_name" VARCHAR(50) NOT NULL,
    "password" VARCHAR(128) NOT NULL,
    "active" BOOL NOT NULL  DEFAULT True,
    "superuser" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "variable_entries" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(225) NOT NULL,
    "amount" DECIMAL(10,2) NOT NULL,
    "supplier" VARCHAR(225) NOT NULL,
    "qualification" VARCHAR(10) NOT NULL  DEFAULT 'Want',
    "note" TEXT NOT NULL,
    "created_at" DATE NOT NULL,
    "author_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "variable_entries"."qualification" IS 'Need: Need\nWant: Want\nLeisure: Leasure\nUnexpected: Unexpected';
CREATE TABLE IF NOT EXISTS "fixed_entries" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(225) NOT NULL UNIQUE,
    "amount" DECIMAL(10,2) NOT NULL,
    "supplier" VARCHAR(225) NOT NULL,
    "qualification" VARCHAR(10) NOT NULL  DEFAULT 'Need',
    "note" TEXT NOT NULL,
    "created_at" DATE NOT NULL,
    "interval" VARCHAR(7) NOT NULL  DEFAULT 'Monthly',
    "author_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "fixed_entries"."qualification" IS 'Need: Need\nWant: Want\nLeisure: Leasure\nUnexpected: Unexpected';
COMMENT ON COLUMN "fixed_entries"."interval" IS 'Weekly: Weekly\nMonthly: Monthly\nYearly: Yearly';
CREATE TABLE IF NOT EXISTS "savingsgoal" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(225) NOT NULL,
    "amount" DECIMAL(10,2) NOT NULL,
    "description" TEXT NOT NULL,
    "author_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
