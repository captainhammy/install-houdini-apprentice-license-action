# Install Apprentice Licenses

This Github Action will install Apprentice (non-commercial) Houdini related licenses.

## Usage

```yaml
  - name: Install Apprentice Licenses
    uses: captainhammy/install-houdini-apprentice-license-action@v2
    with:
      client_id: ${{ secrets.SESI_CLIENT_ID }}
      client_secret_key:  ${{ secrets.SESI_SECRET_KEY }}
      houdini_version: 19.5
```

### Inputs

This action uses the [SideFX Web API](https://www.sidefx.com/docs/api/) to redeem the necessary licenses.

You must provide:
- [Client id and Client secret](https://www.sidefx.com/docs/api/credentials/index.html) values.
- The Houdini **{major.minor}** version to redeem a license for.

If any of the values are not defined then the action will fail.

## Available License Types

The following non-commercial license types will be available:
- Houdini FX
- Mantra
- Karma

## Dependencies

This action is self-contained and will ensure that all it's dependencies (Python 3.9 + requests module) are installed.
