# Dune Analytics

[![Python 3.5](https://img.shields.io/badge/python-3.5-blue.svg)](https://www.python.org/downloads/release/python-350/)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

-------

### Unofficial Python Library for [Dune Analytics](https://duneanalytics.com/)

The library can be used to fetch the table data from `python` backend.

#### Disclaimer: Use at your own risk! 
It may not work for some/all urls.

This library doesn't run the query, rather it fetches the query result from the backend.

### Installation:

use pip to install:

``` 
pip install duneanalytics
```

-----------

### Authentication:

You need to have `username` & `password` for [Dune Analytics](https://duneanalytics.com/)

-----------

### Example usage:

```
from duneanalytics import DuneAnalytics

# initialize client
dune = DuneAnalytics('username', 'password')

# try to login
dune.login()

# fetch token
dune.fetch_auth_token()

# fetch query result id using query id
# query id for any query can be found from the url of the query:
# for example: 
# https://duneanalytics.com/queries/4494/8769 => 4494
# https://duneanalytics.com/queries/3705/7192 => 3705
# https://duneanalytics.com/queries/3751/7276 => 3751

result_id = dune.query_result_id(query_id=5508)

# fetch query result
data = dune.query_result(result_id)
```

