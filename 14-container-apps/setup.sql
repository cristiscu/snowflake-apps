USE ROLE SYSADMIN;
USE test.public;

SHOW IMAGES IN IMAGE REPOSITORY repo;
SHOW COMPUTE POOLS;

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
CALL SYSTEM$GET_SERVICE_STATUS('fake_job')

SHOW SERVICE INSTANCES IN SERVICE fake_job;
SHOW SERVICE CONTAINERS IN SERVICE fake_job;
SELECT SYSTEM$GET_SERVICE_LOGS('fake_job', 0, 'fake-job-cont')

ALTER SERVICE fake_job SUSPEND;
DROP SERVICE fake_job;

ALTER COMPUTE POOL cpu1 SUSPEND;
SHOW COMPUTE POOLS;
