"""
React Native Debugger module for interacting with React Native applications via the Hermes debugger.
"""

import requests
import json
import websocket
import threading
import time
import queue
import logging
from pathlib import Path

# Import JavaScript snippets
from .js_snippets import UI, Interaction
from .javascript_executor import JavaScriptExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ReactNativeDebuggerClient:
    """
    A client for interacting with React Native applications via the Hermes debugger.
    
    This class provides methods to connect to a React Native app's Hermes debugger,
    execute JavaScript code, and perform interactions like tapping elements and entering text.
    """
    
    def __init__(self, device_ip="localhost", metro_port=8081):
        """
        Initialize the ReactNativeDebuggerClient.
        
        Args:
            device_ip (str): The IP address of the device running the React Native app.
            metro_port (int): The port on which the Metro bundler is running.
        """
        self.device_ip = device_ip
        self.metro_port = metro_port
        self.ws = None
        self.connected = False
        self.message_queue = queue.Queue()
        self.next_message_id = 1
        self.pending_requests = {}
        self.ws_thread = None
        self._lock = threading.Lock()
    
    def connect(self, timeout=10):
        """
        Connect to the React Native app's Hermes debugger.
        
        Args:
            timeout (int): Timeout in seconds for the connection attempt.
            
        Returns:
            tuple: (success, message)
        """
        try:
            # Get the list of available targets
            logger.info(f"Connecting to Hermes debugger at {self.device_ip}:{self.metro_port}")
            response = requests.get(f"http://{self.device_ip}:{self.metro_port}/json", timeout=timeout)
            
            if response.status_code != 200:
                return False, f"Failed to get debugging targets: HTTP {response.status_code}"
            
            targets = json.loads(response.text)
            
            if not targets:
                return False, "No debugging targets found"
            
            # Connect to the first available target
            target = targets[0]
            ws_url = target.get('webSocketDebuggerUrl')
            
            if not ws_url:
                return False, "WebSocket URL not found in debugging target"
            
            logger.info(f"Connecting to WebSocket: {ws_url}")
            
            # Connect via WebSocket
            self.ws = websocket.WebSocketApp(
                ws_url,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close,
                on_open=self._on_open
            )
            
            # Start WebSocket connection in a separate thread
            self.ws_thread = threading.Thread(target=self.ws.run_forever, daemon=True)
            self.ws_thread.start()
            
            # Wait for connection to establish
            start_time = time.time()
            while not self.connected and time.time() - start_time < timeout:
                time.sleep(0.1)
            
            if not self.connected:
                return False, "Timed out waiting for WebSocket connection"
            
            logger.info("Connected to Hermes debugger successfully")
            return True, "Connected successfully"
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP request failed: {str(e)}", exc_info=True)
            return False, f"Failed to connect to Metro bundler: {str(e)}"
        except Exception as e:
            logger.error(f"Connection failed: {str(e)}", exc_info=True)
            return False, f"Connection failed: {str(e)}"
    
    def _on_open(self, ws):
        """
        Handle WebSocket connection open event.
        
        Args:
            ws: The WebSocket instance.
        """
        logger.info("WebSocket connection opened")
        self.connected = True
    
    def _on_message(self, ws, message):
        """
        Handle incoming messages from the WebSocket.
        
        Args:
            ws: The WebSocket instance.
            message (str): The message received from the WebSocket.
        """
        try:
            data = json.loads(message)
            logger.debug(f"Received message: {data}")
            
            # Check if this is a response to a pending request
            if 'id' in data and data['id'] in self.pending_requests:
                with self._lock:
                    if data['id'] in self.pending_requests:
                        # Put the result in the corresponding future
                        self.pending_requests[data['id']].put(data)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse WebSocket message: {message}")
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
    
    def _on_error(self, ws, error):
        """
        Handle WebSocket errors.
        
        Args:
            ws: The WebSocket instance.
            error: The error that occurred.
        """
        logger.error(f"WebSocket error: {error}")
        self.connected = False
    
    def _on_close(self, ws, close_status_code, close_msg):
        """
        Handle WebSocket connection close.
        
        Args:
            ws: The WebSocket instance.
            close_status_code: The status code for the close event.
            close_msg: The close message.
        """
        logger.info(f"WebSocket closed: {close_status_code} - {close_msg}")
        self.connected = False
    
    def execute_js(self, code, timeout=5):
        """
        Execute JavaScript code in the React Native context.
        
        Args:
            code (str): The JavaScript code to execute.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, result)
        """
        # Get the next message ID and increment for future use
        message_id = self.next_message_id
        with self._lock:
            self.next_message_id += 1
            
        return JavaScriptExecutor.execute_js(
            ws=self.ws,
            is_connected=self.connected,
            lock=self._lock,
            message_id=message_id,
            pending_requests=self.pending_requests,
            code=code,
            timeout=timeout
        )
    
    def get_ui_tree(self, timeout=5):
        """
        Get the React component tree.
        
        Args:
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            dict: The UI tree structure, or an error message if the operation failed.
        """
        success, result = self.execute_js(UI.get_ui_tree(), timeout)
        if success and result:
            if isinstance(result, dict):
                if result.get('success'):
                    return result.get('tree')
                else:
                    error_msg = f"Failed to get UI tree: {result.get('error', 'Unknown error')}"
                    debug_info = result.get('debugInfo', {})
                    logger.error(f"{error_msg}\nDebug Info: {json.dumps(debug_info, indent=2)}")
                    return {"error": error_msg, "debug_info": debug_info}
            return result
        return {"error": "Failed to execute UI tree retrieval code"}
    
    def tap_element(self, test_id=None, text=None, timeout=5):
        """
        Tap an element by test ID or text content.
        
        Args:
            test_id (str, optional): The testID of the element to tap.
            text (str, optional): The text content to search for.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, message)
        """
        if not self.connected:
            return False, "Not connected"
        
        if test_id:
            code = Interaction.tap_by_test_id(test_id)
        elif text:
            code = Interaction.tap_by_text(text)
        else:
            return False, "Must provide either test_id or text"
        
        success, result = self.execute_js(code, timeout)
        if success:
            if result:
                return True, f"Tapped element with {'test ID: ' + test_id if test_id else 'text: ' + text}"
            else:
                return False, f"Element with {'test ID: ' + test_id if test_id else 'text: ' + text} not found or not tappable"
        return False, f"Failed to tap element: {result}"
    
    def enter_text(self, test_id, text, timeout=5):
        """
        Enter text into a TextInput element.
        
        Args:
            test_id (str): The testID of the input element.
            text (str): The text to enter.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, message)
        """
        if not self.connected:
            return False, "Not connected"
        
        code = Interaction.enter_text_by_test_id(test_id, text)
        
        success, result = self.execute_js(code, timeout)
        if success:
            if result:
                return True, f"Entered text into element with test ID: {test_id}"
            else:
                return False, f"TextInput with test ID: {test_id} not found or not editable"
        return False, f"Failed to enter text: {result}"
    
    def get_current_screen(self, timeout=5):
        """
        Get the current screen/route name (if using React Navigation).
        
        Args:
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            str: The current screen name, or an error message if the operation failed.
        """
        if not self.connected:
            return "Not connected"
        
        success, result = self.execute_js(UI.get_current_screen(), timeout)
        if success:
            return result
        return f"Error: {result}"
    
    def navigate_to_screen(self, screen_name, params=None, timeout=5):
        """
        Navigate to a screen (if using React Navigation).
        
        Args:
            screen_name (str): The name of the screen to navigate to.
            params (dict, optional): Parameters to pass to the screen.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, message)
        """
        if not self.connected:
            return False, "Not connected"
        
        # Convert params to JSON string
        params_json = json.dumps(params or {})
        code = Interaction.navigate_to_screen(screen_name, params_json)
        
        success, result = self.execute_js(code, timeout)
        if success:
            if result:
                return True, f"Navigated to screen: {screen_name}"
            else:
                return False, "Navigation not found or navigation failed"
        return False, f"Failed to navigate: {result}"
    
    def close(self):
        """
        Close the connection to the React Native app.
        
        Returns:
            bool: True if closed successfully, False otherwise.
        """
        try:
            if self.ws:
                self.ws.close()
                self.connected = False
                self.ws = None
                
                # Wait for the WebSocket thread to terminate
                if self.ws_thread and self.ws_thread.is_alive():
                    self.ws_thread.join(timeout=2)
                
                self.ws_thread = None
                logger.info("Connection closed successfully")
                return True
            return False
        except Exception as e:
            logger.error(f"Error closing connection: {str(e)}", exc_info=True)
            return False
    
    def __enter__(self):
        """
        Enter the context manager.
        
        Returns:
            HermesInspector: The inspector instance.
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager.
        
        Args:
            exc_type: The exception type, if any.
            exc_val: The exception value, if any.
            exc_tb: The exception traceback, if any.
        """
        self.close()
    
    def scroll(self, direction="down", distance=300, timeout=5):
        """
        Scroll the screen in the specified direction.
        
        Args:
            direction (str): The direction to scroll ("up", "down", "left", "right").
            distance (int): The distance to scroll in pixels.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, message)
        """
        if not self.connected:
            return False, "Not connected"
        
        # Adjust distance based on direction
        dx = 0
        dy = 0
        if direction == "up":
            dy = -distance
        elif direction == "down":
            dy = distance
        elif direction == "left":
            dx = -distance
        elif direction == "right":
            dx = distance
        
        code = Interaction.scroll(dx, dy)
        
        success, result = self.execute_js(code, timeout)
        if success:
            if result:
                return True, f"Scrolled {direction} by {distance} pixels"
            else:
                return False, f"No scrollable elements found or scroll operation failed"
        return False, f"Failed to execute scroll: {result}"
    
    def scroll_element(self, test_id=None, direction="down", distance=300, timeout=5):
        """
        Scroll a specific element by its test ID.
        
        Args:
            test_id (str): The testID of the scrollable element.
            direction (str): The direction to scroll ("up", "down", "left", "right").
            distance (int): The distance to scroll in pixels.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, message)
        """
        if not self.connected:
            return False, "Not connected"
        
        if not test_id:
            return False, "Must provide test_id"
        
        # Adjust distance based on direction
        dx = 0
        dy = 0
        if direction == "up":
            dy = -distance
        elif direction == "down":
            dy = distance
        elif direction == "left":
            dx = -distance
        elif direction == "right":
            dx = distance
        
        code = Interaction.scroll_element(test_id, dx, dy)
        
        success, result = self.execute_js(code, timeout)
        if success:
            if result:
                return True, f"Scrolled element with test ID: {test_id} {direction} by {distance} pixels"
            else:
                return False, f"Element with test ID: {test_id} not found, not scrollable, or scroll operation failed"
        return False, f"Failed to execute scroll element: {result}"
    
    # Debug Visualization Toggles
    
    def toggle_debug_paint_feature(self, enable=True, timeout=5):
        """
        Enable or disable debug painting.
        
        Args:
            enable (bool): Whether to enable or disable the feature.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, message)
        """
        return False, "Debug paint feature is not available - debug module has been removed"
    
    def toggle_performance_overlay(self, enable=True, timeout=5):
        """
        Enable or disable performance overlay.
        
        Args:
            enable (bool): Whether to enable or disable the feature.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, message)
        """
        return False, "Performance overlay feature is not available - debug module has been removed"
    
    def toggle_repaint_rainbow(self, enable=True, timeout=5):
        """
        Enable or disable repaint rainbow visualization.
        
        Args:
            enable (bool): Whether to enable or disable the feature.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, message)
        """
        return False, "Repaint rainbow visualization is not available in React Native"
    
    def toggle_debug_banner(self, enable=True, timeout=5):
        """
        Enable or disable the debug banner.
        
        Args:
            enable (bool): Whether to enable or disable the feature.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, message)
        """
        return False, "Debug banner feature is not available - debug module has been removed"
    
    # Widget finding and interaction
    
    def find_widgets(self, search_by="all", search_value="", timeout=5):
        """
        Find widgets by key, text, or type.
        
        Args:
            search_by (str): What to search by - "key", "text", "type", or "all".
            search_value (str): The value to search for.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, widgets)
        """
        code = UI.find_widgets(search_by, search_value)
        
        success, result = self.execute_js(code, timeout)
        if success:
            return True, result
        return False, f"Failed to find widgets: {result}"
    
    def is_widget_tree_ready(self, timeout=5):
        """
        Check if the widget tree is ready.
        
        Args:
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, is_ready)
        """
        success, result = self.execute_js(UI.is_widget_tree_ready(), timeout)
        if success:
            return True, result
        return False, f"Failed to check widget tree ready state: {result}"
    
    # Tap Widget by Different Locators
    
    def tap_widget_by_key(self, key_value, timeout=5):
        """
        Tap a widget by its key.
        
        Args:
            key_value (str): The key value of the widget to tap.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, message)
        """
        return self.tap_element(test_id=key_value, timeout=timeout)
    
    def tap_widget_by_text(self, text, timeout=5):
        """
        Tap a widget by its text content.
        
        Args:
            text (str): The text content to search for.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, message)
        """
        return self.tap_element(text=text, timeout=timeout)
    
    def tap_widget_by_type(self, widget_type, timeout=5):
        """
        Tap a widget by its type.
        
        Args:
            widget_type (str): The type of widget to tap.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, message)
        """
        code = Interaction.tap_by_type(widget_type)
        
        success, result = self.execute_js(code, timeout)
        if success:
            if result:
                return True, f"Tapped widget of type: {widget_type}"
            else:
                return False, f"Widget of type: {widget_type} not found or not tappable"
        return False, f"Failed to tap widget: {result}"
    
    def tap_widget_by_tooltip(self, tooltip_text, timeout=5):
        """
        Tap a widget by its tooltip text.
        
        Args:
            tooltip_text (str): The tooltip text to search for.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, message)
        """
        code = Interaction.tap_by_tooltip(tooltip_text)
        
        success, result = self.execute_js(code, timeout)
        if success:
            if result:
                return True, f"Tapped widget with tooltip: {tooltip_text}"
            else:
                return False, f"Widget with tooltip: {tooltip_text} not found or not tappable"
        return False, f"Failed to tap widget: {result}"
    
    # Text Entry by Different Locators
    
    def enter_text_by_key(self, key_value, text, timeout=5):
        """
        Enter text into a widget by its key.
        
        Args:
            key_value (str): The key value of the input widget.
            text (str): The text to enter.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, message)
        """
        return self.enter_text(key_value, text, timeout)
    
    def enter_text_by_type(self, widget_type, text, timeout=5):
        """
        Enter text into a widget by its type.
        
        Args:
            widget_type (str): The type of the input widget.
            text (str): The text to enter.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, message)
        """
        code = Interaction.enter_text_by_type(widget_type, text)
        
        success, result = self.execute_js(code, timeout)
        if success:
            if result:
                return True, f"Entered text into widget of type: {widget_type}"
            else:
                return False, f"Widget of type: {widget_type} not found or not a text input"
        return False, f"Failed to enter text: {result}"
    
    def enter_text_by_text(self, widget_text, text, timeout=5):
        """
        Enter text into a widget by its text content.
        
        Args:
            widget_text (str): The text content of the input widget.
            text (str): The text to enter.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, message)
        """
        code = Interaction.enter_text_by_text(widget_text, text)
        
        success, result = self.execute_js(code, timeout)
        if success:
            if result:
                return True, f"Entered text into widget with text content: {widget_text}"
            else:
                return False, f"Widget with text content: {widget_text} not found or not a text input"
        return False, f"Failed to enter text: {result}"
    
    # Screen Info

    
    def list_views(self, timeout=5):
        """
        List available views.
        
        Args:
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, views)
        """
        code = """
        (function() {
            try {
                const views = [];
                
                if (typeof global !== 'undefined' && global.ReactNative) {
                    views.push({
                        id: 'main',
                        type: 'ReactNative',
                        active: true
                    });
                }
                
                return views;
            } catch (e) {
                console.error('Error listing views:', e);
                return [];
            }
        })();
        """
        
        success, result = self.execute_js(code, timeout)
        if success:
            return True, result
        return False, f"Failed to list views: {result}"
    
    # Dump Tree Methods
    
    def dump_widget_tree(self, timeout=5):
        """
        Dump the widget tree.
        
        Args:
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            dict: The widget tree.
        """
        return self.get_ui_tree(timeout)
        
    # Scroll methods for compatibility with Dart VM client
    
    def scroll_down_by_key(self, key_value, timeout=5):
        """
        Scroll down a widget identified by key.
        
        Args:
            key_value (str): The key of the scrollable widget.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, message)
        """
        return self.scroll_element(test_id=key_value, direction="down", timeout=timeout)
    
    def scroll_up_by_key(self, key_value, timeout=5):
        """
        Scroll up a widget identified by key.
        
        Args:
            key_value (str): The key of the scrollable widget.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, message)
        """
        return self.scroll_element(test_id=key_value, direction="up", timeout=timeout)
    
    def scroll_down_by_key_extended(self, key_value, dx=0, dy=100, duration_microseconds=300000, frequency=60, timeout=5):
        """
        Scroll down a widget with extended parameters.
        
        Args:
            key_value (str): The key of the scrollable widget.
            dx (int): Horizontal scroll amount.
            dy (int): Vertical scroll amount (positive = down).
            duration_microseconds (int): Duration of the scroll in microseconds.
            frequency (int): Scroll frequency.
            timeout (int): Timeout in seconds for the operation.
            
        Returns:
            tuple: (success, message)
        """
        # Convert microseconds to milliseconds
        duration_ms = duration_microseconds / 1000
        # React Native doesn't really use the frequency parameter the same way
        # For simplicity, we'll just use the dx/dy values
        
        if not self.connected:
            return False, "Not connected"
        
        code = Interaction.scroll_element(key_value, dx, dy)
        
        success, result = self.execute_js(code, timeout)
        if success:
            if result:
                return True, f"Scrolled widget with key: {key_value} with parameters dx: {dx}, dy: {dy}"
            else:
                return False, f"Widget with key: {key_value} not found, not scrollable, or scroll operation failed"
        return False, f"Failed to execute extended scroll: {result}"