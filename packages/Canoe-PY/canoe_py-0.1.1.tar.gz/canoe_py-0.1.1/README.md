# Canoe_PY

A custom Python library for interacting with Vector CANoe.

## Installation

```bash
pip install Canoe_PY
```

## Features

- Connect to running CANoe instances
- Open and create CANoe configurations
- Start, stop, and reset measurements
- Get and set signal values
- Get and set system variables
- Get and set environment variables
- Compile and call CAPL functions
- Add and remove databases
- Comprehensive error handling and logging

## Usage

See the [examples](examples/) directory for detailed usage examples.

### Basic Usage

```python
from Canoe_PY import MyCANoe

# Create instance
canoe = MyCANoe()

# Connect to CANoe
canoe._connect_to_canoe()

# Open configuration
canoe.open_configuration("path/to/config.cfg")

# Start measurement
canoe.start_measurement()

# Work with system variables
canoe.set_system_variable_value("sys_var_demo::speed", 50)

# Stop measurement
canoe.stop_measurement()

# Quit CANoe
canoe.quit()
```

## Requirements

- Python 3.6 or higher
- pywin32
- Vector CANoe installed


## License

MIT



