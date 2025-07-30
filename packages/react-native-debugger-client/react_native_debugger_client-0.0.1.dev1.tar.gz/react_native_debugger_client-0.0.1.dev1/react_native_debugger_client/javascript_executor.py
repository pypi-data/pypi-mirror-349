"""
JavaScript Executor for Hermes Debugger.

This module provides a utility class for executing JavaScript code in a React Native
application via the Hermes debugger WebSocket connection.
"""

import json
import queue
import logging

# Configure logging
logger = logging.getLogger(__name__)

class JavaScriptExecutor:
    """
    A utility class for executing JavaScript code in React Native context via Hermes debugger.
    """
    
    @staticmethod
    def execute_js(ws, is_connected, lock, message_id, pending_requests, code, timeout=5):
        """
        Execute JavaScript code in the React Native context.
        
        Args:
            ws: The WebSocket connection to the Hermes debugger
            is_connected (bool): Whether the WebSocket is connected
            lock: A threading lock for thread safety
            message_id (int): The message ID to use
            pending_requests (dict): Dictionary of pending requests by ID
            code (str): The JavaScript code to execute
            timeout (int): Timeout in seconds for the operation
            
        Returns:
            tuple: (success, result)
        """
        if not is_connected:
            return False, "Not connected"
        
        # Create the message
        message = {
            "id": message_id,
            "method": "Runtime.evaluate",
            "params": {
                "expression": code,
                "returnByValue": True,
                "awaitPromise": True
            }
        }
        
        # Create a future for this request
        result_future = queue.Queue()
        with lock:
            pending_requests[message_id] = result_future
        
        try:
            # Send the request
            logger.debug(f"Sending message: {message}")
            ws.send(json.dumps(message))
            
            # Wait for the response with timeout
            try:
                response = result_future.get(timeout=timeout)
                
                # Check for errors
                if 'error' in response:
                    error = response['error']
                    return False, f"JavaScript execution failed: {error.get('message', 'Unknown error')}"
                
                # Extract the result
                if 'result' in response:
                    result = response['result']
                    if 'result' in result:
                        return True, result['result'].get('value')
                    return True, None
                
                return False, "Invalid response format"
            except queue.Empty:
                return False, "Request timed out"
        except Exception as e:
            logger.error(f"Error executing JavaScript: {str(e)}", exc_info=True)
            return False, f"Error: {str(e)}"
        finally:
            # Clean up
            with lock:
                if message_id in pending_requests:
                    del pending_requests[message_id] 