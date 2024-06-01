FROM python:3.10.11

EXPOSE 8501
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY app.py /app/app.py
COPY chat.py /app/chat.py
COPY login.py /app/login.py
COPY styles.py /app/styles.py
WORKDIR /app
CMD ["streamlit", "run", "app.py"]
