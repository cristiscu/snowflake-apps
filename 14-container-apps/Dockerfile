FROM python:3.10-slim-buster
COPY app.py ./
RUN pip install snowflake-snowpark-python[pandas], streamlit, matplotlib
CMD ["streamlit", "run", "app.py"]