-- run in Terminal: snow sql -f deploy.sql -c test_conn

DROP APPLICATION IF EXISTS appnr CASCADE;
DROP APPLICATION PACKAGE IF EXISTS appnr_package;
CREATE APPLICATION PACKAGE appnr_package;
USE APPLICATION PACKAGE appnr_package;

CREATE SCHEMA IF NOT EXISTS shared;
USE SCHEMA shared;
GRANT USAGE ON SCHEMA shared TO SHARE IN APPLICATION PACKAGE appnr_package;

CREATE STAGE IF NOT EXISTS stage1;
PUT file://./app/manifest.yml @stage1/appnr AUTO_COMPRESS=FALSE;
PUT file://./app/environment.yml @stage1/appnr AUTO_COMPRESS=FALSE;
PUT file://./app/setup.sql @stage1/appnr AUTO_COMPRESS=FALSE;
PUT file://./app/streamlit.py @stage1/appnr AUTO_COMPRESS=FALSE;
LIST @stage1;

CREATE APPLICATION appnr
    FROM APPLICATION PACKAGE appnr_package
    USING @stage1/appnr;
