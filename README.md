# MyState: Be one with the electronics universe 🧘‍♀️Ω🧘‍♂️. Collaborate. Interoperate.
<!----------------------------------------------------------------------------->
Framework to simplify configuration and control of appliance-like devices.
`MyState` makes it quick-and-easy to define device state that is readily
controllable from the outside world.

Writing code to control state and react to sensor inputs is time consuming.
Why not (mostly) solve the problem once, and re-use that infrastructure to build
up your next project faster?

## Features
- Route raw sensed input signals through custom signal-generating filters, and
  provide a solid, uniform user-interface experience.
- Load custom device configuration/controlled state on startup by calling `ListenerRoot.script_load()`.
  - A good way to "recall presets" at the press of a button when manual configuration is a bit of a pain.
- Let anyone control your device using `SigLink` interface (by means of a
  serial/other IO connection).
  - Ex: Let a PC control your device using MyState "signals" sent across the USB/serial connection.
  - Configure your device using a custom-built GUI or web interface.
- Applies more formalized (hopefully readable) patterns of "filtering"
  input/sense signals, and applying a "reactive paradigm" to respond accordingly.
- Aspires to enable a future of composable, modular devices where
  extension/customization is the norm. Getting our products to cooperate should
  not be a constant battle requiring mounds of ugly hacks.

## ✨Hilights:
- Call `SigLink.process_signals()` to enable quick-and-easy device control via
  serial/IO connection.


# Details
<!----------------------------------------------------------------------------->
The framework provides access to device state using something the author calls a
"Model-React-Controller" (MRC) -- analogous to a Model-View-Controller.
- NOTE: "React" is used instead of "View" since uC devices more generally
  described as reacting to changes in the model/state data.


# Comments
<!----------------------------------------------------------------------------->
- Libraries designed to handle user input that might get corrupted (ex: debounce signals).
- Code should not raise exceptions, but instead ignore signals/move on when signals cannot be processed.