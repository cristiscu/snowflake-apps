-- to be deployed as a Streamlit App with: snow sql -f deploy.sql -c test_conn
use schema test.public;

create stage if not exists stage1;

put file://./Main.py @stage1/app2 overwrite=true auto_compress=false;
put file://./utils.py @stage1/app2 overwrite=true auto_compress=false;
put file://./environment.yml @stage1/app2 overwrite=true auto_compress=false;
put file://./pages/*.py @stage1/app2/pages overwrite=true auto_compress=false;

create or replace streamlit app2
    root_location = '@test.public.stage1/app2'
    main_file = 'Main.py'
    query_warehouse = 'compute_wh'
    title = 'This is a multi-page Streamlit App';

show streamlits;