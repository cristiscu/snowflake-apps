REM run these one by one in a terminal

docker build --rm --platform linux/amd64 -t fake-job .

docker run -it -p 8501:8501 -e SNOWFLAKE_ACCOUNT -e SNOWFLAKE_USER -e SNOWFLAKE_PASSWORD fake-job

docker tag fake-job yictmgu-xtractpro-std.registry.snowflakecomputing.com/test/public/repo/fake-job

docker login yictmgu-xtractpro-std.registry.snowflakecomputing.com -u cristiscu

docker push yictmgu-xtractpro-std.registry.snowflakecomputing.com/test/public/repo/fake-job

docker rmi -f fake-job