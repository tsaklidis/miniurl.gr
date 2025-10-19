# MiniURL

## The fastest way to minify your links

[![python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![db](https://img.shields.io/badge/db-sqlmodel-7e56c2)](https://sqlmodel.tiangolo.com/)
![Codecov](https://img.shields.io/codecov/c/github/tsaklidis/miniurl.gr?logo=codecov)
[![Last Commit](https://img.shields.io/github/last-commit/tsaklidis/miniurl.gr.svg)](https://github.com/tsaklidis/miniurl.gr/commits/main)

---

MiniURL is a blazing fast, lightweight, and modern URL shortener built with Python and SQLModel. <br>
Easily minify your links with a simple interface.

## 🚀 Features

- **High-performance link shortening**
- **RESTful API** for programmatic access
- **Admin dashboard** for managing links
- **Click statistics & analytics**
- **Custom aliases** for your links
- **Dockerized deployment**
- **Unit and integration tests** with Codecov reporting

## 📦 Tech Stack

- **Backend:** Python 3.12, FastAPI
- **Database:** SQLModel (SQLAlchemy + Pydantic)
- **Containerization:** Docker
- **Testing:** Pytest, Codecov

## 🛠️ Installation

```bash
git clone https://github.com/tsaklidis/miniurl.gr.git
cd miniurl.gr
pip install -r requirements.txt
```

Or run with Docker:

```bash
docker build -t miniurl .
docker run -p 8000:8000 miniurl
```


## 🔗 API Endpoints

- `POST /shorten` — Minify a URL
- `GET /{alias}` — Redirect to the original URL
- `GET /stats/{alias}` — Get click statistics

Explore the interactive documentation at `/docs`!

## 💡 Example Usage

```python
import requests

response = requests.post(
    "http://localhost:8000/shorten",
    json={"url": "https://www.example.com"}
)
print(response.json())
```

## 🧪 Running Tests

```bash
pytest
```

## 📝 Contributing

Pull requests and issues are welcome!

## 📄 License

Licensed under the [MIT License](LICENSE).

---

> Because your links deserve to be short and sweet.
