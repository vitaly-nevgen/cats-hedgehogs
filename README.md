# Quickstart

```
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web pytest -vs

http://127.0.0.1:8000/
```

# API Reference

**/api/pet/** — GET, POST<br/>
**/api/pet/<pet_id>** — GET, PUT, DELETE<br/>
**/api/lot/** — GET, POST<br/>
**/api/lot/<lot_id>/** — GET, PUT, DELETE<br/>
**/api/lot/<lot_id>/bid/** — GET, POST<br/>
**/api/lot/<lot_id>/bid/<bid_id>/** — GET, PUT, DELETE<br/>
**/api/lot/<lot_id>/bid/<bid_id>/accept** — POST<br/>

Use DRF web interface to see available fields.