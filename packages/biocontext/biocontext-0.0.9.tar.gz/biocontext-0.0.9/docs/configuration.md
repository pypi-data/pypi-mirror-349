# Configuration

## OpenAPI Server Configuration

Create a `config.yaml` file in the `biocontext/config` directory:

```yaml
schemas:
  - name: example-server
    url: https://api.example.com/openapi.json
    type: json
    base: https://api.example.com
```

## Development Setup

We use `uv` for dependency management and versioning. The script `bump.sh` is
used to bump the version and create a git tag, which then can be used to create
a release on GitHub that triggers publication to PyPI. It can be used with
semantic versioning by passing the bump type as an argument, e.g. `./bump.sh
patch`.

Adherence to best practices is ensured by a pre-commit hook that runs `ruff`,
`mypy`, and `deptry`. To check the code base at any time, run `make check` from
the terminal.

Docs are built using `mkdocs` (the [Material
theme](https://squidfunk.github.io/mkdocs-material/)); you can preview the docs
by running `uv run mkdocs serve`.
