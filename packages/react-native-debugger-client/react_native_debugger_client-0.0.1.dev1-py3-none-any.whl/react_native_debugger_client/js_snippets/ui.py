"""
UI-related JavaScript snippets for Hermes Inspector.

This module contains JavaScript code for retrieving UI elements and tree structures.
"""

import json

class UI:
    """
    Class containing static methods for generating JavaScript code
    for UI-related operations in React Native applications.
    """
    
    @staticmethod
    def get_ui_tree():
        """
        Generate JavaScript to get the UI tree (component hierarchy).
        
        Returns:
            str: JavaScript code to execute.
        """
        return """
(function() {
    try {
        // Debug info to help diagnose issues
        const debugInfo = {
            isBridgeless: typeof global === 'undefined',
            hasReactDevTools: typeof window !== 'undefined' && !!window.__REACT_DEVTOOLS_GLOBAL_HOOK__,
            hasFbBridge: typeof __fbBatchedBridge !== 'undefined',
            hasDocument: typeof document !== 'undefined',
            environment: {}
        };

        // Try to get environment info safely
        try {
            if (typeof global !== 'undefined') {
                debugInfo.environment.global = {
                    hasReactNative: !!global.ReactNative,
                    version: global.ReactNative ? global.ReactNative.version : null
                };
            }
        } catch (e) {
            debugInfo.environment.globalError = e.toString();
        }

        // Function to safely traverse the React fiber tree
        function traverseReactTree() {
            // First try React DevTools hook approach
            if (typeof window !== 'undefined' && window.__REACT_DEVTOOLS_GLOBAL_HOOK__) {
                const hook = window.__REACT_DEVTOOLS_GLOBAL_HOOK__;
                if (hook.renderers && hook.renderers.size > 0) {
                    const renderer = Array.from(hook.renderers.values())[0];
                    const roots = hook.getFiberRoots(1);
                    
                    if (roots && roots.size > 0) {
                        const root = Array.from(roots)[0];
                        const hostRoot = root.current;
                        
                        function traverseFiber(fiber, depth = 0) {
                            if (!fiber) return null;
                            
                            const result = {
                                type: typeof fiber.type === 'string' ? fiber.type : (fiber.type?.displayName || fiber.type?.name || 'Unknown'),
                                key: fiber.key,
                                props: {},
                                children: []
                            };
                            
                            // Safely extract props
                            if (fiber.memoizedProps) {
                                for (const k in fiber.memoizedProps) {
                                    try {
                                        const v = fiber.memoizedProps[k];
                                        if (typeof v !== 'function' && typeof v !== 'object') {
                                            result.props[k] = v;
                                        }
                                    } catch (e) {}
                                }
                            }
                            
                            // Add text content if available
                            if (fiber.memoizedProps?.children && typeof fiber.memoizedProps.children === 'string') {
                                result.text = fiber.memoizedProps.children;
                            }
                            
                            // Add testID if available
                            if (fiber.memoizedProps?.testID) {
                                result.testID = fiber.memoizedProps.testID;
                            }
                            
                            // Process children
                            let child = fiber.child;
                            while (child) {
                                const childData = traverseFiber(child, depth + 1);
                                if (childData) {
                                    result.children.push(childData);
                                }
                                child = child.sibling;
                            }
                            
                            return result;
                        }
                        
                        const tree = traverseFiber(hostRoot);
                        return {
                            success: true,
                            debugInfo,
                            tree
                        };
                    }
                }
            }
            
            // Try alternative approaches if React DevTools hook failed
            
            // Try React Native's component registry (classic mode)
            if (typeof __fbBatchedBridge !== 'undefined') {
                const componentRegistry = __fbBatchedBridge._remoteModuleRegistry;
                if (componentRegistry && componentRegistry.UIManager) {
                    return {
                        success: true,
                        debugInfo,
                        tree: {
                            type: "ReactNativeRoot",
                            message: "Found React Native UIManager",
                            components: Object.keys(componentRegistry)
                        }
                    };
                }
            }
            
            // Try DOM-based approach (React Native Web)
            if (typeof document !== 'undefined') {
                const rootElements = document.querySelectorAll('[data-testid]');
                if (rootElements.length > 0) {
                    const domTree = {
                        type: "ReactDOMRoot",
                        children: Array.from(rootElements).map(el => ({
                            type: el.tagName,
                            testID: el.getAttribute('data-testid'),
                            text: el.textContent,
                            children: []
                        }))
                    };
                    
                    return {
                        success: true,
                        debugInfo,
                        tree: domTree
                    };
                }
            }
            
            // No approach succeeded
            return {
                success: false,
                debugInfo,
                error: "Could not access React component tree through any available method"
            };
        }
        
        return traverseReactTree();
    } catch (e) {
        return {
            success: false,
            error: e.toString()
        };
    }
})();
"""
    
    @staticmethod
    def is_widget_tree_ready():
        """
        Generate JavaScript to check if widget tree is ready.
        
        Returns:
            str: JavaScript code to execute.
        """
        return """
(function() {
    try {
        if (typeof window !== 'undefined' && window.__REACT_DEVTOOLS_GLOBAL_HOOK__) {
            const hook = window.__REACT_DEVTOOLS_GLOBAL_HOOK__;
            if (hook.renderers && hook.renderers.size > 0) {
                const roots = hook.getFiberRoots(1);
                return roots && roots.size > 0;
            }
        }
        
        return false;
    } catch (e) {
        console.error('Error checking widget tree ready state:', e);
        return false;
    }
})();
"""
    
    @staticmethod
    def find_widgets(search_by, search_value):
        """
        Generate JavaScript to find widgets by key, text, or type.
        
        Args:
            search_by (str): What to search by - "key", "text", "type", or "all".
            search_value (str): The value to search for.
            
        Returns:
            str: JavaScript code to execute.
        """
        return """
(function() {
    try {
        // Function to find elements in the React tree
        function findElements(searchBy, searchValue) {
            const results = [];
            
            function traverse(fiber, path = []) {
                if (!fiber) return;
                
                const elementType = typeof fiber.type === 'string' ? 
                    fiber.type : (fiber.type?.displayName || fiber.type?.name || 'Unknown');
                
                let match = false;
                
                // Check if this element matches the search criteria
                if (searchBy === 'key' || searchBy === 'all') {
                    if (fiber.key && fiber.key.includes(searchValue)) {
                        match = true;
                    }
                }
                
                if (searchBy === 'text' || searchBy === 'all') {
                    const hasText = (
                        (fiber.memoizedProps && fiber.memoizedProps.children === searchValue) ||
                        (fiber.memoizedProps && fiber.memoizedProps.text === searchValue) ||
                        (fiber.pendingProps && fiber.pendingProps.children === searchValue)
                    );
                    
                    if (hasText) {
                        match = true;
                    }
                }
                
                if (searchBy === 'type' || searchBy === 'all') {
                    if (elementType.includes(searchValue)) {
                        match = true;
                    }
                }
                
                if (match) {
                    // Create a simple representation of the element
                    const element = {
                        id: fiber.stateNode?._nativeTag || fiber._debugID || results.length,
                        type: elementType,
                        key: fiber.key,
                        props: {},
                        path: [...path, elementType]
                    };
                    
                    // Safely extract props
                    if (fiber.memoizedProps) {
                        for (const k in fiber.memoizedProps) {
                            try {
                                const v = fiber.memoizedProps[k];
                                if (typeof v !== 'function' && typeof v !== 'object') {
                                    element.props[k] = v;
                                }
                            } catch (e) {}
                        }
                    }
                    
                    // Add text content if available
                    if (fiber.memoizedProps?.children && typeof fiber.memoizedProps.children === 'string') {
                        element.text = fiber.memoizedProps.children;
                    }
                    
                    // Add testID if available
                    if (fiber.memoizedProps?.testID) {
                        element.testID = fiber.memoizedProps.testID;
                    }
                    
                    results.push(element);
                }
                
                // Process children
                if (fiber.child) {
                    traverse(fiber.child, [...path, elementType]);
                }
                
                // Process siblings
                if (fiber.sibling) {
                    traverse(fiber.sibling, path);
                }
            }
            
            // Start traversal from root
            const hook = window.__REACT_DEVTOOLS_GLOBAL_HOOK__;
            if (hook && hook.renderers.size > 0) {
                const roots = hook.getFiberRoots(1);
                if (roots && roots.size > 0) {
                    const root = Array.from(roots)[0];
                    traverse(root.current);
                }
            }
            
            return results;
        }
        
        return findElements(""" + json.dumps(search_by) + """, """ + json.dumps(search_value) + """);
    } catch (e) {
        console.error('Error finding widgets:', e);
        return [];
    }
})();
"""
    
    @staticmethod
    def get_current_screen():
        """
        Generate JavaScript to get current screen or route name.
        
        Returns:
            str: JavaScript code to execute.
        """
        return """
(function() {
    try {
        // Try to access React Navigation state
        if (typeof window !== 'undefined') {
            // Check for React Navigation in window context
            if (window.ReactNavigation && window.ReactNavigation.navigation) {
                const nav = window.ReactNavigation.navigation;
                const currentRoute = nav.getCurrentRoute();
                return currentRoute ? currentRoute.name : "Unknown Screen";
            }
            
            // Alternative approach for React Navigation 5+
            if (window.__REACT_NAVIGATION_DEVTOOLS_EXTENSION__ && 
                window.__REACT_NAVIGATION_DEVTOOLS_EXTENSION__.navigationContainers) {
                const containers = window.__REACT_NAVIGATION_DEVTOOLS_EXTENSION__.navigationContainers;
                if (containers.size > 0) {
                    const container = containers.values().next().value;
                    const state = container.getRootState();
                    if (state && state.routes && state.routes.length > 0) {
                        const currentRoute = state.routes[state.index];
                        return currentRoute.name;
                    }
                }
            }
        }
        
        // Try to access React Native's component registry
        if (typeof __fbBatchedBridge !== 'undefined') {
            return "Current screen detection requires React Navigation setup";
        }
        
        return "Unknown Screen (Navigation not found)";
    } catch (e) {
        return "Error getting current screen: " + e.toString();
    }
})();
"""
    
    @staticmethod
    def get_display_refresh_rate():
        """
        Generate JavaScript to get the display refresh rate.
        
        Returns:
            str: JavaScript code to execute.
        """
        return """
(function() {
    try {
        if (typeof window !== 'undefined' && window.screen) {
            if (window.screen.displayRate) {
                return window.screen.displayRate;
            }
            
            // Try to estimate using requestAnimationFrame
            if (window.requestAnimationFrame) {
                // This is just a placeholder - actual implementation would need 
                // to measure multiple frames for accuracy
                return 60; // Default to 60Hz
            }
        }
        
        if (typeof global !== 'undefined' && global.ReactNative) {
            // ReactNative might expose this in the global object
            return 60; // Default to 60Hz
        }
        
        return null;
    } catch (e) {
        console.error('Error getting display refresh rate:', e);
        return null;
    }
})();
"""