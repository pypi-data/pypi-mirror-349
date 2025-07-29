# dbdev-docker

**dbdev-docker** is a CLI tool for developers to automate the creation and management of SQL database containers using Docker.
It supports multiple database engines (MySQL, PostgreSQL, MariaDB, and more), secure credential generation, and an extensible modular codebase—perfect for local development and quick database prototyping.

---

## 🚀 Features

* **Easy CLI:** Create, list, and remove database containers via the command line
* **Multi-DB Support:** MySQL, PostgreSQL, MariaDB (easy to extend for more)
* **Secure Credentials:** Generates strong random passwords
* **Configurable:** Uses environment variables and .env files
* **Logging & Error Handling:** Robust and production-oriented
* **Extensible:** Clean, modular Python code ready for new features
* **Can run via Docker:** No Python install needed if you prefer using containers

---

## 📦 Requirements

* **Docker** (must be installed and running on your machine)

  * [Get Docker](https://docs.docker.com/get-docker/)
* **Python 3.8+** (for installation via pip)

---

## 🔧 Installation

### Install via pip (recommended)

```bash
pip install dbdev-docker
```

Or, for development:

```bash
git clone https://github.com/leticiamantovani/dbdev-docker.git
cd dbdev-docker
pip install -e .
```

---

### Run via Docker

If you don't want to install Python or dependencies, you can use the CLI inside a Docker container.

**Build the Docker image:**

```bash
docker build -t dbdev .
```

**Run a command (example: list containers):**

```bash
docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  dbdev list
```

> **Note:**
> You must mount the Docker socket (`-v /var/run/docker.sock:/var/run/docker.sock`) for the CLI inside the container to control Docker on your host machine.

---

## ⚡ Usage Examples

### Show help

```bash
dbdev --help
```

### Create a new database container

```bash
dbdev create --image mysql --db mydb --user devuser --password mypass --root-password rootpass
```

* `--image`: Database image (mysql, postgres, mariadb) [DEFAULT: mysql]
* `--db`: Name of the database to create [REQUIRED]
* `--user`: Database user [OPTIONAL, random if not provided]
* `--password`: User's password [OPTIONAL, random if not provided]
* `--root-password`: Root/admin password [OPTIONAL, random if not provided]

### List all managed containers

```bash
dbdev list
```

### Get details of a specific container

```bash
dbdev info ${db_name} [RE]
```

* `db_name`: Name of the database to create [REQUIRED]

### Remove a database container

```bash
dbdev remove --id <container_id>
```

* `--id`: ID of the container to remove [REQUIRED]

---

## ⚙️ Configuration

You can use a `.env` file to define default values:

```
DEFAULT_DB_IMAGE=mysql
DEFAULT_DB_PORT=3306
```

---

## 🐳 Supported Database Images

* **MySQL** (default)
* **PostgreSQL**
* **MariaDB**

Want support for another image? Open a pull request or submit a feature request!

---

## 🛠️ Development & Contribution

Contributions are welcome! To set up for local development:

```bash
git clone https://github.com/leticiamantovani/dbdev-docker.git
cd dbdev-docker
pip install -e .
pip install pytest
```

To run the tests:

```bash
pytest tests/
```

To add a new database image:

* Edit `src/docker_manager.py`, add the image config in `DB_IMAGES`.

Open an issue or pull request with your improvements or bug reports.

---

## 🚨 Troubleshooting

* **Docker not installed/running:**
  Make sure Docker is installed and running on your machine before running any commands.
* **Permission denied on docker.sock:**
  On Linux, you might need to add your user to the `docker` group or use `sudo`.

---

## 📝 License

MIT License. See [LICENSE](LICENSE) for details.

---

## ⭐ Credits

Created by [Leticia Mantovani](https://github.com/leticiamantovani).
Contributions, feedback, and issues are very welcome!

---

> *If you use and like this project, please give it a ⭐ on GitHub!*
