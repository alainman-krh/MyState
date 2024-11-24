# MyState: Be one with the electronics universe 🧘‍♀️Ω🧘‍♂️. Collaborate. Interoperate.
<!----------------------------------------------------------------------------->
Framework to simplify configuration and control of appliance-like devices.
Quickly build up device state, and have it automatically accessible from the outside world.

✨Hilights:
- Call `SigLink.process_signals()` to enable easy device control via serial/IO connection.

## Features
- Route raw sensed input signals through custom signal-generating filters, and
  provide a solid, uniform user-interface experience.
- Load/save configuration/controlled state from a single function call.
- Let anyone control your device using `SigLink` interface (by means of a
  serial/other IO connection).
  - Ex: Let a PC control your device using signals sent from Python across its USB/serial connection.
- Aspires to enable a future of composable, modular devices where
  extension/customization is the norm. Getting our products to cooperate should
  not be a constant battle requiring mounds of ugly hacks.

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