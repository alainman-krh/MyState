# Naming convention (try to build one)
`filter_someinput()` #Reads state of sensor, and triggers `process_signal(associated_signal)`

```python
def filter_sense(sensedata)
    "Triggers handler for detected event"
    pass

def process_inputs()
    "Reads sense inputs and calls filter_sense()"
    for sensein in sensor_list:
        sensedata = sensein.read()
        sensein.filter_sense(sensedata)
```

On a button, `sensein.read()` => `button.isactive()`
NOTE: On a physically latching button, the state machine might only debounce (if even that's required).
On a rotary encoder, `sensein.read()` => `encoder.read_delta()`

Possible events triggered by `filter_sense()`:
    `press_sensed`, `press_detected`

Other potential names to use:
- `MyStateMRC` (Model-React-Controller)
- `EasySense`, `EasyCktIO`, `EasyDeviceIO`
- `SenseFilter`, `HwSignalFilter`


#TODO: `SigUpdate`:
- update ... 0: disable updates
- update ... 1: enable updates & update
