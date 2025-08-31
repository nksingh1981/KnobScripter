#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
KnobScripter Nuke 16 Compatibility Test
This script tests the main compatibility issues with Nuke 16.
Run this script inside Nuke to verify the fixes work.
"""

import nuke

def test_qt_imports():
    """Test Qt imports work correctly across Nuke versions"""
    print(f"Testing Qt imports for Nuke {nuke.NUKE_VERSION_MAJOR}.{nuke.NUKE_VERSION_MINOR}")
    
    try:
        if nuke.NUKE_VERSION_MAJOR < 11:
            from PySide import QtCore, QtGui, QtGui as QtWidgets
            from PySide.QtCore import Qt
            QAction = QtGui.QAction
            QStringListModel = QtGui.QStringListModel
            print("PySide imports successful (Nuke < 11)")
        elif nuke.NUKE_VERSION_MAJOR < 16:
            from PySide2 import QtWidgets, QtGui, QtCore
            from PySide2.QtCore import Qt
            QAction = QtWidgets.QAction
            QStringListModel = QtGui.QStringListModel
            print("PySide2 imports successful (Nuke 11-15)")
        else:
            from PySide6 import QtWidgets, QtGui, QtCore
            from PySide6.QtCore import Qt
            QAction = QtGui.QAction  # In PySide6, QAction is in QtGui
            QStringListModel = QtCore.QStringListModel  # In PySide6, QStringListModel is in QtCore
            print("PySide6 imports successful (Nuke 16+)")
            
        # Test creating instances
        action = QAction("Test Action")
        model = QStringListModel()
        print("QAction and QStringListModel instances created successfully")
        
        return True
        
    except ImportError as e:
        print(f"Import error: {e}")
        return False
    except Exception as e:
        print(f"Error creating Qt objects: {e}")
        return False

def test_knobscripter_import():
    """Test KnobScripter can be imported"""
    try:
        import KnobScripter
        print("KnobScripter imported successfully")
        return True
    except ImportError as e:
        print(f"KnobScripter import failed: {e}")
        return False
    except Exception as e:
        print(f"KnobScripter error: {e}")
        return False

def test_regex_compatibility():
    """Test QRegExp compatibility"""
    try:
        if nuke.NUKE_VERSION_MAJOR < 16:
            from PySide2.QtCore import QRegExp
            regex = QRegExp("test")
            print("QRegExp works (PySide2)")
        else:
            try:
                from PySide6.QtCore import QRegularExpression as QRegExp
                regex = QRegExp("test")
                print("QRegularExpression works as QRegExp (PySide6)")
            except ImportError:
                from PySide6.QtCore import QRegExp
                regex = QRegExp("test")
                print("QRegExp works (PySide6 fallback)")
        return True
    except Exception as e:
        print(f"Regex compatibility error: {e}")
        return False

def main():
    """Run all compatibility tests"""
    print("=" * 60)
    print("KnobScripter Nuke 16 Compatibility Test")
    print("=" * 60)
    
    tests = [
        ("Qt Imports", test_qt_imports),
        ("Regex Compatibility", test_regex_compatibility),
        ("KnobScripter Import", test_knobscripter_import),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        try:
            if test_func():
                passed += 1
            else:
                print(f"{test_name} failed")
        except Exception as e:
            print(f"{test_name} crashed: {e}")

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed}/{total} tests passed")
    if passed == total:
        print("All tests passed! KnobScripter should work with this Nuke version.")
    else:
        print("Some tests failed. Check the output above for details.")
    print("=" * 60)

if __name__ == "__main__":
    main()
