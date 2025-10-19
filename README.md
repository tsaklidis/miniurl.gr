# MiniURL

[![python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![db](https://img.shields.io/badge/db-sqlmodel-7e56c2)](https://sqlmodel.tiangolo.com/)
![Codecov](https://img.shields.io/codecov/c/github/tsaklidis/miniurl.gr?logo=codecov)
[![Last Commit](https://img.shields.io/github/last-commit/tsaklidis/miniurl.gr.svg)](https://github.com/tsaklidis/miniurl.gr/commits/main)

---


## The fastest way to minify your links

MiniURL is a fast, lightweight, and modern URL shortener built with Python and SQLModel. <br>
Easily minify your links with a simple interface.<br>

Because your links deserve to be short and sweet.

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
- **Cache:** Redis
- **Database:** SQLModel (SQLAlchemy + Pydantic)
- **Containerization:** Docker
- **Testing:** Pytest, Codecov

## 📊 Stats
<img src="image.png" alt="Project structure showing image.png in red" style="max-width:80%; border-radius:8px;">

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
- `GET /stats/{alias}` — Get click statistics (TODO)

## 💡 Example Usage

```python
import requests

data = {"url": "https://www.example.com"}
response = requests.post("https://miniurl.gr/api/v1.0/minify", json=data)
print(response.json())
```

## 📝 Contributing

Pull requests and issues are welcome!

## 📄 License

Licensed under the [MIT License](LICENSE).

