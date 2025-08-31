# KnobScripter Nuke 16 Compatibility Fixes

## Overview
This document outlines the compatibility issues found and fixes applied to make KnobScripter work with Nuke 16, which uses PySide6 instead of PySide2.

## FIXED ISSUES

### 1. Qt Framework Version Compatibility
**Problem**: Code only handled PySide (Nuke < 11) and PySide2 (Nuke ≥ 11), but Nuke 16 uses PySide6.

**Solution**: Updated import pattern in all files to handle PySide6:
```python
try:
    if nuke.NUKE_VERSION_MAJOR < 11:
        from PySide import QtCore, QtGui, QtGui as QtWidgets
        from PySide.QtCore import Qt
        QAction = QtGui.QAction
        QStringListModel = QtGui.QStringListModel
    elif nuke.NUKE_VERSION_MAJOR < 16:
        from PySide2 import QtWidgets, QtGui, QtCore
        from PySide2.QtCore import Qt
        QAction = QtWidgets.QAction
        QStringListModel = QtGui.QStringListModel
    else:
        from PySide6 import QtWidgets, QtGui, QtCore
        from PySide6.QtCore import Qt
        QAction = QtGui.QAction  # In PySide6, QAction is in QtGui
        QStringListModel = QtCore.QStringListModel  # In PySide6, moved to QtCore
except ImportError:
    from Qt import QtCore, QtGui, QtWidgets
    # Compatibility fallbacks
    try:
        QAction = QtGui.QAction
    except AttributeError:
        QAction = QtWidgets.QAction
    try:
        QStringListModel = QtCore.QStringListModel
    except AttributeError:
        QStringListModel = QtGui.QStringListModel
```

**Files Updated**:
- knob_scripter.py
- utils.py
- ksscripteditormain.py
- widgets.py
- ksscripteditor.py
- snippets.py
- script_output.py
- pythonhighlighter.py
- blinkhighlighter.py
- keywordhotbox.py
- findreplace.py
- dialogs.py
- codegallery.py
- prefs.py
- letItSnow.py

### 2. QAction Location Change (CRITICAL FIX)
**Problem**: In PySide6, `QAction` moved from `QtWidgets` to `QtGui`.

**Error**: `AttributeError: module 'PySide6.QtWidgets' has no attribute 'QAction'`

**Solution**: Updated all QAction references to use compatibility variable:
- Changed `QtWidgets.QAction` → `QAction` (with proper import compatibility)
- Added QAction compatibility to import blocks

**Files Updated**:
- knob_scripter.py (16 instances fixed)

### 3. QRegExp Compatibility
**Problem**: PySide6 deprecated QRegExp in favor of QRegularExpression.

**Solution**: Added compatibility layer:
```python
# In highlighter files
try:
    QRegExp = QtCore.QRegularExpression  # PySide6
except AttributeError:
    QRegExp = QtCore.QRegExp  # PySide/PySide2
```

**Files Updated**:
- pythonhighlighter.py
- blinkhighlighter.py

### 4. QStringListModel Location Change
**Problem**: `QStringListModel` moved from `QtGui` to `QtCore` in PySide6.

**Solution**: Added compatibility handling in imports and existing try/except blocks.

**Files Updated**:
- ksscripteditormain.py (already had try/except, improved with compatibility imports)

### 5. Tab Stop Methods Renamed (CRITICAL FIX)
**Problem**: In PySide6, tab stop methods were renamed:
- `setTabStopWidth()` → `setTabStopDistance()`
- `tabStopWidth()` → `tabStopDistance()`

**Error**: `AttributeError: 'ScriptOutputWidget' object has no attribute 'setTabStopWidth'. Did you mean: 'setTabStopDistance'?`

**Solution**: Added compatibility wrapper functions:
```python
def setTabStopWidth_compat(widget, width):
    if hasattr(widget, 'setTabStopDistance'):
        widget.setTabStopDistance(width)  # PySide6
    elif hasattr(widget, 'setTabStopWidth'):
        widget.setTabStopWidth(width)  # PySide2

def tabStopWidth_compat(widget):
    if hasattr(widget, 'tabStopDistance'):
        return widget.tabStopDistance()  # PySide6
    elif hasattr(widget, 'tabStopWidth'):
        return widget.tabStopWidth()  # PySide2
    return 80  # Default fallback
```

