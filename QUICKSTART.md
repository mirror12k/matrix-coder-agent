# Quick Start Guide

Get up and running with Matrix Coder Agent in minutes.

## Installation

```bash
pip install matrix-coder-agent
```

## Basic Usage

### Command Line

```bash
matrix-coder-agent
```

Then interact with natural language:
```
> Create a Python calculator with add, subtract, multiply, divide functions
> Read the config.json file and tell me what's in it
> Write a hello world program in hello.py
```

### Python Code

```python
from matrix_coder_agent import StrandsFileAgent

# Create agent
agent = StrandsFileAgent()

# Run a task
response = agent("Create a simple web server in Python")
print(response)
```

## Configuration

### AWS Setup

1. **Configure AWS Credentials**:
   ```bash
   aws configure
   ```

2. **Enable Bedrock Model Access**:
   - Go to AWS Console → Amazon Bedrock
   - Navigate to "Model access"
   - Request access to Claude models

3. **Verify Access**:
   ```bash
   aws bedrock list-foundation-models --region us-east-1 --by-provider anthropic
   ```

### Custom Configuration

```python
from matrix_coder_agent import StrandsFileAgent

# Different region
agent = StrandsFileAgent(region_name="us-west-2")

# Different model
agent = StrandsFileAgent(
    model_id="anthropic.claude-3-5-sonnet-20241022-v2:0"
)

# Disable auto-approval (require human confirmation)
agent = StrandsFileAgent(auto_approve=False)

# Custom system prompt
agent = StrandsFileAgent(
    system_prompt="You are a Python expert. Focus on clean, well-tested code."
)
```

## Common Use Cases

### 1. Building Programs

```python
agent = StrandsFileAgent()
response = agent("""
Create a command-line todo list application in Python with:
- Add tasks
- List tasks
- Mark tasks as complete
- Delete tasks
- Save/load from JSON file
""")
```

### 2. Code Review

```python
agent = StrandsFileAgent(
    system_prompt="You are a code reviewer. Focus on bugs and best practices."
)
response = agent("Review the code in app.py and suggest improvements")
```

### 3. Debugging

```python
agent = StrandsFileAgent()
response = agent("Find and fix the bug in calculator.py that's causing division errors")
```

### 4. Documentation

```python
agent = StrandsFileAgent(
    system_prompt="You are a documentation expert. Write clear, comprehensive docs."
)
response = agent("Add docstrings and comments to all functions in utils.py")
```

## Troubleshooting

### AWS Credentials Error

```bash
# Test credentials
aws sts get-caller-identity

# If fails, reconfigure
aws configure
```

### Bedrock Access Denied

- Request model access in AWS Bedrock console
- Check IAM permissions include `bedrock:InvokeModel`

### Import Error

```bash
# Reinstall package
pip install --upgrade matrix-coder-agent

# Or install from source
git clone https://github.com/mirror12k/matrix-coder-agent.git
cd matrix-coder-agent
pip install -e .
```

## Available Tools

The agent has access to these tools:

- **file_read** - Read file contents
- **file_write** - Write content to files
- **shell** - Execute shell commands
- **editor** - Advanced file editing
- **think** - Structured reasoning
- **journal** - Maintain context across sessions

## Environment Variables

```bash
# AWS Configuration
export AWS_REGION=us-east-1
export AWS_DEFAULT_REGION=us-east-1

# Bypass tool consent (for autonomous operation)
export BYPASS_TOOL_CONSENT=true
```

## Next Steps

- Read the [full documentation](README.md)
- Check out [example use cases](README.md#advanced-configuration)
- Learn about [system prompts](README.md#system-prompt)
- Understand [auto-approval mode](README.md#auto-approval-mode)
- Review [security considerations](README.md#security-notes)

## Support

- **Issues**: https://github.com/mirror12k/matrix-coder-agent/issues
- **Documentation**: https://github.com/mirror12k/matrix-coder-agent#readme
- **Strands SDK**: https://strandsagents.com/

## Quick Tips

1. **Be Specific**: Clear instructions get better results
   - ❌ "Make a program"
   - ✅ "Create a Python program that reads CSV files and calculates the average of numeric columns"

2. **Iterative Development**: Break complex tasks into steps
   ```python
   agent("Create a basic Flask app")
   agent("Add a /health endpoint")
   agent("Add error handling")
   ```

3. **Use Context**: The agent maintains conversation history
   ```python
   agent("Read config.json")
   agent("Update the database_url setting to localhost")  # Knows about config.json
   ```

4. **Autonomous Mode**: Default is fully autonomous - perfect for batch processing
   ```python
   agent = StrandsFileAgent(auto_approve=True)  # Default
   ```

5. **Human-in-Loop**: Enable for critical operations
   ```python
   agent = StrandsFileAgent(auto_approve=False)
   ```

## License

MIT License - See [LICENSE](LICENSE) for details.
