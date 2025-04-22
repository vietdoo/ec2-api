FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

# Entrypoint for Uvicorn
CMD ["uvicorn", "vec2.app:app", "--host", "0.0.0.0", "--port", "10000"]
