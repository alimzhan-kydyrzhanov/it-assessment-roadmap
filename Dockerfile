FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["sh", "-c", "pytest -v && python -m assess.cli --out reports/assessment.md && cat reports/assessment.md"]
