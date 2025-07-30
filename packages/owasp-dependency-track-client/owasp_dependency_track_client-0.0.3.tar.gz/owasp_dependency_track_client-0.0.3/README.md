# OWASP Dependency Track Python API client

## Usage

```shell
pip install owasp-dependency-track-client
```

Create the client
```python
from owasp_dt import Client

client = Client(
    base_url="http://localhost:8081/api",
    headers={
        "X-Api-Key": "YOUR API KEY"
    },
    verify_ssl=True,
    raise_on_unexpected_status=True,
)
```

Call endpoints:
```python
from owasp_dt.api.project import get_projects

projects = get_projects.sync(client=client)
assert len(projects) > 0
```

## CLI

If you're looking for a CLI tool, visit: https://github.com/mreiche/owasp-dependency-track-cli
