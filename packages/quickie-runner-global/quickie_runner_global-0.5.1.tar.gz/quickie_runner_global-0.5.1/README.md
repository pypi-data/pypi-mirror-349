# Quickie Global

This package provides a separate binary `qkg` that allows you to run global quickie tasks from any directory, without conflicts with quickie tasks defined in your projects.

## Installing

It is recommended to use `pipx` to install in an isolated environment:

```sh
pipx install quickie-runner-global
qkg --help
```

If you have any issues with the `quickie` package missing when running `qkg`, you can inject it manually:

```sh
pipx inject quickie-runner-global quickie-runner
```
