# Archives of the python docs

For the purpose of figuring out what worked, when. Inspired by `caniuse` and the Mozilla Developer Network's browser compatibility efforts.

# The project

```yaml
repo_root:
  - archive: # ~94M, all told
      - LICENSE # licence governing python and its docs since 1.0
      - ${version}.zip # the .zip for that version
  - scripts:
      - download-all.py # downloads the zips
  - LICENSE # the license governing the scraper project
```

## legal

**All documentation is licensed under as described in [./archive/LICENSE](./archive/LICENSE).**

The code to scrape the documentation is licensed under [./LICENSE](./LICENSE).
