# Typing Extensions

This project is a branch of <a target="_blank" rel="noopener" href="https://pypi.org/project/typing-extensions/">typing-extensions</a> on <a href="https://www.qpython.org">QPython</a>.

## Overview

The typing_extensions module serves two related purposes:

Enable use of new type system features on older Python versions. For example, typing.TypeGuard is new in Python 3.10, but typing_extensions allows users on previous Python versions to use it too.
Enable experimentation with new type system PEPs before they are accepted and added to the typing module.
typing_extensions is treated specially by static type checkers such as mypy and pyright. Objects defined in typing_extensions are treated the same way as equivalent forms in typing.

typing_extensions uses Semantic Versioning. The major version will be incremented only for backwards-incompatible changes. Therefore, it's safe to depend on typing_extensions like this: typing_extensions >=x.y, <(x+1), where x.y is the first version that includes all features you need.
