# DetectIQ
DetectIQ is an AI-powered security rule management platform that helps create, analyze, and optimize detection rules across multiple security platforms. It is primarily used as a Python library (`detectiq.core` module) for integration into your own scripts and tools. See examples in the [examples](examples/) directory for more information.
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: LGPL v2.1](https://img.shields.io/badge/License-LGPL_v2.1-blue.svg)](https://www.gnu.org/licenses/lgpl-2.1)
[![Status: Alpha](https://img.shields.io/badge/Status-Alpha-red.svg)]()
- [Quickstart](#quickstart)
- [Current Features](#current-features)
- [Road Map](#road-map)
- [Using as a Package](#using-as-a-package)
- [Environment Configuration](#environment-configuration)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Support & Community](#support--community)
- [Acknowledgments](#acknowledgments)

> ⚠️ **IMPORTANT DISCLAIMER**
> 
> This project is currently a **Proof of Concept** and is under active development:
> - Features are incomplete and actively being developed
> - Bugs and breaking changes are expected
> - Project structure and APIs may change significantly
> - Documentation may be outdated or incomplete
> - Not recommended for production use at this time
> - Security features are still being implemented
> 
> We welcome all feedback and contributions, but please use at your own risk!

## Quickstart
To get started with using DetectIQ as a library:

**Step 1.** Clone the repository.
```bash
git clone https://github.com/AttackIQ/DetectIQ.git
cd DetectIQ
```

**Step 2.** Set your environment variables (using [`.env.example`](.env.example) as a template for API keys, e.g., `OPENAI_API_KEY`).
```bash
cp .env.example .env
# Edit .env with your API keys
```

**Step 3.** Install the package and its dependencies, preferably in a virtual environment.
```bash
# Using poetry (recommended)
poetry install --all-extras

# Or using pip
# pip install .
```

**Step 4.** Explore the examples in the `examples/` directory to see how to use the library.

## Current Features
### AI-Powered Detection 
- Create and optimize detection rules using OpenAI's LLM models
- Intelligent rule suggestions based on context and best practices
- Automated rule validation and testing 
- Upload malware samples and PCAP files for static analysis, automatically adding context for YARA and Snort rule creation
- LLM Rule creation analysis and detection logic returned in the rule creation response

### Rule Repository Integration 
- Enhanced by community-tested repositories:
  - SigmaHQ Core Ruleset
  - YARA-Forge Rules
  - Snort3 Community Ruleset
- Automatically check and update repositories with rule changes
- Vectorize rules for efficient similarity comparison for more context-aware rule creation engine

### Static Analysis Integration 
- Automated file analysis for YARA rules
- PCAP analysis for Snort rule creation
- Implicit log analysis for Sigma rule optimization (Explicit Analysis Coming Soon)

### Multi-Platform Integration 
- Automatic Sigma rule translation to various SIEM queries leveraging advanced AI models.
- Seamlessly create Splunk Enterprise Security correlation rules from Sigma rules

## Road Map
- [ ] Custom/local LLM models, embeddings, and vector stores
- [ ] More integrations with SIEMs such as Elastic and Microsoft XDR
- [ ] Explicit log analysis for Sigma rule optimization
- [ ] Rule testing and validation
- [ ] Rule searching, e.g. "Do I have a rule in place that can detect this?"
- [ ] Deployment tracking and workflow automation
- [ ] Project refactoring for production readiness
- [ ] Rule management without OpenAI requirements
- [ ] More non-webapp examples

## Using as a Package

DetectIQ can be installed as a Python package from PyPI:

```bash
pip install detectiq
```

This allows you to leverage DetectIQ's detection rule management capabilities in your own Python projects:

```python
import asyncio
from typing import cast
import os

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "your-api-key"

from langchain.schema.language_model import BaseLanguageModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from detectiq.core.llm.yara_rules import YaraLLM
from detectiq.core.llm.toolkits.base import create_rule_agent
from detectiq.core.llm.toolkits.yara_toolkit import YaraToolkit

async def main():
    # Initialize LLMs
    agent_llm = cast(BaseLanguageModel, ChatOpenAI(temperature=0, model="gpt-4o"))
    rule_creation_llm = cast(BaseLanguageModel, ChatOpenAI(temperature=0, model="gpt-4o"))
    
    # Initialize YARA tools
    yara_llm = YaraLLM(
        embedding_model=OpenAIEmbeddings(model="text-embedding-3-small"),
        agent_llm=agent_llm,
        rule_creation_llm=rule_creation_llm,
        rule_dir="./rules",
        vector_store_dir="./vectorstore",
    )
    
    # Create agent
    yara_agent = create_rule_agent(
        rule_type="yara",
        vectorstore=yara_llm.vectordb,
        rule_creation_llm=yara_llm.rule_creation_llm,
        agent_llm=yara_llm.agent_llm,
        toolkit_class=YaraToolkit,
    )
    
    # Create a rule
    result = await yara_agent.ainvoke({"input": "Create a YARA rule to detect ransomware"})
    print(result.get("output"))

if __name__ == "__main__":
    asyncio.run(main())
```

For more detailed examples, see the [examples](examples/) directory.

For instructions on publishing the package to PyPI, see [PUBLISHING.md](PUBLISHING.md).

## Environment Configuration

DetectIQ uses environment variables for configuration, primarily for API keys like `OPENAI_API_KEY`. A comprehensive example with documentation is provided in [.env.example](.env.example).

To configure the application for use with examples or your own scripts:

1. Copy the example file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your specific settings:
   ```bash
   # Required for LLM functionality
   OPENAI_API_KEY=your-api-key-here
   
   # Optional configurations
   LOG_LEVEL=INFO
   DEBUG=False
   ```

3. The same `.env` file can be used for both the web application and the examples.

## Development

DetectIQ includes a comprehensive Makefile to assist with development, testing, and publishing tasks.

### Prerequisites

Before development, ensure you have:

1. Python 3.9+ installed
2. Poetry installed
3. Required development dependencies:
   ```bash
   make install-dev
   ```

This will install all development dependencies, including:
- Testing tools (pytest)
- Code quality tools (black, ruff)
- Package building tools (build, twine)
- Keyring backends (keyrings.alt) for token management

### Makefile Commands

To view all available commands:

```bash
make help
```

#### Common Development Commands

```bash
# Installation
make install              # Install package with all extras

# Code quality
make format               # Format Python files
make test                 # Run tests with coverage

# Package management
make update               # Update dependencies using Poetry
make version              # Display current version
make version-patch        # Bump patch version (0.0.X)
make version-minor        # Bump minor version (0.X.0)
make version-major        # Bump major version (X.0.0)

# PyPI publishing
make build                # Build package for PyPI
make publish              # Publish to PyPI (after versioning and building)
```

For more details on publishing the package, see [PUBLISHING.md](PUBLISHING.md).

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project uses multiple licenses:
- Core Project: LGPL v2.1
- Sigma Rules: Detection Rule License (DRL)
- YARA Rules: YARAForge License
- Snort Rules: GPL with VRT License

## Support & Community
- Join our [SigmaHQ Discord](https://discord.gg/27r98bMv6c) for discussions
- Report issues via GitHub Issues

## Acknowledgments
- SigmaHQ Community
- YARA-Forge Contributors
- Snort Community
- OpenAI for GPT-4o Integration
