-- run in Terminal: snow sql -f deploy.sql -c test_conn

DROP APPLICATION IF EXISTS fake CASCADE;
DROP APPLICATION PACKAGE IF EXISTS fake_package;
CREATE APPLICATION PACKAGE fake_package;
USE APPLICATION PACKAGE fake_package;

CREATE SCHEMA IF NOT EXISTS shared;
USE SCHEMA shared;
GRANT USAGE ON SCHEMA shared TO SHARE IN APPLICATION PACKAGE fake_package;

CREATE STAGE IF NOT EXISTS stage1;
PUT file://./app/manifest.yml @stage1/fake AUTO_COMPRESS=FALSE;
PUT file://./app/environment.yml @stage1/fake AUTO_COMPRESS=FALSE;
PUT file://./app/README.md @stage1/fake AUTO_COMPRESS=FALSE;
PUT file://./app/setup.sql @stage1/fake AUTO_COMPRESS=FALSE;
PUT file://./app/streamlit.py @stage1/fake AUTO_COMPRESS=FALSE;
LIST @stage1;

CREATE APPLICATION fake
    FROM APPLICATION PACKAGE fake_package
    USING @stage1/fake;
