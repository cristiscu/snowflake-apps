FROM python:3.10-slim-buster
COPY app.py ./
COPY requirements.txt ./
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]