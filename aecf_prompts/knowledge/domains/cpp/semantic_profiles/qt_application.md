---
profile_id: cpp_qt_application
title: C++ Qt Application Development
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-15
profile_type: framework
stack_nodes:
  - cpp
requires: []
precedence: 80
fallback_mode: warn_continue
compatibility:
  - cpp
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=qt
  - keyword=qml
  - keyword=qwidget
  - keyword=qobject
  - manifest=.pro
max_lines_per_section: 6
tags:
  - cpp
  - qt
  - gui
  - desktop
  - qml
---

LAST_REVIEW: 2026-03-15
OWNER SEACHAD

## STACK

C++ Qt development uses the Qt framework for cross-platform GUI and systems applications with signals/slots, QObject hierarchy, and QML for declarative UI.

## ARCHITECTURE RULES

- Separate business logic from UI code; keep models, services, and views in distinct modules.
- Use the Model-View pattern (QAbstractItemModel) for data-driven UI components.
- Keep QObject ownership hierarchy explicit; parent-child relationships manage lifetime.
- Use dependency injection for services instead of relying on global singletons.
- Separate QML UI from C++ backend through clearly defined Q_PROPERTY and Q_INVOKABLE interfaces.

## DESIGN PATTERNS

- Signals and slots for decoupled component communication.
- QAbstractItemModel subclasses for list, tree, and table data presentation.
- Q_PROPERTY with NOTIFY signal for QML data binding.
- Plugin architecture using Qt plugin system for extensibility.
- Worker threads with signal/slot connections for non-blocking UI.

## CODING RULES

- Use `Q_OBJECT` macro in all QObject-derived classes that declare signals or slots.
- Prefer `connect()` with function pointer syntax over string-based SIGNAL/SLOT macros.
- Use smart pointers for non-QObject resources; rely on Qt parent-child for QObjects.
- Keep slot implementations short; delegate complex logic to service classes.
- Use `QScopedPointer` or `std::unique_ptr` for resources that do not fit the parent-child model.

## SECURITY RULES

- Validate all user input from forms, network, and file loading before processing.
- Sanitize QML and JavaScript content loaded from external sources.
- Review plugin loading paths for untrusted code injection.
- Protect credential storage and network communication with Qt's SSL/TLS support.

## TESTING RULES

- Use Qt Test framework for unit tests with `QSignalSpy` for signal verification.
- Test models with `QAbstractItemModelTester` to verify model contract compliance.
- Cover signal/slot connections, property bindings, and error handling paths.
- Separate GUI tests from business logic tests; test logic without instantiating widgets.
- Include one regression test for thread-safety in signal/slot cross-thread communication.

## COMMON MISTAKES

- Forgetting `Q_OBJECT` macro, causing moc to skip the class and signals/slots to fail silently.
- Managing QObject lifetime with smart pointers while also setting a parent (double-free).
- Blocking the main event loop with long-running operations instead of using worker threads.
- Using string-based SIGNAL/SLOT syntax that fails silently at runtime.
- Tight coupling between QML and C++ internals without proper interface contracts.

## AECF AUDIT CHECKS

- Verify business logic is testable without UI widget instantiation.
- Verify QObject lifetime management is consistent (parent-child or smart pointer, not both).
- Verify signals/slots use compile-time-checked connection syntax.
- Verify models conform to Qt model contract (verified with QAbstractItemModelTester).
- Verify non-blocking patterns are used for long-running operations.
