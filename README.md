# BTN Product Recommender (Prototype)

A Django-based prototype web application that recommends BTN products using a decision-tree questionnaire. Includes an analytics dashboard restricted to admin/staff users.


## Requirements

* **Python 3.12.9**
* pip


## Installation Instructions

### 1. Clone the repository

```bash
git clone https://github.com/AdamSyauqi/btn-recommender.git
cd btn-recommender
```

---

### 2. Create a Python virtual environment (Python 3.12.9)

#### Windows (PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
```

#### macOS / Linux

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python --version
```

Ensure the output shows:

```text
Python 3.12.9
```

---

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a file named `.env` in the project root directory.

Example `.env`:

```env
SECRET_KEY=replace-this-with-a-long-random-secret
```

#### Generate a Django `SECRET_KEY`

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated key and paste it into `.env`.

> **Important:** Do not commit `.env` to version control.

---

### 5. Run database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Create an admin user

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

---

### 7. Run the development server

```bash
python manage.py runserver
```

Access the application:

* Questionnaire: [http://127.0.0.1:8000/q/](http://127.0.0.1:8000/q/)
* Analytics (admin only): [http://127.0.0.1:8000/analytics/](http://127.0.0.1:8000/analytics/)


## Troubleshooting

### `no such table: django_session`

Ensure migrations have been applied:

```bash
python manage.py migrate
```

### Analytics page not accessible

Only admin/staff users can access analytics. Create an admin account using:

```bash
python manage.py createsuperuser
```

## Notes
This project was made in Python 3.12.9. While other python versions may work, the author gives no guarantee as the author had not tried other python versions for this project.


## License

This project uses publicly available data from Bank BTN and is intended for academic and prototyping purposes.
