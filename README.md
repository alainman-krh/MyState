# MyState: Be one with the electronics universe 🧘‍♀️Ω🧘‍♂️. Collaborate. Interoperate.
<!----------------------------------------------------------------------------->
Framework to simplify configuration and control of appliance-like devices.
Quickly build up device state, and have it automatically accessible from the outside world.

✨Hilights:
- Call `SigLink.process_signals()` to enable easy device control via serial/IO connection.

## Features
- Route raw input/sense signals through ready-built filters that provide a solid human-interface experience.
- Load/save configuration/controlled state from a single function call.
- Let anyone control your device using `SigLink` interface (by means of a serial/other IO connection).
- Aspires to a more composable design space where interfaces are built with extension/
  customization in mind. External devices shouldn't need hacks to work with your designs.

# Details
<!----------------------------------------------------------------------------->
- Framework provides access to device state using something the author calls a
  "Model-React-Controller" (MRC) -- analogous to a Model-View-Controller.
  - NOTE: "React" is used instead of "View" since uC devices more generally
    described as reacting to changes in the model/state data.

# Comments
<!----------------------------------------------------------------------------->
- Libraries designed to handle user input that might get corrupted (ex: debounce signals).
- Code should not raise exceptions, but instead ignore signals/move on when signals cannot be processed.