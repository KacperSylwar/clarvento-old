#!/bin/bash
set -e

echo "=== Clar — deploy produkcyjny ==="

# Buduj obrazy
docker compose -f docker-compose.prod.yml build --no-cache

# Uruchom bazę i redis najpierw
docker compose -f docker-compose.prod.yml up -d db redis
echo "Czekam na bazę danych..."
sleep 5

# Uruchom wszystko (entrypoint.sh wykona migracje automatycznie)
docker compose -f docker-compose.prod.yml up -d

echo ""
echo "=== Gotowe! ==="
echo "Backend:  accutrace.of-course.pl → localhost:4004"
echo "Frontend: v1.of-course.pl        → localhost:4005"
echo ""
echo "Seed danych testowych:"
echo "  docker compose -f docker-compose.prod.yml exec backend uv run python manage.py seed_data"
