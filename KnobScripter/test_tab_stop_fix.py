#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick test for the setTabStopWidth compatibility fix
Run this in Nuke to test if the issue is resolved.
"""

import nuke

def test_tab_stop_compatibility():
    """Test the tab stop width compatibility"""
    print(f"Testing tab stop compatibility in Nuke {nuke.NUKE_VERSION_MAJOR}.{nuke.NUKE_VERSION_MINOR}")
    
    try:
        # Import required modules
        if nuke.NUKE_VERSION_MAJOR >= 16:
            from PySide6 import QtWidgets
        else:
            from PySide2 import QtWidgets
        
        # Create a simple text widget to test
        widget = QtWidgets.QTextEdit()
        
        # Test the methods
        print("Testing tab stop methods...")
        
        # Test getter
        if hasattr(widget, 'tabStopDistance'):
            current_width = widget.tabStopDistance()
            print(f"tabStopDistance() works: {current_width}")
        elif hasattr(widget, 'tabStopWidth'):
            current_width = widget.tabStopWidth()
            print(f"tabStopWidth() works: {current_width}")
        else:
            print("No tab stop getter method found")
            return False
            
        # Test setter
        if hasattr(widget, 'setTabStopDistance'):
            widget.setTabStopDistance(40)
            print("setTabStopDistance() works")
        elif hasattr(widget, 'setTabStopWidth'):
            widget.setTabStopWidth(40)
            print("setTabStopWidth() works")
        else:
            print("No tab stop setter method found")
            return False

        print("Tab stop compatibility test passed!")
        return True
        
    except Exception as e:
        print(f"Tab stop compatibility test failed: {e}")
        return False

def test_font_metrics_compatibility():
    """Test font metrics compatibility"""
    print("Testing font metrics compatibility...")
    
    try:
        if nuke.NUKE_VERSION_MAJOR >= 16:
            from PySide6 import QtGui
        else:
            from PySide2 import QtGui
            
        font = QtGui.QFont()
        metrics = QtGui.QFontMetrics(font)
        
        # Test width measurement
        if hasattr(metrics, 'horizontalAdvance'):
            width = metrics.horizontalAdvance('A')
            print(f"horizontalAdvance() works: {width}")
        elif hasattr(metrics, 'width'):
            width = metrics.width('A')
            print(f"width() works: {width}")
        else:
            print("No width measurement method found")
            return False

        print("Font metrics compatibility test passed!")
        return True
        
    except Exception as e:
        print(f"Font metrics compatibility test failed: {e}")
        return False

def main():
    """Run all compatibility tests"""
    print("=" * 50)
    print("Tab Stop & Font Metrics Compatibility Test")
    print("=" * 50)
    
    tests = [
        ("Tab Stop Methods", test_tab_stop_compatibility),
        ("Font Metrics Methods", test_font_metrics_compatibility),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"{test_name} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("=" * 50)

if __name__ == "__main__":
    main()
