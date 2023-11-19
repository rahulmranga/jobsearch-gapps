CREATE TABLE listings (
 job_id                      varchar,
 employer_name               varchar,
 job_publisher               varchar,
 job_employment_type         varchar,
 job_title                   varchar,
 job_apply_link              varchar,
 job_apply_quality_score     float,
 job_posted_at_timestamp     bigint,
 job_posted_at_datetime_utc  varchar,
 job_city                    varchar,
 job_state                   varchar,
 job_country                 varchar,
 job_google_link             varchar,
 job_highlights              varchar,
 job_naics_name              varchar,
 apply_flag                  CHAR(1) DEFAULT 'N'
 );