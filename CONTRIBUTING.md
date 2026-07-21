# Contributing to CyberLab Pro

## How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

## Plugin Development
Plugins must have a `run(parent, db, logger, config)` function.
See `plugins/hello_world.py` for an example.

## Code Style
- Python 3.8+
- Tkinter for GUI
- No external dependencies
- Follow existing module patterns
