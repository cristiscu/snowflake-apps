-- run in Terminal: snow sql -f deploy.sql -c test_conn

DROP APPLICATION IF EXISTS appn CASCADE;
DROP APPLICATION PACKAGE IF EXISTS appn_package;
CREATE APPLICATION PACKAGE appn_package;
USE APPLICATION PACKAGE appn_package;

CREATE SCHEMA IF NOT EXISTS shared;
USE SCHEMA shared;
GRANT USAGE ON SCHEMA shared TO SHARE IN APPLICATION PACKAGE appn_package;

CREATE STAGE IF NOT EXISTS stage1;
PUT file://./app/manifest.yml @stage1/appn AUTO_COMPRESS=FALSE;
PUT file://./app/environment.yml @stage1/appn AUTO_COMPRESS=FALSE;
PUT file://./app/README.md @stage1/appn AUTO_COMPRESS=FALSE;
PUT file://./app/setup.sql @stage1/appn AUTO_COMPRESS=FALSE;
PUT file://./app/streamlit.py @stage1/appn AUTO_COMPRESS=FALSE;
LIST @stage1;

CREATE APPLICATION appn
    FROM APPLICATION PACKAGE appn_package
    USING @stage1/appn;
