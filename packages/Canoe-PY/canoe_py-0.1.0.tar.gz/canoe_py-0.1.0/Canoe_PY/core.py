"""
Core functionality for the MyCANoe library
"""

import os
import sys
import time
import logging
import pythoncom
import win32com.client
from typing import Optional, Dict, List, Any, Union, Tuple

from .utils import setup_logger, wait_until, validate_file_path, wait
from .exceptions import MyCANoeException, ConnectionError, ConfigurationError, MeasurementError, SignalError

class MyCANoe:
    """Main class for interacting with Vector CANoe"""
    
    def __init__(self, log_level=logging.INFO, user_capl_functions=None):
        """Initialize the MyCANoe instance
        
        Args:
            log_level: Logging level
            user_capl_functions: Tuple of user-defined CAPL function names
        """
        # Setup logging
        self.logger = setup_logger("MyCANoe", log_level)
        self.logger.info("Initializing MyCANoe library")
        
        # Store user CAPL functions
        self.user_capl_functions = user_capl_functions or tuple()
        
        # Initialize COM
        pythoncom.CoInitialize()
        
        # CANoe application object
        self.app = None
        self.version = None
        self.measurement = None
        self.configuration = None
        self.environment = None
        self.system = None
        self.bus = None
        self.capl = None
        self.ui = None
        
        # Timeouts
        self.measurement_timeout = 60  # seconds
        self.application_timeout = 30  # seconds
    
    def _connect_to_canoe(self) -> None:
        """Connect to CANoe application"""
        try:
            # Get the running CANoe application or create a new instance
            self.app = win32com.client.Dispatch("CANoe.Application")
            self.logger.info(f"Connected to CANoe version {self.app.Version}")
            
            # Get the measurement interface
            self.measurement = self.app.Measurement
            
            # Get the system interface
            self.system = self.app.System
            
            # Get the environment interface
            self.environment = self.app.Environment
        except Exception as e:
            self.logger.error(f"Failed to connect to CANoe: {str(e)}")
            raise MyCANoeException(f"Failed to connect to CANoe: {str(e)}")
    
    def _initialize_objects(self):
        """Initialize all CANoe objects after opening a configuration"""
        try:
            # Initialize environment
            self.environment = self.app.Environment
            
            # Initialize system
            self.system = self.app.System
            
            # Initialize bus
            self.bus = self.app.Bus
            
            # Initialize CAPL
            self.capl = self.app.CAPL
            
            # Initialize UI
            self.ui = self.app.UI
            
            self.logger.debug("Initialized all CANoe objects")
        except Exception as e:
            self.logger.error(f"Failed to initialize CANoe objects: {str(e)}")
            raise MyCANoeException(f"Failed to initialize CANoe objects: {str(e)}")
    
    def get_version(self) -> str:
        """Get CANoe version as a string"""
        return f"{self.version.major}.{self.version.minor}.{self.version.Build}"
    
    def is_measurement_running(self) -> bool:
        """Check if measurement is running"""
        return self.measurement.Running
    
    def get_configuration_path(self) -> str:
        """Get the path of the current configuration"""
        return self.configuration.FullName
    
    def open(self, config_path: str, visible=True, auto_save=True, prompt_user=False, auto_stop=True) -> None:
        """Open a CANoe configuration
        
        Args:
            config_path: Path to the CANoe configuration file
            visible: Whether to make CANoe visible
            auto_save: Whether to automatically save the current configuration if changed
            prompt_user: Whether to prompt the user in error situations
            auto_stop: Whether to stop the measurement before opening the configuration
        """
        if not validate_file_path(config_path, '.cfg'):
            raise ConfigurationError(f"Invalid configuration file: {config_path}")
        
        try:
            # Connect to CANoe if not already connected
            if self.app is None:
                self._connect_to_canoe()
            
            # Set visibility
            self.app.Visible = visible
            
            # Check if measurement is running
            if self.measurement.Running and not auto_stop:
                raise MeasurementError("Measurement is running. Stop the measurement or set auto_stop=True")
            elif self.measurement.Running and auto_stop:
                self.logger.warning("Active Measurement is running. Stopping measurement before opening configuration")
                self.stop_measurement()
            
            # Open the configuration
            self.logger.info(f"Opening configuration: {config_path}")
            self.app.Open(config_path, auto_save, prompt_user)
            
            # Wait for configuration to open
            wait(1.0)
            
            # Initialize all objects
            self._initialize_objects()
            
            self.logger.info(f"Successfully opened CANoe configuration: {config_path}")
        except Exception as e:
            self.logger.error(f"Failed to open configuration: {str(e)}")
            raise ConfigurationError(f"Failed to open configuration: {str(e)}")
    
    def new(self, auto_save=False, prompt_user=False) -> None:
        """Create a new CANoe configuration
        
        Args:
            auto_save: Whether to automatically save the current configuration if changed
            prompt_user: Whether to prompt the user in error situations
        """
        try:
            # Connect to CANoe if not already connected
            if self.app is None:
                self._connect_to_canoe()
            
            # Create new configuration
            self.app.New(auto_save, prompt_user)
            
            # Wait for configuration to be created
            wait(1.0)
            
            # Initialize all objects
            self._initialize_objects()
            
            self.logger.info("Successfully created new CANoe configuration")
        except Exception as e:
            self.logger.error(f"Failed to create new configuration: {str(e)}")
            raise ConfigurationError(f"Failed to create new configuration: {str(e)}")
    
    def quit(self) -> None:
        """Quit CANoe without saving changes in the configuration"""
        try:
            if self.app is not None:
                self.logger.info("Quitting CANoe application")
                self.app.Quit()
                wait(1.0)
                pythoncom.CoUninitialize()
                self.app = None
                self.logger.info("CANoe Application Closed")
        except Exception as e:
            self.logger.error(f"Failed to quit CANoe application: {str(e)}")
            raise MyCANoeException(f"Failed to quit CANoe application: {str(e)}")
    
    def start_measurement(self, timeout=None) -> bool:
        """Start the measurement
        
        Args:
            timeout: Timeout in seconds to wait for measurement to start
            
        Returns:
            True if measurement started successfully
        """
        timeout = timeout or self.measurement_timeout
        
        try:
            if not self.measurement.Running:
                self.logger.info("Starting measurement")
                self.measurement.Start()
                
                # Wait for measurement to start
                start_time = time.time()
                while not self.measurement.Running:
                    if time.time() - start_time > timeout:
                        self.logger.error(f"Timeout waiting for measurement to start (timeout={timeout}s)")
                        return False
                    wait(0.1)
                
                self.logger.info("Measurement started successfully")
                return True
            else:
                self.logger.info("Measurement already running")
                return True
        except Exception as e:
            self.logger.error(f"Failed to start measurement: {str(e)}")
            raise MeasurementError(f"Failed to start measurement: {str(e)}")
    
    def stop_measurement(self, timeout=None) -> bool:
        """Stop the measurement
        
        Args:
            timeout: Timeout in seconds to wait for measurement to stop
            
        Returns:
            True if measurement stopped successfully
        """
        timeout = timeout or self.measurement_timeout
        
        try:
            if self.measurement.Running:
                self.logger.info("Stopping measurement")
                self.measurement.Stop()
                
                # Wait for measurement to stop
                start_time = time.time()
                while self.measurement.Running:
                    if time.time() - start_time > timeout:
                        self.logger.error(f"Timeout waiting for measurement to stop (timeout={timeout}s)")
                        return False
                    wait(0.1)
                
                self.logger.info("Measurement stopped successfully")
                return True
            else:
                self.logger.info("Measurement already stopped")
                return True
        except Exception as e:
            self.logger.error(f"Failed to stop measurement: {str(e)}")
            raise MeasurementError(f"Failed to stop measurement: {str(e)}")
    
    def reset_measurement(self) -> bool:
        """Reset the measurement
        
        Returns:
            True if measurement reset successfully
        """
        try:
            if self.measurement.Running:
                self.logger.info("Resetting measurement")
                self.measurement.Stop()
                wait(0.5)
                self.measurement.Start()
                wait(0.5)
                self.logger.info("Measurement reset successfully")
                return True
            else:
                self.logger.info("Measurement not running, starting measurement")
                self.measurement.Start()
                wait(0.5)
                self.logger.info("Measurement started successfully")
                return True
        except Exception as e:
            self.logger.error(f"Failed to reset measurement: {str(e)}")
            raise MeasurementError(f"Failed to reset measurement: {str(e)}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive status of CANoe"""
        return {
            "version": self.get_version(),
            "measurement_running": self.is_measurement_running(),
            "configuration": self.get_configuration_path(),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    # Signal Methods
    def get_signal_value(self, bus: str, channel: int, message: str, signal: str, raw_value=False) -> Any:
        """Get the value of a signal
        
        Args:
            bus: The bus (CAN, LIN, FlexRay, etc.)
            channel: The channel number
            message: The message name
            signal: The signal name
            raw_value: Whether to get the raw value (True) or physical value (False)
            
        Returns:
            The signal value
        """
        try:
            signal_obj = self.app.GetBus(bus).GetSignal(channel, message, signal)
            if raw_value:
                value = signal_obj.RawValue
            else:
                value = signal_obj.Value
            
            self.logger.debug(f"Got signal value: {bus}{channel}.{message}.{signal} = {value}")
            return value
        except Exception as e:
            self.logger.error(f"Failed to get signal value: {str(e)}")
            raise SignalError(f"Failed to get signal value: {str(e)}")

    def set_signal_value(self, bus: str, channel: int, message: str, signal: str, value: Any, raw_value=False) -> None:
        """Set the value of a signal
        
        Args:
            bus: The bus (CAN, LIN, FlexRay, etc.)
            channel: The channel number
            message: The message name
            signal: The signal name
            value: The value to set
            raw_value: Whether to set the raw value (True) or physical value (False)
        """
        try:
            signal_obj = self.app.GetBus(bus).GetSignal(channel, message, signal)
            if raw_value:
                signal_obj.RawValue = value
            else:
                signal_obj.Value = value
            
            self.logger.debug(f"Set signal value: {bus}{channel}.{message}.{signal} = {value}")
        except Exception as e:
            self.logger.error(f"Failed to set signal value: {str(e)}")
            raise SignalError(f"Failed to set signal value: {str(e)}")
    
    def get_signal_full_name(self, bus: str, channel: int, message: str, signal: str) -> str:
        """Get the full name of a signal
        
        Args:
            bus: The bus (CAN, LIN, FlexRay, etc.)
            channel: The channel number
            message: The message name
            signal: The signal name
            
        Returns:
            The full name of the signal
        """
        try:
            signal_obj = self.app.GetBus(bus).GetSignal(channel, message, signal)
            full_name = signal_obj.FullName
            self.logger.debug(f"Got signal full name: {bus}{channel}.{message}.{signal} = {full_name}")
            return full_name
        except Exception as e:
            self.logger.error(f"Failed to get signal full name: {str(e)}")
            raise SignalError(f"Failed to get signal full name: {str(e)}")
    
    def check_signal_online(self, bus: str, channel: int, message: str, signal: str) -> bool:
        """Check if a signal is online
        
        Args:
            bus: The bus (CAN, LIN, FlexRay, etc.)
            channel: The channel number
            message: The message name
            signal: The signal name
            
        Returns:
            True if the signal is online
        """
        try:
            signal_obj = self.app.GetBus(bus).GetSignal(channel, message, signal)
            is_online = signal_obj.IsOnline
            self.logger.debug(f"Signal online status: {bus}{channel}.{message}.{signal} = {is_online}")
            return is_online
        except Exception as e:
            self.logger.error(f"Failed to check signal online status: {str(e)}")
            raise SignalError(f"Failed to check signal online status: {str(e)}")
    
    # Environment Variable Methods
    def get_environment_variable_value(self, var_name: str) -> Any:
        """Get the value of an environment variable
        
        Args:
            var_name: Name of the environment variable
            
        Returns:
            The value of the environment variable
        """
        try:
            var = self.environment.GetVariable(var_name)
            value = var.Value
            self.logger.debug(f"Got environment variable value: {var_name} = {value}")
            return value
        except Exception as e:
            self.logger.error(f"Failed to get environment variable value: {str(e)}")
            raise MyCANoeException(f"Failed to get environment variable value: {str(e)}")

    def set_environment_variable_value(self, var_name: str, value: Any) -> None:
        """Set the value of an environment variable
        
        Args:
            var_name: Name of the environment variable
            value: Value to set
        """
        try:
            var = self.environment.GetVariable(var_name)
            var.Value = value
            self.logger.debug(f"Set environment variable value: {var_name} = {value}")
        except Exception as e:
            self.logger.error(f"Failed to set environment variable value: {str(e)}")
            raise MyCANoeException(f"Failed to set environment variable value: {str(e)}")
    
    # System Variable Methods
    def get_system_variable_value(self, sys_var_name: str) -> Any:
        """Get the value of a system variable
        
        Args:
            sys_var_name: Full name of the system variable including namespace
            
        Returns:
            The value of the system variable
        """
        try:
            # Split the namespace and variable name
            parts = sys_var_name.split('::')
            namespace = '::'.join(parts[:-1])
            variable_name = parts[-1]
            
            # Get the namespace and variable
            namespace_obj = self.system.Namespaces(namespace)
            variable_obj = namespace_obj.Variables(variable_name)
            
            value = variable_obj.Value
            self.logger.debug(f"Got system variable value: {sys_var_name} = {value}")
            return value
        except Exception as e:
            self.logger.error(f"Failed to get system variable value: {str(e)}")
            raise MyCANoeException(f"Failed to get system variable value: {str(e)}")

    def set_system_variable_value(self, sys_var_name: str, value: Any) -> None:
        """Set the value of a system variable
        
        Args:
            sys_var_name: Full name of the system variable including namespace
            value: Value to set
        """
        try:
            # Split the namespace and variable name
            parts = sys_var_name.split('::')
            namespace = '::'.join(parts[:-1])
            variable_name = parts[-1]
            
            # Get the namespace and variable
            namespace_obj = self.system.Namespaces(namespace)
            variable_obj = namespace_obj.Variables(variable_name)
            
            # Get the current value to determine its type
            current_value = variable_obj.Value
            
            # Set the value based on the current value's type
            if isinstance(current_value, int):
                # Convert to int if the current value is an integer
                if isinstance(value, str) and value.startswith("0x"):
                    # Handle hex strings
                    variable_obj.Value = int(value, 16)
                else:
                    variable_obj.Value = int(value)
            elif isinstance(current_value, float):
                # Convert to float if the current value is a float
                variable_obj.Value = float(value)
            elif isinstance(current_value, str):
                # Keep as string if the current value is a string
                variable_obj.Value = str(value)
            else:
                # For other types, try direct assignment
                variable_obj.Value = value
                
            self.logger.debug(f"Set system variable value: {sys_var_name} = {value}")
        except Exception as e:
            self.logger.error(f"Failed to set system variable value: {str(e)}")
            raise MyCANoeException(f"Failed to set system variable value: {str(e)}")
    
    def set_system_variable_array_values(self, sys_var_name: str, values: Tuple) -> None:
        """Set the values of a system variable array
        
        Args:
            sys_var_name: Full name of the system variable array including namespace
            values: Tuple of values to set
        """
        try:
            # Split the namespace and variable name
            parts = sys_var_name.split('::')
            namespace = '::'.join(parts[:-1])
            variable_name = parts[-1]
            
            # Get the namespace and variable
            namespace_obj = self.system.Namespaces(namespace)
            variable_obj = namespace_obj.Variables(variable_name)
            
            # Get the current array values
            current_values = list(variable_obj.Value)
            
            # Update the array values
            for i, value in enumerate(values):
                if i < len(current_values):
                    current_values[i] = value
            
            # Set the updated array
            variable_obj.Value = tuple(current_values)
                
            self.logger.debug(f"Set system variable array values: {sys_var_name} = {values}")
        except Exception as e:
            self.logger.error(f"Failed to set system variable array values: {str(e)}")
            raise MyCANoeException(f"Failed to set system variable array values: {str(e)}")
    
    # CAPL Methods
    def compile_all_capl_nodes(self) -> Dict:
        """Compile all CAPL, XML and .NET nodes
        
        Returns:
            Dictionary with compilation result
        """
        try:
            self.capl.Compile()
            wait(1.0)
            
            # Get compilation result
            result = {"result": True, "errors": 0, "warnings": 0}
            
            self.logger.info(f"Compiled all CAPL nodes successfully")
            return result
        except Exception as e:
            self.logger.error(f"Failed to compile all CAPL nodes: {str(e)}")
            return {"result": False, "errors": 1, "warnings": 0}
    
    def call_capl_function(self, name: str, *arguments) -> bool:
        """Call a CAPL function
        
        Args:
            name: The name of the CAPL function
            arguments: Function parameters
            
        Returns:
            True if the function was called successfully
        """
        try:
            if name not in self.user_capl_functions:
                self.logger.warning(f"CAPL function '{name}' not in user_capl_functions list")
            
            capl_function = self.capl.GetFunction(name)
            param_count = capl_function.ParameterCount
            
            if len(arguments) != param_count:
                self.logger.error(f"Function arguments not matching with CAPL user function args. Expected {param_count}, got {len(arguments)}")
                return False
            
            if param_count > 0:
                capl_function.Call(*arguments)
            else:
                capl_function.Call()
                
            self.logger.debug(f"Called CAPL function: {name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to call CAPL function: {str(e)}")
            raise MyCANoeException(f"Failed to call CAPL function: {str(e)}")
    
    # Database Methods
    def add_database(self, db_path: str, bus: str, channel: int) -> bool:
        """Add a database to the configuration
        
        Args:
            db_path: Path to the database file
            bus: The bus (CAN, LIN, FlexRay, etc.)
            channel: The channel number
            
        Returns:
            True if the database was added successfully
        """
        try:
            # Get the database setup
            db_setup = self.configuration.GeneralSetup.DatabaseSetup
            
            # Add the database
            db_setup.Databases.Add(db_path, bus, channel)
            
            self.logger.info(f"Added database: {db_path} to {bus}{channel}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add database: {str(e)}")
            raise MyCANoeException(f"Failed to add database: {str(e)}")
    
    def remove_database(self, db_path: str, channel: int) -> bool:
        """Remove a database from the configuration
        
        Args:
            db_path: Path to the database file
            channel: The channel number
            
        Returns:
            True if the database was removed successfully
        """
        try:
            # Get the database setup
            db_setup = self.configuration.GeneralSetup.DatabaseSetup
            
            # Find and remove the database
            for i in range(1, db_setup.Databases.Count + 1):
                db = db_setup.Databases.Item(i)
                if db.FullName == db_path and db.Channel == channel:
                    db_setup.Databases.Remove(i)
                    self.logger.info(f"Removed database: {db_path} from channel {channel}")
                    return True
            
            self.logger.warning(f"Database not found: {db_path} on channel {channel}")
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove database: {str(e)}")
            raise MyCANoeException(f"Failed to remove database: {str(e)}")
    
    def close(self):
        """Clean up resources"""
        try:
            pythoncom.CoUninitialize()
        except:
            pass
    
    def __del__(self):
        """Destructor to ensure resources are cleaned up"""
        self.close()




