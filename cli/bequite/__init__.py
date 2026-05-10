"""BeQuite CLI package.

The CLI thin wrapper lands in v0.5.0 (pyproject.toml + __main__.py + commands.py
+ skill_loader.py + config.py + hooks.py). This v0.4.2 release ships only the
audit module; v0.4.3 ships the freshness module. They're importable as
standalone Python modules pre-CLI:

    python -m cli.bequite.audit --help
    python -m cli.bequite.freshness --help

Once v0.5.0 ships, both are wired under `bequite audit` / `bequite freshness`.
"""

__version__ = "0.17.0"
