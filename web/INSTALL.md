
# Instalación Rápida
1) Crear venv y activar
2) pip install -r requirements.txt
3) Copiar .env.example a .env y completar claves
4) python manage.py migrate
5) python manage.py createsuperuser
6) python manage.py loaddata demo.json  # datos de prueba (opcional)
7) python manage.py runserver
- Home: / (carrusel + destacados)
- Catálogo: /catalog/
- Carrito: /cart/
- Admin: /admin/  (Carousel slides)
- Reporting: /panel/reports/
