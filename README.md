# Archives of the python docs

For the purpose of figuring out what worked, when. Inspired by `caniuse` and the Mozilla Developer Network's browser compatibility efforts.

# The project

```yaml
repo_root:
  archive:
    - LICENSE # licence governing python since 1.0
    - $version: # the archive files for that version
        rst: ...
        html: ...
  scrapers:
    - $version: ... # something to download, extract the RST, HTML docs
  scripts: ...
```

## legal

All documentation is licensed under as described in [./archive/LICENSE](./archive/LICENSE).

The code to assemble the documentation is licensed under [./LICENSE](./LICENSE)
