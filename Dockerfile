FROM python:slim AS python-builder

RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

RUN python3 generate.py

# ----------------------

FROM node:lts-slim AS node-builder

RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=python-builder /app /app

RUN npm install -g bower

RUN bower install --allow-root

# ----------------------

FROM nginx:alpine AS runtime
RUN rm -rf /usr/share/nginx/html/*
COPY --from=node-builder /app/web /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]