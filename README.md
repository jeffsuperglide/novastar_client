# Panama Canal Authority NovaStar API Client, novastar_client

## novastar_client

A Python client library for working with the NovaStar API, with documentation published via pdoc on GitHub pages.  See [Releases](https://github.com/jeffsuperglide/novastar_client/releases) and the latest release for this package details and install guidance.

## Overview

`novastar_client` is meant for developers who want to control or integrate NovaStar workflows from Python code instead of relying entirely on desktop tools.  The documentation site is structured as API reference material, so the package is best approached as importable library for scripts, services, and internal utilities.

## What it includes

- A Python package under the `novastar_client` name, documented with pdoc.
- An API-first layout intended for code-based usage.
- Published release artifacts for installation from GitHub release pages.

## Installation

Install from the repository's [Releases](https://github.com/jeffsuperglide/novastar_client/releases) using the package file provided on the GitHub release page.  Release assets include a tarball and wheel.  Download to install with pip, or install directly from the release version.  It is suggested to use the wheel for installation because it will be a quicker install.

### Option 1: PyPI (recommended)

This is the easiest and most reliable way to install \`novastar-client\`. It pulls the package straight from PyPI, resolves dependencies automatically, and works the same way on Windows, macOS, and Linux.

<!-- latest-release:pip:start -->
```bash
pip install novastar-client==1.2.3
```
<!-- /latest-release:pip:end -->

Or, to get the latest release without pinning a version:

```bash
pip install novastar-client
```

Using `uv`?

<!-- latest-release:uv:start -->
```bash
uv add novastar-client==1.2.3
```
<!-- /latest-release:uv:end -->

This release is published to PyPI via [Trusted Publishing](https://docs.pypi.org/trusted-publishers/), meaning it was built and signed directly by this repository's GitHub Actions workflow with no manually-handled credentials involved.

### Option 2: Install directly from this release

If you can't reach PyPI (e.g. an offline or restricted environment) or want the exact artifact attached to this GitHub release, install the wheel or source tarball directly:

<!-- latest-release:whl:start -->
```bash
pip install "https://github.com/jeffsuperglide/novastar_client/releases/download/v1.2.3/novastar_client-1.2.3-py3-none-any.whl"
```
<!-- /latest-release:whl:end -->

<!-- latest-release:dist:start -->
```bash
pip install "https://github.com/jeffsuperglide/novastar_client/releases/download/v1.2.3/novastar_client-1.2.3.tar.gz"
```
<!-- /latest-release:dist:end -->

<!-- latest-release:dl:start -->
Or download `novastar_client-1.2.3-py3-none-any.whl` / `novastar_client-1.2.3.tar.gz` from [Releases](https://github.com/jeffsuperglide/novastar_client/releases) and install from disk:
<!-- /latest-release:dl:end -->

<!-- latest-release:disk:start -->
```bash
pip install ./novastar_client-1.2.3-py3-none-any.whl
```
<!-- /latest-release:disk:end -->

### Option 3: Build from source

<!-- latest-release:clone:start -->
```bash
git clone https://github.com/jeffsuperglide/novastar_client.git
cd novastar_client
git checkout v1.2.3
pip install .
```
<!-- /latest-release:clone:end -->

## Documentation

The full API reference is published at [client docs](https://jeffsuperglide.github.io/novastar_client/).  Reference for:

- Module and class names.
- Method signatures.
- Parmeter details.
- Return values.

## Reference Links

[API-UI](https://panama-cloud-ns5.trilynx-novastar.systems/novastar/data/api/v1/api-ui)

[Operator Manual](https://panama-cloud-ns5.trilynx-novastar.systems/novastar/doc/operator/user/)

[Operator Map](https://panama-cloud-ns5.trilynx-novastar.systems/novastar/operator/map)

[Stations API Call - Simple](https://panama-cloud-ns5.trilynx-novastar.systems/novastar/data/api/v1/stations)

[TriLynx NovaStar Web Services Docs Home](https://software.trilynx.systems/nsdataws/latest/doc-user/).

[Jython.org](https://www.jython.org/)

[Python 2.7](https://docs.python.org/2.7/)
