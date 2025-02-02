CREATE APPLICATION ROLE IF NOT EXISTS appnr_role;

CREATE OR ALTER VERSIONED SCHEMA code;
GRANT USAGE ON SCHEMA code TO APPLICATION ROLE appnr_role;

-- typical callback to manage external reference (ADD/REMOVE/CLEAR)
create or replace procedure code.update_reference(
   name string, oper string, alias string)
   returns string
   language sql
as
begin
   case (oper)
      when 'ADD' then select system$set_reference(:name, :alias);
      when 'REMOVE' then select system$remove_reference(:name, :alias);
      when 'CLEAR' then select system$remove_all_references();
      else return 'Unknown operation: ' || oper;
   end case;
   return 'Success';
end;
grant usage on procedure code.update_reference(string, string, string)
   to application role appnr_role;

CREATE STREAMLIT IF NOT EXISTS code.streamlit
    FROM '/'
    MAIN_FILE = 'streamlit.py'
    TITLE = 'Streamlit Native App with Ref';
GRANT USAGE ON STREAMLIT code.streamlit
    TO APPLICATION ROLE appnr_role;
