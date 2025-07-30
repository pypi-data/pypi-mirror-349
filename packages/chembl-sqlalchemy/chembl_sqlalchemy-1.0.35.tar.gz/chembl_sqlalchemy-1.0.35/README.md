# chembl-sqlalchemy

SQLAlchemy ORM models for the [ChEMBL](https://www.ebi.ac.uk/chembl/) database, enabling programmatic access to ChEMBL data using Python.

This package allows you to query and explore ChEMBL bioactivity data using SQLAlchemy, without having to manually define the table schemas yourself.

---

## Installation

Install via pip:

```bash
pip install chembl-sqlalchemy
```

---

## Usage

```python
from chembl_sqlalchemy import Activities
from sqlalchemy import create_engine, select, sessionmaker

# Connect to a local ChEMBL SQLite database
engine = create_engine("sqlite:///chembl_35.db")
Session = sessionmaker(bind=engine)
session = Session()

# Example query: Get first 1000 non-null pChEMBL values
query = (
    select(Activities.molregno, Activities.pchembl_value, Activities.standard_type)
    .where(Activities.pchembl_value.isnot(None))
    .limit(1000)
)

results = session.execute(query).fetchall()

for molregno, pchembl_value, standard_type in results:
    print(molregno, pchembl_value, standard_type)
```

---

## Versioning

The versioning scheme is:

```
MAJOR.MINOR.CHEMBL_VERSION
```

For example:

* `1.0.35` → First release of the ORM wrapper
* `1.1.35` → Minor enhancements to the ORM wrapper

Each package version explicitly corresponds to a specific ChEMBL database version to avoid compatibility issues.

---

## Database Files

The package does **not** include the ChEMBL database file itself. You can download the corresponding SQLite file from the [ChEMBL downloads page](https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/).

Place it in your project directory or reference it by path when creating the SQLAlchemy engine.

---

## License

This project is licensed under the MIT License.
