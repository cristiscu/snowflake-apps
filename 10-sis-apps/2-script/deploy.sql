-- to be deployed as a Streamlit App with: snow sql -f deploy.sql -c test_conn
use schema test.public;

create stage if not exists stage1;

put file://./app.py @stage1/app1 overwrite=true auto_compress=false;
put file://./environment.yml @stage1/app1 overwrite=true auto_compress=false;

create or replace streamlit app1
    root_location = '@test.public.stage1/app1'
    main_file = 'app.py'
    query_warehouse = 'compute_wh'
    title = 'This is a basic Streamlit App';

show streamlits;