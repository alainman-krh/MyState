## `1-PkgUpload`
<!----------------------------------------------------------------------------->
Helper utilities to upload a given demo/package to CircuitPython-enabled boards.

# Available utilities
<!----------------------------------------------------------------------------->
`pkg_upload.py`:
- The upload utilities themselves
- Alternative to using recommended IDE/flow.
- Works well launched from VSCode.

# How to monitor serial output
<!----------------------------------------------------------------------------->
Here are a few suggestions for serial monitors on different platforms:

- Linux:
  - "screen": `screen /dev/path/to/device` (must install)

- Windows:
  - VSCode: Serial Monitor plugin (by Microsoft)<br>
    Suggest: Line ending = CR / "terminal mode"
  - putty (must install)<br>
    WARN: Security issue found on some versions in 2024.
