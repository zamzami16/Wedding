# Wedding Invitation Backed API

API dapat dlihat di Postman.

## Django installation

### Create Virtual Environment

```bash
python -m venv venv

venv/scripts/activate
```

### Install Environment

```bash
pip install -r Requirements.txt
```

## Run Server

### Create Django Migrations

Pindah ke direktori wedding (yang ada file `manage.py`)

```bash
cd wedding
```

Jalankan migrasi

```bash
python manage.py makemigrations
python manage.py migrate
```

Jalankan server

```bash
python manage.py runserver
```
