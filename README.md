# MyState
Framework to simplify configuration and control of appliance-like devices.
Turn on IOLink to make your device controllable from a serial/IO connection.

## Features
- Route raw hardware signals through ready-built filters that provide a solid human-interface experience.
- Load load/save config/controlled state from a single function call.
- Let anyone control your device by linking state to a serial/IO connection.

# Details
- Framework provides access to device state using something the author calls a
  "Model-React-Controller" (MRC) analogous to a Model-View-Controller.
- "React" is used instead of "View" since uC devices more generally described
  as reacting to changes in the model/state data.

# Comments
- Libraries meant to handle user input that might get corrupted.
- Will not typically raise exceptions. Will just ignore what can't be processed.