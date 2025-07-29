# Vibehacker Metasploit MCP

A FastMCP-based interface for Metasploit Framework, enabling AI agents to interact with Metasploit capabilities.

## Prerequisites

- Python 3.10+
- Metasploit Framework
- uv (Python package manager)

## Setup with uv

This project uses [uv](https://github.com/astral-sh/uv) for dependency management. uv is a fast, reliable Python package installer and resolver.

### Installing uv

If you don't have uv installed:

```bash
pip install uv
```

### Setting up the project

1. Clone the repository:
```bash
git clone https://github.com/foolsec/vibehacker_metasploit_mcp.git
cd vibehacker_metasploit_mcp
```

2. Create and activate a virtual environment with uv:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv pip install -e .
```

### Running Metasploit RPC Server

Before running the application, start the Metasploit RPC server:

```bash
# Full configuration with all options
msfrpcd -P kalipassword -S -a 127.0.0.1 -p 55553
```

Or use the simpler command to start the RPC server in the background on the default port (55553):

```bash
msfrpcd -P your_password
```

### Environment Variables

Set the following environment variables:

```bash
export MSF_PASSWORD=kalipassword
export MSF_SERVER=127.0.0.1
export MSF_PORT=55553
```

### Running the Application

```bash
python main.py
```
or to test the tools 
```bash
mcp dev main.py
```
 
## Features

- List available Metasploit exploits
- List available payloads
- Generate payloads
- Run exploits against targets
- Scan targets
- Manage active sessions
- Send commands to sessions

## License

See the [LICENSE](LICENSE) file for details.
