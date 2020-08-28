# Quickstart

```
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web pytest -vs

http://127.0.0.1:8000/
```

# API Reference

**/api/pet/** — GET, POST
**/api/pet/<pet_id>** — GET, PUT, DELETE
**/api/lot/** — GET, POST
**/api/lot/<lot_pk>/** — GET, PUT, DELETE
**/api/lot/<lot_pk>/bid/** — GET, POST
**/api/lot/<lot_pk>/bid/<bid_pk>/** — GET, PUT, DELETE
**/api/lot/<lot_pk>/bid/<bid_pk>/accept** — POST

Use DRF web interface to see available fields.