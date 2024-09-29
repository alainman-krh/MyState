## `devutils`: Utilities to help with development.
<!----------------------------------------------------------------------------->

# Serial Monitors
<!----------------------------------------------------------------------------->
Linux:
- "screen": `screen /dev/path/to/device` (must install)
Windows:
- VSCode: Serial Monitor plugin (by Microsoft)
  Suggest: Line ending = CR / "terminal mode"
- putty (must install). WARN: Security issue found on some versions in 2024.

# Available utilities
<!----------------------------------------------------------------------------->
`upload.py`:
- Simple utility to upload a given project/demo to the CircuitPython-enabled board.
- Avoids needing to use recommended IDE/flow.
- Works well launched from VSCode.

