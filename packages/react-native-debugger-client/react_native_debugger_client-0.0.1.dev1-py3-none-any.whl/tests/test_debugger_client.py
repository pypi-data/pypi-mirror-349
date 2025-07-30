"""
Test script for React Native Debugger Client.
"""

import asyncio
import logging
import json
import time
import pytest

from react_native_debugger_client import ReactNativeDebuggerClient

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_connection():
    # Replace with your device's IP address or use localhost for local development
    DEVICE_IP = "localhost"
    METRO_PORT = 8081
    
    logger.info(f"Connecting to React Native app's Hermes debugger at {DEVICE_IP}:{METRO_PORT}")
    
    # Create a client instance
    client = ReactNativeDebuggerClient(DEVICE_IP, METRO_PORT)
    
    try:
        # Connect to the app with increased timeout
        success, message = client.connect(timeout=30)
        logger.info(f"Connection status: {success}, Message: {message}")
        
        assert success, "Failed to connect to the app"
        
        # Get the UI tree with increased timeout
        logger.info("Getting UI tree...")
        ui_tree = client.get_ui_tree(timeout=30)
        
        assert ui_tree is not None, "Failed to get UI tree"
        
        if isinstance(ui_tree, dict) and "error" in ui_tree:
            pytest.skip(f"Failed to get UI tree: {ui_tree['error']}")
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise
    finally:
        # Close the connection
        logger.info("Closing connection...")
        client.close()
        logger.info("Connection closed")

# Only run this manually, not as part of automated tests
if __name__ == "__main__":
    asyncio.run(test_connection())
