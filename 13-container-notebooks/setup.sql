CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION pypi_access
    ALLOWED_NETWORK_RULES = (snowflake.external_access.pypi_rule)
    ENABLED = true;

GRANT USAGE ON INTEGRATION pypi_access
    TO ROLE sysadmin;