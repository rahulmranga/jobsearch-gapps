FROM node:14 as frontend-builder

# Install PostgreSQL client library
RUN apt-get update && apt-get install -y libpq-dev build-essential

# Stage 1: Build the React frontend
WORKDIR /jobsearch

COPY app.py .
COPY utils.py .
COPY package.json .
COPY package-lock.json .
RUN npm install

COPY /public/ /jobsearch/public
COPY /src/ /jobsearch/src
RUN npm run build
COPY /build /

# Stage 2: Build the Flask app and include the frontend build
FROM python:3.9-slim

COPY requirements.txt .
RUN apt-get update && apt-get -y dist-upgrade && apt-get install -y libpq-dev

RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt


# Set environment variables for PostgreSQL connections
ENV POSTGRES_USER=my_db_user
ENV POSTGRES_PASSWORD=my_db_password
ENV POSTGRES_HOST=my_db_host
ENV POSTGRES_PORT=my_db_port
ENV POSTGRES_DB=my_db_name

WORKDIR /jobsearch
COPY --from=frontend-builder /jobsearch /jobsearch

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
