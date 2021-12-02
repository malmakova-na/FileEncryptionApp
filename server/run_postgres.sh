docker run \
    -d \
    -p 5432:5432 \
    -e POSTGRES_DB=postgres_db \
    -e POSTGRES_USER=test_user \
    -e POSTGRES_PASSWORD=test_pwd \
    -e POSTGRES_HOST=127.0.0.1 \
    -e POSTGRES_PORT=5432 \
    postgres