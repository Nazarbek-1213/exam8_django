# Render Deploy Yo'riqnomasi

## 1. Repoga push qiling
```bash
git add .
git commit -m "Render uchun tayyorlash"
git push origin main
```

## 2. Render dashboardda
**Variant A — Blueprint (avtomatik):**
- New → Blueprint → repoyingizni tanlang
- `render.yaml` faylini Render avtomatik o'qiydi (web service + postgres)

**Variant B — qo'lda Web Service:**
1. New → Web Service → repo
2. Environment: **Python 3**
3. Build Command: `./build.sh`
4. Start Command: `gunicorn config.wsgi:application`
5. Environment Variables qo'shing:
   - `SECRET_KEY` — long random string
   - `DEBUG` — `False`
   - `PYTHON_VERSION` — `3.12.5`
   - `DATABASE_URL` — Postgres ulanish stringi (Render Postgres yaratib oling)

## 3. Database
- Render → New → PostgreSQL → free plan
- Yaratilgach `Internal Database URL` ni nusxalab `DATABASE_URL` env-ga qo'ying

## 4. Superuser yaratish (kerak bo'lsa)
Render shellda:
```bash
python manage.py createsuperuser
```

## Mahalliy ishga tushirish
```powershell
$env:DEBUG="True"
.\venv\Scripts\python.exe manage.py runserver
```
