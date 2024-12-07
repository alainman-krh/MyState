[VSPLG_SERMON]: <https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-serial-monitor>
## `1-PkgUpload`
<!----------------------------------------------------------------------------->
Helper utilities to upload a given demo/package to CircuitPython-enabled boards.

# Available utilities
<!----------------------------------------------------------------------------->
`pkg_upload.py`: The upload script itself.
- Alternative to using recommended IDE/flow.
- User configurable.
- Works well launched from VSCode.

# How to monitor serial output of Circuit Python device
<!----------------------------------------------------------------------------->
Here are a few suggestions for serial monitors on different platforms:

- Linux:
  - "screen": `screen /dev/path/to/device` (must install)

- Windows:
  - VSCode: [Serial Monitor plugin (by Microsoft)][VSPLG_SERMON]<br>
    Suggest: Line ending = CR / "terminal mode"
  - putty (must install)<br>
    WARN: Security issue found on some versions in 2024.
