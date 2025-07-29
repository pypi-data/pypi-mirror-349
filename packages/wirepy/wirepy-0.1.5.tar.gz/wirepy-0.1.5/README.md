# Wirepy

Wirepy is a Python project scaffolding tool designed to accelerate the development of FastAPI-based applications. It provides a command-line interface (CLI) to generate boilerplate code, manage migrations, and organize your project structure following best practices.

## Features
- **CLI Tooling**: Easily scaffold new FastAPI projects and components.
- **Project Templates**: Predefined templates for controllers, models, routes, schemas, services, and core utilities.
- **Database Integration**: Built-in support for database configuration and migrations using Alembic.
- **Environment Management**: Template for `.env` and requirements management.

## Folder Structure

```
wirepy/
├── wirepy/
│   ├── __init__.py
│   ├── cli.py
│   ├── scaffold.py
│   ├── migrations.py
│   └── templates/
│        ├── app/
│        │   ├── controllers/
│        │   ├── models/
│        │   ├── routes/
│        │   ├── schemas/
│        │   ├── services/
│        │   └── core/
│        │       ├── config.py
│        │       └── database.py
│        ├── __init__.py
│        ├── alembic/
│        ├── alembic.ini
│        ├── main.py
│        ├── .env
│        ├── requirements.txt
│        └── README.md
├── pyproject.toml
├── venv (your local virtual environment)
├── README.md
├── LICENSE
```

## Getting Started

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd wirepy
   ```
2. **Create a virtual environment:**
   ```sh
   python3 -m venv vvenv
   source vvenv/bin/activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r wirepy/templates/requirements.txt
   ```
4. **Use the CLI to scaffold a new project or component:**
   ```sh
   python -m wirepy.cli <command>
   ```

## License

This project is licensed under the terms of the MIT License. See the `LICENSE` file for details.
