USE ROLE ACCOUNTADMIN;
USE test.public;

-- ================================================
-- create image repo (cannot drop single images)
CREATE IMAGE REPOSITORY IF NOT EXISTS repo;
SHOW IMAGE REPOSITORIES;                    -- get repo URL
SHOW IMAGES IN IMAGE REPOSITORY repo;       -- call after pushing images here

-- ================================================
-- create CPU compute pool
CREATE COMPUTE POOL IF NOT EXISTS cpu1
    INSTANCE_FAMILY=CPU_X64_XS
    MIN_NODES=1
    MAX_NODES=1
    INITIALLY_SUSPENDED=TRUE
    AUTO_SUSPEND_SECS=60;
DESC COMPUTE POOL cpu1;
ALTER COMPUTE POOL cpu1 STOP ALL;
DESC COMPUTE POOL cpu1;
SHOW COMPUTE POOLS;

-- ================================================
-- grant access to SYSADMIN
grant USAGE on database test to role SYSADMIN;
grant ALL on schema test.public to role SYSADMIN;
grant ALL on warehouse compute_wh to role SYSADMIN;

grant READ on image repository test.public.repo to role SYSADMIN;
grant USAGE, OPERATE on compute pool cpu1 to role SYSADMIN;

-- ================================================
-- create job service
USE ROLE SYSADMIN;
EXECUTE JOB SERVICE
    IN COMPUTE POOL cpu1
    FROM SPECIFICATION $$
        spec:
          containers:
          - name: fake-job-cont
            image: /test/public/repo/fake-job
    $$
    NAME=fake_job
    ASYNC=true
    QUERY_WAREHOUSE='compute_wh';   -- try first without it!
DESC SERVICE fake_job;
SHOW SERVICES;
CALL SYSTEM$GET_SERVICE_STATUS('fake_job');

SHOW SERVICE INSTANCES IN SERVICE fake_job;
SHOW SERVICE CONTAINERS IN SERVICE fake_job;
SELECT SYSTEM$GET_SERVICE_LOGS('fake_job', 0, 'fake-job-cont')

-- ================================================
-- stop all processing
ALTER SERVICE fake_job SUSPEND;
DROP SERVICE fake_job;

ALTER COMPUTE POOL cpu1 SUSPEND;
SHOW COMPUTE POOLS;
