FROM python:3.12-alpine AS build
WORKDIR /app
COPY pyproject.toml app.py ./
RUN pip install --no-cache-dir .

FROM python:3.12-alpine
WORKDIR /app
ENV PORT=8080 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN adduser -D -u 10001 app
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY app.py ./
USER app
EXPOSE 8080
CMD ["python", "app.py"]
