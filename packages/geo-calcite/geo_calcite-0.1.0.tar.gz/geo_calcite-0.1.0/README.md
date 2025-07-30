# Geo-Calcite Python Client

[![PyPI version](https://img.shields.io/pypi/v/geo-calcite.svg)](https://pypi.org/project/geo-calcite) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

A lightweight Python client for interacting with the Geo-Calcite API.  
Provides helpers for connecting to, refreshing, querying, and disconnecting from Geo-Calcite data sources over HTTP, and returns results as native Python objects or pandas DataFrames.

---

## Features

- **Connect** to one or more Geo-Calcite data sources by DID (data identifier)  
- **Refresh** existing connections  
- **Disconnect** from data sources  
- **Query** connected sources via SQL and return results as a pandas DataFrame  

---

## Table of Contents

- [Geo-Calcite Python Client](#geo-calcite-python-client)
  - [Features](#features)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Quickstart](#quickstart)
  - [Contributing](#contributing)
  - [License](#license)


---

## Installation

Install via pip:

```bash
pip install geo_calcite
```

---

## Quickstart

```python
from geo_calcite import GeoCalciteClient

# Create a GeoCalcite client
client = GeoCalciteClient()

# Connect to datasource
dids = [1, 2, 3]
client.connect(dids)

# Query
sql = "SELECT * FROM heat_flow.Combined_05 LIMIT 10"
df = client.query(sql)
print(df)

# Disconnect from datasource
client.disconnect(dids)
```

---

## Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch: git checkout -b feature/foo
3. Commit your changes: git commit -am 'Add foo feature'
4. Push to the branch: git push origin feature/foo
5. Open a Pull Request

---

## License
This project is licensed under the Apache License, Version 2.0. See the LICENSE file for details.