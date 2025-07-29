# Pilot Probing

A framework for LLM (Large Language Model) tracing and evaluation.

## 🚀 Features

- Trace and analyze LLM interactions
- Monitor model performance and behavior
- Gather metrics for model evaluation
- Support for multiple LLM providers
- Extensible architecture for custom evaluation methods

## 📋 Requirements

- Python 3.10+
- Dependencies listed in pyproject.toml

## 🔧 Installation

### From uv (recommended)

```bash
uv pip install pilot-probing
```

For development:

```bash
uv pip install -e ".[dev]"
```


## 🧹 Code Quality

This project uses several tools to ensure code quality:

- **mypy**: Type checking
- **ruff**: Linting

Run all quality checks:

```bash

# Check types
mypy src/

# Lint code
ruff .
```

## 📚 Documentation

Detailed documentation is available in the `docs/` directory.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Run the quality checks and tests
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

