FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

COPY templates/ ./templates/

EXPOSE 5000

HEALTHCHECK --interval=3s --timeout=2s --start-period=2s --retries=2 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["python", "app.py"]