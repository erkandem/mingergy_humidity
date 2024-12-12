# Dockerfile for the dash version
# huge image, needs cleanup of requirements
#  - matplotlib not needed
#  - pandas could be facored out, seems just for convenience? Performance change?
# Build and run with:
#     docker build -t dash-app
#     docker run  -p 8050:8050 dash-app
FROM python:3.12-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
COPY humidity.py .
COPY dash_app.py .
EXPOSE 8050
CMD ["gunicorn", "dash_app:server", "--workers", "4", "--bind", "0.0.0.0:8050"]
