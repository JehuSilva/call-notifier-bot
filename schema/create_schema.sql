CREATE SCHEMA IF NOT EXISTS pizzall;
CREATE OR REPLACE TABLE pizzall.callpicks(
    id  INTEGER,
    caller_id  STRING,
    clean_caller_id  STRING,
    date  DATETIME,
    destination  STRING,
    duration  INTEGER,
    has_notes  BOOLEAN,
    person_name  STRING,
    player  BOOLEAN,
    pretty_date  STRING,
    rating  STRING,
    redirection_type  STRING,
    returned  BOOLEAN,
    status  STRING,
    tagged  BOOLEAN,
    trunk  STRING,
    trunk_description  STRING,
    uniqueid  STRING,
    update_time  DATETIME
);