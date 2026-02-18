# PAGE ANALYEZER
Page Analyzer is a web application that analyzes websites for SEO readiness.

### Hexlet tests and linter status:
[![Actions Status](https://github.com/gbespamiatnykh/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/gbespamiatnykh/python-project-83/actions)

### CI and SonarQube status:
[![Build](https://github.com/gbespamiatnykh/python-project-83/actions/workflows/build.yml/badge.svg)](https://github.com/gbespamiatnykh/python-project-83/actions/workflows/build.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=gbespamiatnykh_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=gbespamiatnykh_python-project-83)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=gbespamiatnykh_python-project-83&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=gbespamiatnykh_python-project-83)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=gbespamiatnykh_python-project-83&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=gbespamiatnykh_python-project-83)

## Live Demo
https://python-project-83-ju0z.onrender.com
## Tech Stack
- Python 3.12
- Flask
- uv
- Gunicorn
- psycopg2
- python-dotenv
- Bootstrap
- validators
- requests
- BeautifulSoup

## Installation
### Clone the repository:
```bash
git clone git@github.com:gbespamiatnykh/python-project-83.git
```
```bash
cd python-project-83
```
### Create virtual environment and install dependencies:
```bash
make install
```
### Environment variables:
Create a '.env' file in the project root and set:
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/dbname
### Run the application:
```bash
make start
```
