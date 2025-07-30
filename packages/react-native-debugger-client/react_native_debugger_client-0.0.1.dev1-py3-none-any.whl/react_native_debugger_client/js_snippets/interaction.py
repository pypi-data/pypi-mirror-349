"""
Interaction-related JavaScript snippets for Hermes Inspector.

This module contains JavaScript code for interacting with UI elements
such as tapping, scrolling, and entering text.
"""

import json


class Interaction:
    """
    Class containing static methods for generating JavaScript code
    for UI interactions in React Native applications.
    """
    
    @staticmethod
    def tap_by_test_id(test_id):
        """
        Generate JavaScript to tap an element by its testID.
        
        Args:
            test_id (str): The testID of the element to tap.
            
        Returns:
            str: JavaScript code to execute.
        """
        return """
(function() {
    try {
        // Function to find element by testID and trigger press event
        function findAndTapByTestId(testId) {
            // Try to find the element in the React tree
            function traverse(fiber) {
                if (!fiber) return null;
                
                // Check if this element has the testID
                if (fiber.memoizedProps && fiber.memoizedProps.testID === testId) {
                    // Found the element, now find its closest Touchable ancestor
                    let current = fiber;
                    while (current) {
                        const type = current.type && (current.type.displayName || current.type.name);
                        if (type && (type.includes('Touchable') || type.includes('Pressable'))) {
                            if (current.memoizedProps && current.memoizedProps.onPress) {
                                current.memoizedProps.onPress();
                                return true;
                            }
                        }
                        current = current.return;
                    }
                }
                
                // Check children
                if (fiber.child) {
                    const result = traverse(fiber.child);
                    if (result) return result;
                }
                
                // Check siblings
                if (fiber.sibling) {
                    const result = traverse(fiber.sibling);
                    if (result) return result;
                }
                
                return null;
            }
            
            // Start traversal from root
            const hook = window.__REACT_DEVTOOLS_GLOBAL_HOOK__;
            if (hook && hook.renderers.size > 0) {
                const roots = hook.getFiberRoots(1);
                if (roots && roots.size > 0) {
                    const root = Array.from(roots)[0];
                    return traverse(root.current) || false;
                }
            }
            
            return false;
        }
        
        return findAndTapByTestId(""" + json.dumps(test_id) + """);
    } catch (e) {
        console.error('Error in tap by testID:', e);
        return false;
    }
})();
"""
    
    @staticmethod
    def tap_by_text(text):
        """
        Generate JavaScript to tap an element by its text content.
        
        Args:
            text (str): The text content to search for.
            
        Returns:
            str: JavaScript code to execute.
        """
        return """
(function() {
    try {
        // Function to find element by text content and trigger press event
        function findAndTapByText(searchText) {
            // Try to find the element in the React tree
            function traverse(fiber) {
                if (!fiber) return null;
                
                // Check if this element has the text content
                const hasText = (
                    (fiber.memoizedProps && fiber.memoizedProps.children === searchText) ||
                    (fiber.memoizedProps && fiber.memoizedProps.text === searchText) ||
                    (fiber.pendingProps && fiber.pendingProps.children === searchText)
                );
                
                if (hasText) {
                    // Found the element, now find its closest Touchable ancestor
                    let current = fiber;
                    while (current) {
                        const type = current.type && (current.type.displayName || current.type.name);
                        if (type && (type.includes('Touchable') || type.includes('Pressable'))) {
                            if (current.memoizedProps && current.memoizedProps.onPress) {
                                current.memoizedProps.onPress();
                                return true;
                            }
                        }
                        current = current.return;
                    }
                }
                
                // Check children
                if (fiber.child) {
                    const result = traverse(fiber.child);
                    if (result) return result;
                }
                
                // Check siblings
                if (fiber.sibling) {
                    const result = traverse(fiber.sibling);
                    if (result) return result;
                }
                
                return null;
            }
            
            // Start traversal from root
            const hook = window.__REACT_DEVTOOLS_GLOBAL_HOOK__;
            if (hook && hook.renderers.size > 0) {
                const roots = hook.getFiberRoots(1);
                if (roots && roots.size > 0) {
                    const root = Array.from(roots)[0];
                    return traverse(root.current) || false;
                }
            }
            
            return false;
        }
        
        return findAndTapByText(""" + json.dumps(text) + """);
    } catch (e) {
        console.error('Error in tap by text:', e);
        return false;
    }
})();
"""
    
    @staticmethod
    def tap_by_type(widget_type):
        """
        Generate JavaScript to tap an element by its type.
        
        Args:
            widget_type (str): The type of widget to tap.
            
        Returns:
            str: JavaScript code to execute.
        """
        return """
(function() {
    try {
        // Function to find element by type and trigger press event
        function findAndTapByType(type) {
            // Try to find the element in the React tree
            function traverse(fiber) {
                if (!fiber) return null;
                
                // Check if this element has the matching type
                const elementType = typeof fiber.type === 'string' ? 
                    fiber.type : (fiber.type?.displayName || fiber.type?.name || '');
                
                if (elementType.includes(type)) {
                    // Found the element, now find its closest Touchable ancestor
                    let current = fiber;
                    while (current) {
                        const currentType = current.type && (current.type.displayName || current.type.name);
                        if (currentType && (currentType.includes('Touchable') || currentType.includes('Pressable'))) {
                            if (current.memoizedProps && current.memoizedProps.onPress) {
                                current.memoizedProps.onPress();
                                return true;
                            }
                        }
                        current = current.return;
                    }
                }
                
                // Check children
                if (fiber.child) {
                    const result = traverse(fiber.child);
                    if (result) return result;
                }
                
                // Check siblings
                if (fiber.sibling) {
                    const result = traverse(fiber.sibling);
                    if (result) return result;
                }
                
                return null;
            }
            
            // Start traversal from root
            const hook = window.__REACT_DEVTOOLS_GLOBAL_HOOK__;
            if (hook && hook.renderers.size > 0) {
                const roots = hook.getFiberRoots(1);
                if (roots && roots.size > 0) {
                    const root = Array.from(roots)[0];
                    return traverse(root.current) || false;
                }
            }
            
            return false;
        }
        
        return findAndTapByType(""" + json.dumps(widget_type) + """);
    } catch (e) {
        console.error('Error in tap by type:', e);
        return false;
    }
})();
"""
    
    @staticmethod
    def tap_by_tooltip(tooltip_text):
        """
        Generate JavaScript to tap an element by its tooltip text.
        
        Args:
            tooltip_text (str): The tooltip text to search for.
            
        Returns:
            str: JavaScript code to execute.
        """
        return """
(function() {
    try {
        // Function to find element by tooltip and trigger press event
        function findAndTapByTooltip(tooltip) {
            // Try to find the element in the React tree
            function traverse(fiber) {
                if (!fiber) return null;
                
                // Check if this element has the tooltip text
                const hasTooltip = (
                    (fiber.memoizedProps && fiber.memoizedProps.accessibilityLabel === tooltip) ||
                    (fiber.memoizedProps && fiber.memoizedProps.tooltip === tooltip) ||
                    (fiber.memoizedProps && fiber.memoizedProps['aria-label'] === tooltip)
                );
                
                if (hasTooltip) {
                    // Found the element, now find its closest Touchable ancestor
                    let current = fiber;
                    while (current) {
                        const type = current.type && (current.type.displayName || current.type.name);
                        if (type && (type.includes('Touchable') || type.includes('Pressable'))) {
                            if (current.memoizedProps && current.memoizedProps.onPress) {
                                current.memoizedProps.onPress();
                                return true;
                            }
                        }
                        current = current.return;
                    }
                }
                
                // Check children
                if (fiber.child) {
                    const result = traverse(fiber.child);
                    if (result) return result;
                }
                
                // Check siblings
                if (fiber.sibling) {
                    const result = traverse(fiber.sibling);
                    if (result) return result;
                }
                
                return null;
            }
            
            // Start traversal from root
            const hook = window.__REACT_DEVTOOLS_GLOBAL_HOOK__;
            if (hook && hook.renderers.size > 0) {
                const roots = hook.getFiberRoots(1);
                if (roots && roots.size > 0) {
                    const root = Array.from(roots)[0];
                    return traverse(root.current) || false;
                }
            }
            
            return false;
        }
        
        return findAndTapByTooltip(""" + json.dumps(tooltip_text) + """);
    } catch (e) {
        console.error('Error in tap by tooltip:', e);
        return false;
    }
})();
"""
    
    @staticmethod
    def enter_text_by_test_id(test_id, text):
        """
        Generate JavaScript to enter text into an element by its testID.
        
        Args:
            test_id (str): The testID of the input element.
            text (str): The text to enter.
            
        Returns:
            str: JavaScript code to execute.
        """
        return """
(function() {
    try {
        // Find input by testID and set its text
        const findAndSetTextByTestId = (testId, inputText) => {
            // Try DOM-based approach for React Native Web
            if (typeof document !== 'undefined') {
                const elements = document.querySelectorAll(`[data-testid="${testId}"]`);
                if (elements.length > 0 && (elements[0].tagName === 'INPUT' || elements[0].tagName === 'TEXTAREA')) {
                    elements[0].value = inputText;
                    // Trigger change event
                    const event = new Event('input', { bubbles: true });
                    elements[0].dispatchEvent(event);
                    return true;
                }
            }
            
            // Try to access React Native's component registry
            if (typeof __fbBatchedBridge !== 'undefined') {
                // This is a simplified approach - in a real implementation,
                // we would need more sophisticated techniques to find and interact
                // with specific components
                return false;
            }
            
            return false;
        };
        
        return findAndSetTextByTestId(""" + json.dumps(test_id) + """, """ + json.dumps(text) + """);
    } catch (e) {
        return false;
    }
})();
"""
    
    @staticmethod
    def enter_text_by_type(widget_type, text):
        """
        Generate JavaScript to enter text into an element by its type.
        
        Args:
            widget_type (str): The type of the input widget.
            text (str): The text to enter.
            
        Returns:
            str: JavaScript code to execute.
        """
        return """
(function() {
    try {
        // Function to find input by type and set its text
        function findAndSetTextByType(type, inputText) {
            // Try to find the element in the React tree
            function traverse(fiber) {
                if (!fiber) return null;
                
                // Check if this element has the matching type
                const elementType = typeof fiber.type === 'string' ? 
                    fiber.type : (fiber.type?.displayName || fiber.type?.name || '');
                
                if (elementType.includes(type)) {
                    // Check if this is an input element (TextInput)
                    if (elementType.includes('TextInput') || elementType.includes('Input')) {
                        if (fiber.memoizedProps && fiber.memoizedProps.onChangeText) {
                            fiber.memoizedProps.onChangeText(inputText);
                            return true;
                        }
                        
                        if (fiber.memoizedProps && fiber.memoizedProps.onChange) {
                            const event = { nativeEvent: { text: inputText } };
                            fiber.memoizedProps.onChange(event);
                            return true;
                        }
                    }
                }
                
                // Check children
                if (fiber.child) {
                    const result = traverse(fiber.child);
                    if (result) return result;
                }
                
                // Check siblings
                if (fiber.sibling) {
                    const result = traverse(fiber.sibling);
                    if (result) return result;
                }
                
                return null;
            }
            
            // Start traversal from root
            const hook = window.__REACT_DEVTOOLS_GLOBAL_HOOK__;
            if (hook && hook.renderers.size > 0) {
                const roots = hook.getFiberRoots(1);
                if (roots && roots.size > 0) {
                    const root = Array.from(roots)[0];
                    return traverse(root.current) || false;
                }
            }
            
            return false;
        }
        
        return findAndSetTextByType(""" + json.dumps(widget_type) + """, """ + json.dumps(text) + """);
    } catch (e) {
        console.error('Error in enter text by type:', e);
        return false;
    }
})();
"""
    
    @staticmethod
    def enter_text_by_text(widget_text, text):
        """
        Generate JavaScript to enter text into an element by its text content.
        
        Args:
            widget_text (str): The text content of the input widget.
            text (str): The text to enter.
            
        Returns:
            str: JavaScript code to execute.
        """
        return """
(function() {
    try {
        // Function to find input by text and set its text
        function findAndSetTextByText(searchText, inputText) {
            // Try to find the element in the React tree
            function traverse(fiber) {
                if (!fiber) return null;
                
                // Check if this element has the text content
                const hasText = (
                    (fiber.memoizedProps && fiber.memoizedProps.children === searchText) ||
                    (fiber.memoizedProps && fiber.memoizedProps.text === searchText) ||
                    (fiber.pendingProps && fiber.pendingProps.children === searchText) ||
                    (fiber.memoizedProps && fiber.memoizedProps.placeholder === searchText)
                );
                
                if (hasText) {
                    // Check if this is an input element (TextInput)
                    const elementType = typeof fiber.type === 'string' ? 
                        fiber.type : (fiber.type?.displayName || fiber.type?.name || '');
                        
                    if (elementType.includes('TextInput') || elementType.includes('Input')) {
                        if (fiber.memoizedProps && fiber.memoizedProps.onChangeText) {
                            fiber.memoizedProps.onChangeText(inputText);
                            return true;
                        }
                        
                        if (fiber.memoizedProps && fiber.memoizedProps.onChange) {
                            const event = { nativeEvent: { text: inputText } };
                            fiber.memoizedProps.onChange(event);
                            return true;
                        }
                    }
                }
                
                // Check children
                if (fiber.child) {
                    const result = traverse(fiber.child);
                    if (result) return result;
                }
                
                // Check siblings
                if (fiber.sibling) {
                    const result = traverse(fiber.sibling);
                    if (result) return result;
                }
                
                return null;
            }
            
            // Start traversal from root
            const hook = window.__REACT_DEVTOOLS_GLOBAL_HOOK__;
            if (hook && hook.renderers.size > 0) {
                const roots = hook.getFiberRoots(1);
                if (roots && roots.size > 0) {
                    const root = Array.from(roots)[0];
                    return traverse(root.current) || false;
                }
            }
            
            return false;
        }
        
        return findAndSetTextByText(""" + json.dumps(widget_text) + """, """ + json.dumps(text) + """);
    } catch (e) {
        console.error('Error in enter text by text:', e);
        return false;
    }
})();
"""
    
    @staticmethod
    def scroll(dx, dy):
        """
        Generate JavaScript to scroll in a direction.
        
        Args:
            dx (int): Horizontal scroll amount.
            dy (int): Vertical scroll amount.
            
        Returns:
            str: JavaScript code to execute.
        """
        return """
(function() {
    try {
        // Function to find scrollable elements and scroll them
        function scrollInDirection(dx, dy) {
            // Start traversal from root to find scrollable views
            function findScrollableViews(fiber) {
                if (!fiber) return [];
                
                const scrollables = [];
                const type = fiber.type && (typeof fiber.type === 'string' ? 
                    fiber.type : (fiber.type.displayName || fiber.type.name));
                
                // Check if this element is scrollable
                const isScrollable = (
                    type && (
                        type.includes('ScrollView') || 
                        type.includes('FlatList') || 
                        type.includes('SectionList') ||
                        type.includes('ScrollableView')
                    )
                );
                
                if (isScrollable) {
                    scrollables.push(fiber);
                }
                
                // Check children
                if (fiber.child) {
                    scrollables.push(...findScrollableViews(fiber.child));
                }
                
                // Check siblings
                if (fiber.sibling) {
                    scrollables.push(...findScrollableViews(fiber.sibling));
                }
                
                return scrollables;
            }
            
            // Get React DevTools hook
            const hook = window.__REACT_DEVTOOLS_GLOBAL_HOOK__;
            if (hook && hook.renderers.size > 0) {
                const roots = hook.getFiberRoots(1);
                if (roots && roots.size > 0) {
                    const root = Array.from(roots)[0];
                    const scrollables = findScrollableViews(root.current);
                    
                    if (scrollables.length > 0) {
                        // Try to scroll each scrollable view
                        for (const scrollable of scrollables) {
                            const stateNode = scrollable.stateNode;
                            
                            // Try different scrolling methods
                            if (stateNode && stateNode.scrollTo) {
                                // ScrollView typically has scrollTo
                                stateNode.scrollTo({ 
                                    x: dx > 0 ? dx : undefined, 
                                    y: dy > 0 ? dy : undefined, 
                                    animated: true 
                                });
                                return true;
                            } else if (stateNode && stateNode.scrollToOffset) {
                                // FlatList typically has scrollToOffset
                                stateNode.scrollToOffset({ 
                                    offset: Math.abs(dy || dx), 
                                    animated: true 
                                });
                                return true;
                            } else if (scrollable.memoizedProps && scrollable.memoizedProps.onScroll) {
                                // Try to simulate a scroll event
                                const scrollEvent = {
                                    nativeEvent: {
                                        contentOffset: { 
                                            x: dx > 0 ? dx : 0, 
                                            y: dy > 0 ? dy : 0 
                                        },
                                        contentSize: { 
                                            width: 1000, 
                                            height: 1000 
                                        },
                                        layoutMeasurement: { 
                                            width: 400, 
                                            height: 700 
                                        }
                                    }
                                };
                                scrollable.memoizedProps.onScroll(scrollEvent);
                                return true;
                            }
                        }
                    }
                }
            }
            
            return false;
        }
        
        return scrollInDirection(""" + str(dx) + """, """ + str(dy) + """);
    } catch (e) {
        console.error('Error in scroll:', e);
        return false;
    }
})();
"""
    
    @staticmethod
    def scroll_element(test_id, dx, dy):
        """
        Generate JavaScript to scroll a specific element by its testID.
        
        Args:
            test_id (str): The testID of the scrollable element.
            dx (int): Horizontal scroll amount.
            dy (int): Vertical scroll amount.
            
        Returns:
            str: JavaScript code to execute.
        """
        return """
(function() {
    try {
        // Function to find a specific scrollable element by testID and scroll it
        function scrollElementByTestId(testId, dx, dy) {
            // Find the element with the given testID
            function findElementByTestId(fiber) {
                if (!fiber) return null;
                
                // Check if this element has the testID
                if (fiber.memoizedProps && fiber.memoizedProps.testID === testId) {
                    return fiber;
                }
                
                // Check children
                if (fiber.child) {
                    const result = findElementByTestId(fiber.child);
                    if (result) return result;
                }
                
                // Check siblings
                if (fiber.sibling) {
                    const result = findElementByTestId(fiber.sibling);
                    if (result) return result;
                }
                
                return null;
            }
            
            // Get React DevTools hook
            const hook = window.__REACT_DEVTOOLS_GLOBAL_HOOK__;
            if (hook && hook.renderers.size > 0) {
                const roots = hook.getFiberRoots(1);
                if (roots && roots.size > 0) {
                    const root = Array.from(roots)[0];
                    const element = findElementByTestId(root.current);
                    
                    if (element) {
                        // Check if the element itself is scrollable
                        const type = element.type && (typeof element.type === 'string' ? 
                            element.type : (element.type.displayName || element.type.name));
                        
                        const isScrollable = (
                            type && (
                                type.includes('ScrollView') || 
                                type.includes('FlatList') || 
                                type.includes('SectionList') ||
                                type.includes('ScrollableView')
                            )
                        );
                        
                        if (isScrollable) {
                            // Try to scroll the element
                            const stateNode = element.stateNode;
                            
                            if (stateNode && stateNode.scrollTo) {
                                stateNode.scrollTo({ 
                                    x: dx > 0 ? dx : undefined, 
                                    y: dy > 0 ? dy : undefined, 
                                    animated: true 
                                });
                                return true;
                            } else if (stateNode && stateNode.scrollToOffset) {
                                stateNode.scrollToOffset({ 
                                    offset: Math.abs(dy || dx), 
                                    animated: true 
                                });
                                return true;
                            } else if (element.memoizedProps && element.memoizedProps.onScroll) {
                                // Try to simulate a scroll event
                                const scrollEvent = {
                                    nativeEvent: {
                                        contentOffset: { 
                                            x: dx > 0 ? dx : 0, 
                                            y: dy > 0 ? dy : 0 
                                        },
                                        contentSize: { 
                                            width: 1000, 
                                            height: 1000 
                                        },
                                        layoutMeasurement: { 
                                            width: 400, 
                                            height: 700 
                                        }
                                    }
                                };
                                element.memoizedProps.onScroll(scrollEvent);
                                return true;
                            }
                        }
                        
                        // If the element itself is not scrollable, look for a scrollable parent
                        let current = element.return;
                        while (current) {
                            const parentType = current.type && (typeof current.type === 'string' ? 
                                current.type : (current.type.displayName || current.type.name));
                            
                            const isParentScrollable = (
                                parentType && (
                                    parentType.includes('ScrollView') || 
                                    parentType.includes('FlatList') || 
                                    parentType.includes('SectionList') ||
                                    parentType.includes('ScrollableView')
                                )
                            );
                            
                            if (isParentScrollable) {
                                // Try to scroll the parent
                                const stateNode = current.stateNode;
                                
                                if (stateNode && stateNode.scrollTo) {
                                    stateNode.scrollTo({ 
                                        x: dx > 0 ? dx : undefined, 
                                        y: dy > 0 ? dy : undefined, 
                                        animated: true 
                                    });
                                    return true;
                                } else if (stateNode && stateNode.scrollToOffset) {
                                    stateNode.scrollToOffset({ 
                                        offset: Math.abs(dy || dx), 
                                        animated: true 
                                    });
                                    return true;
                                } else if (current.memoizedProps && current.memoizedProps.onScroll) {
                                    // Try to simulate a scroll event
                                    const scrollEvent = {
                                        nativeEvent: {
                                            contentOffset: { 
                                                x: dx > 0 ? dx : 0, 
                                                y: dy > 0 ? dy : 0 
                                            },
                                            contentSize: { 
                                                width: 1000, 
                                                height: 1000 
                                            },
                                            layoutMeasurement: { 
                                                width: 400, 
                                                height: 700 
                                            }
                                        }
                                    };
                                    current.memoizedProps.onScroll(scrollEvent);
                                    return true;
                                }
                            }
                            
                            current = current.return;
                        }
                    }
                }
            }
            
            return false;
        }
        
        return scrollElementByTestId(""" + json.dumps(test_id) + """, """ + str(dx) + """, """ + str(dy) + """);
    } catch (e) {
        console.error('Error in scroll element:', e);
        return false;
    }
})();
"""
    
    @staticmethod
    def navigate_to_screen(screen_name, params_json):
        """
        Generate JavaScript to navigate to a different screen.
        
        Args:
            screen_name (str): The name of the screen to navigate to.
            params_json (str): JSON string of parameters to pass to the screen.
            
        Returns:
            str: JavaScript code to execute.
        """
        return """
(function() {
    try {
        // Try to access React Navigation
        if (typeof window !== 'undefined') {
            // Check for React Navigation in window context
            if (window.ReactNavigation && window.ReactNavigation.navigation) {
                const nav = window.ReactNavigation.navigation;
                nav.navigate(""" + json.dumps(screen_name) + """, """ + params_json + """);
                return true;
            }
            
            // Alternative approach for React Navigation 5+
            if (window.__REACT_NAVIGATION_DEVTOOLS_EXTENSION__ && 
                window.__REACT_NAVIGATION_DEVTOOLS_EXTENSION__.navigationContainers) {
                const containers = window.__REACT_NAVIGATION_DEVTOOLS_EXTENSION__.navigationContainers;
                if (containers.size > 0) {
                    const container = containers.values().next().value;
                    container.navigate(""" + json.dumps(screen_name) + """, """ + params_json + """);
                    return true;
                }
            }
        }
        
        return false;
    } catch (e) {
        return false;
    }
})();
"""
    
    @staticmethod
    def exit_app():
        """
        Generate JavaScript to exit the application.
        
        Returns:
            str: JavaScript code to execute.
        """
        return """
(function() {
    try {
        if (typeof global !== 'undefined' && global.ReactNative) {
            if (global.ReactNative.BackHandler && global.ReactNative.BackHandler.exitApp) {
                global.ReactNative.BackHandler.exitApp();
                return true;
            }
        }
        
        return false;
    } catch (e) {
        console.error('Error exiting app:', e);
        return false;
    }
})();
"""