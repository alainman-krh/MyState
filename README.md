# MyState
Framework to simplify configuration and control of appliance-like devices.

✨Hilights:
- Call `SigLink.process_signals()` to enable easy device control via serial/IO connection.

## Features
- Route raw hardware signals through ready-built filters that provide a solid human-interface experience.
- Load load/save config/controlled state from a single function call.
- Let anyone control your device using `SigLink` interface though a serial/IO connection.

# Details
- Framework provides access to device state using something the author calls a
  "Model-React-Controller" (MRC) analogous to a Model-View-Controller.
  - "React" is used instead of "View" since uC devices more generally described
    as reacting to changes in the model/state data.

# Comments
- Libraries designed to handle user input that might get corrupted (ex: debounce signals).
- Will not to raise exceptions, but will instead ignore signals/move on when they cannot be processed.