# React Native Debugger Client

A Python client for interacting with React Native applications via the Hermes debugger.

## Features

- Connect to a React Native app's Hermes debugger
- Execute JavaScript code in the React Native context
- Interact with UI elements (tap, scroll, enter text)
- Get the React component tree
- Navigate between screens
- Debug utilities (toggle debug features, performance overlay)
- Widget finder utilities

## Installation

```bash
pip install react-native-debugger-client
```

## Usage

### Basic Usage

```python
from react_native_debugger_client import ReactNativeDebuggerClient

# Connect to a React Native app running on your device or emulator
client = ReactNativeDebuggerClient(device_ip="localhost", metro_port=8081)
success, message = client.connect()

if success:
    # Get the UI tree
    ui_tree = client.get_ui_tree()
    
    # Tap a button
    client.tap_element(test_id="submit_button")
    
    # Enter text in an input field
    client.enter_text(test_id="email_input", text="user@example.com")
    
    # Scroll down
    client.scroll("down")
    
    # Navigate to a screen
    client.navigate_to_screen("HomeScreen")
    
    # Execute custom JavaScript
    client.execute_js("console.log('Hello from Python!');")
    
    # Close the connection when done
    client.close()
```

### Context Manager

You can also use the client as a context manager:

```python
with ReactNativeDebuggerClient() as client:
    success, message = client.connect()
    if success:
        client.tap_element(text="Login")
```

## API Reference

### Connection

- `__init__(device_ip="localhost", metro_port=8081)` - Initialize the client
- `connect(timeout=10)` - Connect to the React Native app's Hermes debugger
- `close()` - Close the connection

### UI Interaction

- `tap_element(test_id=None, text=None, timeout=5)` - Tap an element by test ID or text content
- `enter_text(test_id, text, timeout=5)` - Enter text into a TextInput element
- `scroll(direction="down", distance=300, timeout=5)` - Scroll the screen
- `scroll_element(test_id=None, direction="down", distance=300, timeout=5)` - Scroll a specific element

### Navigation

- `get_current_screen(timeout=5)` - Get the name of the current screen
- `navigate_to_screen(screen_name, params=None, timeout=5)` - Navigate to a specific screen

### Widget Utilities

- `find_widgets(search_by="all", search_value="", timeout=5)` - Find widgets matching criteria
- `tap_widget_by_key(key_value, timeout=5)` - Tap a widget by its key
- `tap_widget_by_text(text, timeout=5)` - Tap a widget by its text content
- `tap_widget_by_type(widget_type, timeout=5)` - Tap a widget by its type
- `tap_widget_by_tooltip(tooltip_text, timeout=5)` - Tap a widget by its tooltip text
- `enter_text_by_key(key_value, text, timeout=5)` - Enter text in a widget by its key
- `enter_text_by_type(widget_type, text, timeout=5)` - Enter text in a widget by its type
- `enter_text_by_text(widget_text, text, timeout=5)` - Enter text in a widget by its text content

### Debug Utilities

- `toggle_debug_paint_feature(enable=True, timeout=5)` - Toggle debug paint feature
- `toggle_performance_overlay(enable=True, timeout=5)` - Toggle performance overlay
- `toggle_repaint_rainbow(enable=True, timeout=5)` - Toggle repaint rainbow
- `toggle_debug_banner(enable=True, timeout=5)` - Toggle debug banner

## Requirements

- Python 3.7+
- requests>=2.28.0
- websocket-client>=1.3.0

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.