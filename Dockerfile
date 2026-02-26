FROM python:alpine AS python-builder

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

RUN python3 generate.py

# ----------------------

FROM node:lts-alpine AS node-builder

WORKDIR /app
COPY --from=python-builder /app /app

# Install bower
RUN npm install -g bower

# Install frontend deps
RUN bower install --allow-root

# ----------------------

FROM nginx:alpine AS runtime

# Remove default nginx html
RUN rm -rf /usr/share/nginx/html/*

# Copy generated static site
COPY --from=node-builder /app/web /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]