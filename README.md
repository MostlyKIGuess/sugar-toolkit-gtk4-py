# sugar-toolkit-gtk4-py

A modern GTK4 port of the Sugar Toolkit for Python activities.

## Project Status

This project is a ground-up reimplementation of the Sugar Toolkit using GTK4 and modern Python practices. We're maintaining compatibility with Sugar's core concepts while leveraging GTK4's improved APIs.

## Component Status

| Component | Status | Module | Description |
|-----------|--------|---------|-------------|
| **XoColor** | Done | `sugar.graphics` | Color handling with Sugar's standard palette |
| **Activity** | Done | `sugar.activity` | Base activity class with GTK4 window management |
| **SimpleActivity** | Done | `sugar.activity` | Quick-start activity template |
| **Alert** | In Works | `sugar.graphics` | Dialog system for user notifications |
| **Icon** | In Works | `sugar.graphics` | Sugar-style icon handling |
| **Style** | In Works | `sugar.graphics` | Sugar visual styling constants |
| **Window** | In Works | `sugar.graphics` | Enhanced window management |
| **ToolbarBox** | In Works | `sugar.graphics` | Activity toolbar container |

- More to be Added!



## Installation

### From Source
```bash
git clone https://github.com/sugarlabs/sugar-toolkit-gtk4-py.git
cd sugar-toolkit-gtk4-py
pip install -e .
```

### Development Setup
```bash
make install-dev
```

## Quick Start

```python
from sugar.activity import SimpleActivity
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

class MyActivity(SimpleActivity):
    def __init__(self):
        super().__init__()
        
        # Your activity code here
        label = Gtk.Label(label="Hello, Welcome GTK4!")
        self.set_canvas(label)

def main():
    """Run the activity with proper GTK4 application lifecycle."""
    app = Gtk.Application(application_id='org.sugarlabs.TestActivity')
    
    def on_activate(app):
        activity = MyActivity()
        app.add_window(activity)
        activity.present()
    
    app.connect('activate', on_activate)
    return app.run()

if __name__ == '__main__':
    main()
```

## Development

### Running Tests
```bash
make test
```

### Running with Coverage
```bash
make test-coverage
```

### Code Formatting
```bash
make format
```


### Building Package
```bash
make build
```

### Running Examples
```bash
make example
```

## Makefile Usage

The project includes a comprehensive Makefile with targets for all development, testing, and packaging workflows. Use `make help` to see all available targets.

### Installation and Setup
```bash
make install          # Install package in development mode
make install-dev      # Install with development dependencies
make dev-setup        # Complete development environment setup
```

### Testing and Quality Assurance
```bash
make test             # Run all tests
make test-coverage    # Run tests with HTML coverage report
make format           # Format code with black
make format-check     # Check code formatting without changes
make dev-test         # Run full development test suite
```

### Building and Packaging
```bash
make build            # Build wheel and source distributions
make dist             # Alias for build
make tarball          # Create source tarball
make check            # Verify package integrity with twine
make dev-build        # Clean, build, and check package
```

### Publishing
```bash
make upload-test      # Upload to Test PyPI
make upload           # Upload to production PyPI
```

### Utilities
```bash
make clean            # Remove build artifacts and cache files
make example          # Run the basic activity example
make test-toolkit     # Test toolkit installation (python -m sugar)
make ci-test          # Simulate complete CI pipeline locally
make help             # Show all available targets with descriptions
```

### Development Workflow Examples

**Setting up for development:**
```bash
make dev-setup        # Install everything needed
make test             # Verify setup works
```

**Before committing changes:**
```bash
make dev-test         # Run full test suite with formatting checks
```

**Creating a release:**
```bash
make dev-build        # Clean build and verify package integrity
make tarball          # Create source distribution
make check            # Final verification before upload
```

**Testing the complete CI workflow locally:**
```bash
make ci-test          # Runs the full CI pipeline simulation
```



## Requirements

- Python 3.8+
- GTK4
- PyGObject 3.42+
- GObject Introspection


## License

LGPL-2.1-or-later
