

For development, we will use docker compose to s3 comptible with minio and kafka minio,jupter notebook with spark and delta lake and kafka

```
docker compose build # build the docker images
docker compose up
```

In production, we can host it through kubernetes and use the helm chart to deploy it.


Open http://127.0.0.1:8888/lab/tree/quickstart.ipynb
