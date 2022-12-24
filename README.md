

### curl examples

```sh
curl -XPOST -H 'Content-type: application/json' http://localhost:8000/api/login/ -d '{"username": "admin@admin.com", "password": "admin@admin.com"}' | jq .
```