**Files Updated**:
- knob_scripter.py (2 instances fixed)

### 6. Font Metrics Methods (CRITICAL FIX)
**Problem**: `QFontMetrics.horizontalAdvance()` was introduced in Qt 5.11, replacing `width()`.

**Solution**: Added compatibility wrapper:
```python
def fontMetrics_width_compat(font_metrics, text):
    if hasattr(font_metrics, 'horizontalAdvance'):
        return font_metrics.horizontalAdvance(text)  # Qt 5.11+
    elif hasattr(font_metrics, 'width'):
        return font_metrics.width(text)  # Older Qt
    return len(text) * 8  # Fallback estimate
```

**Files Updated**:
- knob_scripter.py (1 instance fixed)
- ksscripteditor.py (1 instance fixed)

## REMAINING ISSUES TO ADDRESS

### 1. Layout.setMargin() Deprecation
**Problem**: `setMargin()` method was deprecated in favor of `setContentsMargins()`.

**Current Usage** (16 occurrences):
```python
layout.setMargin(0)  # Deprecated
```

**Should be**:
```python
layout.setContentsMargins(0, 0, 0, 0)  # Modern approach
```

**Files Affected**:
- widgets.py (5 occurrences)
- snippets.py (2 occurrences)
- codegallery.py (2 occurrences)
- prefs.py (5 occurrences)
- keywordhotbox.py (1 occurrence)
- findreplace.py (1 occurrence)

### 2. String Escape Sequences
**Problem**: Invalid escape sequences in regex patterns.

**Examples**:
```python
'\+', '\*', '\%'  # Should be raw strings or properly escaped
```

**Should be**:
```python
r'\+', r'\*', r'\%'  # Raw strings
# or
'\\+', '\\*', '\\%'  # Properly escaped
```

## 🔧 RECOMMENDATIONS FOR FULL COMPATIBILITY

### Quick Fix Implementation
To fully resolve all compatibility issues, implement these additional changes:

1. **Create a compatibility helper module** (`qt_compat.py`):
```python
import nuke

try:
    if nuke.NUKE_VERSION_MAJOR < 11:
        from PySide import QtCore, QtGui, QtGui as QtWidgets
        from PySide.QtCore import Qt
        QRegExp = QtCore.QRegExp
        QStringListModel = QtGui.QStringListModel
    elif nuke.NUKE_VERSION_MAJOR < 16:
        from PySide2 import QtWidgets, QtGui, QtCore
        from PySide2.QtCore import Qt
        QRegExp = QtCore.QRegExp
        QStringListModel = QtGui.QStringListModel
    else:
        from PySide6 import QtWidgets, QtGui, QtCore
        from PySide6.QtCore import Qt
        QRegExp = QtCore.QRegularExpression
        QStringListModel = QtCore.QStringListModel
except ImportError:
    from Qt import QtCore, QtGui, QtWidgets
    try:
        QRegExp = QtCore.QRegularExpression
        QStringListModel = QtCore.QStringListModel
    except AttributeError:
        QRegExp = QtCore.QRegExp
        QStringListModel = QtGui.QStringListModel

# Layout compatibility
def setLayoutMargin(layout, margin):
    if hasattr(layout, 'setContentsMargins'):
        layout.setContentsMargins(margin, margin, margin, margin)
    else:
        layout.setMargin(margin)  # Fallback for older Qt versions
```

2. **Replace all setMargin() calls** with the compatibility function.

3. **Fix string escape sequences** by converting to raw strings.

## 🧪 TESTING

After implementing fixes, test the following functionality:
- [ ] Script editor opens without errors
- [ ] Syntax highlighting works (Python and Blink)
- [ ] Code completion functions
- [ ] All dialog boxes display properly
- [ ] File operations work correctly
- [ ] Preferences panel functions
- [ ] Code gallery functions
- [ ] Snippet functionality works

## 📝 VERSION INFO

- **KnobScripter Version**: 3.1 (Jan 15 2024)
- **Target Nuke Versions**: 16+
- **Qt Framework**: PySide6
- **Compatibility**: Maintains backward compatibility with Nuke 11-15 (PySide2) and Nuke <11 (PySide)
