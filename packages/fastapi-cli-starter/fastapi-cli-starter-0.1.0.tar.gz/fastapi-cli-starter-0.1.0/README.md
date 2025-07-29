# create-fastapi-app

A CLI tool to scaffold FastAPI applications with best practices baked in.  
Usage:

```bash
create-fastapi-app myproject


---

## ✅ Step 5: Build and Publish to PyPI

### 1. **Install packaging tools**

```bash
pip install setuptools wheel twine

rm -rf dist build *.egg-info

python setup.py sdist bdist_wheel
