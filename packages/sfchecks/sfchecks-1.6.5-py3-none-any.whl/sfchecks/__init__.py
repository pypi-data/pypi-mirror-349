"""
A library for writing `flag.py` checks.

Of interest to developers are probably:
    - `sfchecks.types`
    - `sfchecks.utils`
    - `sfchecks.tools`



## Writing checks using sfchecks

Write your checks in `fs/SF/conf/flag.py` (instead of flag.yml).

Minimally, your script must contain a method called `check()` that returns a string
describing the check status, e.g. `fixed`, `vulnerable`, or `broken-functionality`.

It is highly recommended to use the `sfchecks.utils.check` decorator to avoid issues
with `sf-rebuild-and-test`.

```python
import sfchecks.utils

@sfchecks.utils.check
def check():
    return 'fixed'
```

To replicate the YAML style checks, there are a number of helper methods. See the example below.

To store shared methods and such, add a Python script to `/SF/conf/templates.d`, and import them with
`sfchecks.utils.import_from_templates`.

### Example

```python
import logging
import sfchecks.utils
from sfchecks.utils import check_for
from sfchecks.types import CheckResult
import requests

@sfchecks.utils.check
def check() -> CheckResult | None:
    return sfchecks.utils.run_checks([
        check_for('broken-webserver', website_is_down),
        check_for('broken-functionality', login_broken),
        check_for('vulnerable', vulnerable),
        check_for('fixed', fixed),
    ])

def user_login(password="password") -> requests.Response:
    return requests.post(
        "http://vulnerableapp.com:3000/api/users/login",
        json={"user": {"email": "user@vulnerableapp.com", "password": password}}
    )

def website_is_down() -> bool:
    r = requests.get("http://vulnerableapp.com")
    return r.status_code != 200

def login_broken() -> bool:
    return user_login().status_code != 200

def vulnerable() -> bool:
    logging.info("This will always print")
    logging.debug("This will only print in debug mode or if the DEBUG environment variable is set")
    return user_login(password="', 'saltsalt') OR '1' LIMIT 1;-- ").status_code == 200

def fixed() -> bool:
    return user_login().status_code == 200

if __name__ == "__main__":
    check()
```

![image](../../docs/yaml.png)

*<3 checks.yml*
"""
