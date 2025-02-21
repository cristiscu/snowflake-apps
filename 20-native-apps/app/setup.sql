CREATE APPLICATION ROLE IF NOT EXISTS fake_role;

CREATE OR ALTER VERSIONED SCHEMA code;
GRANT USAGE ON SCHEMA code TO APPLICATION ROLE fake_role;

CREATE STREAMLIT IF NOT EXISTS code.streamlit
    FROM '/'
    MAIN_FILE = 'streamlit.py'
    TITLE = 'Fake Data Generator';
GRANT USAGE ON STREAMLIT code.streamlit
    TO APPLICATION ROLE fake_role;
