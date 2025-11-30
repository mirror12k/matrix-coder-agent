# Strands File Agent (AWS Bedrock)

A Strands agent with file read and write capabilities, built using the Strands SDK with AWS Bedrock backend.

## Features

- **Strands SDK Integration**: Built on the official Strands agents framework
- **AWS Bedrock Backend**: Uses AWS Bedrock for Claude model invocation
- **File Operations**: Read and write files using built-in Strands tools
- **Extended Tool Set**: Includes shell, editor, think, and journal tools for comprehensive development tasks
- **Automatic Agentic Loop**: Strands handles tool use and multi-turn conversations automatically
- **Streaming Responses**: Real-time output from Claude
- **IAM Authentication**: Uses current AWS credentials from environment
- **Development-Focused System Prompt**: Pre-configured as an autonomous development and program solving agent
- **Auto-Approval Mode**: Fully autonomous operation without human intervention (enabled by default)

## Prerequisites

- Python 3.8+
- AWS account with Bedrock access
- AWS credentials configured (IAM role, environment variables, or AWS CLI)
- Access to Claude Sonnet 4.5 model in AWS Bedrock

## AWS Setup

### 1. Enable Bedrock Model Access

Before using this agent, you need to request access to Claude models in AWS Bedrock:

1. Go to AWS Console > Amazon Bedrock
2. Navigate to "Model access" in the left sidebar
3. Click "Request model access"
4. Select "Anthropic Claude" models, including Claude Sonnet 4.5
5. Submit the request and wait for approval (usually instant)

### 2. AWS Credentials

The agent uses standard AWS credential resolution in this order:

1. **IAM Role** (if running on EC2, ECS, Lambda, etc.)
2. **Environment variables** (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
3. **AWS CLI credentials** (`~/.aws/credentials`)
4. **EC2 Instance Metadata** (if on EC2)

No additional configuration needed if you already have AWS credentials set up.

## Installation

1. Navigate to the project directory:
```bash
cd /app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

This installs:
- `strands-agents` - The Strands SDK
- `strands-agents-tools` - Pre-built tools including file operations
- `boto3` - AWS SDK for Bedrock access

## Usage

### Interactive Mode

Run the agent in interactive mode:

```bash
python main.py
```

or

```bash
python agent.py
```

### Example Commands

Once the agent is running, you can use natural language to perform file operations:

- **Read a file**:
  ```
  Read the contents of config.json
  ```

- **Write to a file**:
  ```
  Write "Hello, World!" to greeting.txt
  ```

- **Complex operations**:
  ```
  Read the data.txt file and write its contents to backup.txt
  ```

The Strands SDK automatically handles:
- Tool selection and invocation
- Multi-turn conversations
- Error handling
- Response formatting

### Programmatic Usage

You can also use the agent programmatically in your Python code:

```python
from agent import StrandsFileAgent

# Initialize the agent (uses current AWS credentials)
agent = StrandsFileAgent(region_name="us-east-1")

# Run a task
response = agent("Read the file example.txt")
print(response)

# Or call directly
response = agent("Write Hello to test.txt")
print(response)
```

### Advanced Configuration

Customize the agent with different models or settings:

```python
from agent import StrandsFileAgent

# Use a different Bedrock model
agent = StrandsFileAgent(
    region_name="us-west-2",
    model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
    streaming=True
)

# Disable streaming
agent = StrandsFileAgent(streaming=False)

# Custom system prompt
agent = StrandsFileAgent(
    system_prompt="You are a specialized code reviewer. Focus on security and performance."
)

# Disable auto-approval (require human intervention for tool calls)
agent = StrandsFileAgent(auto_approve=False)
```

### Auto-Approval Mode

By default, the agent runs in **autonomous mode** with auto-approval enabled. This means:

- The agent can execute tool calls (file operations, shell commands, etc.) without waiting for human approval
- No interrupts are raised during tool execution
- The agent operates completely autonomously to complete tasks

This is ideal for automated workflows, CI/CD pipelines, and scenarios where you trust the agent to operate independently.

**Disabling Auto-Approval:**

If you want human-in-the-loop control where the agent requests approval before executing tools:

```python
agent = StrandsFileAgent(auto_approve=False)
```

With auto-approval disabled, the agent will pause and request confirmation before executing potentially dangerous operations (like shell commands or file writes).

**How It Works:**

The auto-approval system uses a `BeforeToolCallEvent` hook that automatically approves all tool calls. When enabled, the hook logs each tool call but allows it to proceed without interruption.

### System Prompt

The agent comes with a comprehensive system prompt (defined in `prompts.py`) that configures it as an autonomous development and program solving agent. The prompt instructs the agent to:

- Analyze requirements and plan solutions methodically
- Write clean, maintainable code with proper error handling
- Test implementations thoroughly and iterate on failures
- Use file tools effectively to read, write, and modify code
- Work step-by-step through development tasks
- Debug issues by analyzing errors and applying fixes

**Viewing the System Prompt:**
```python
from prompts import DEVELOPMENT_AGENT_SYSTEM_PROMPT
print(DEVELOPMENT_AGENT_SYSTEM_PROMPT)
```

**Customizing the System Prompt:**

You can provide your own system prompt when initializing the agent:

```python
custom_prompt = """You are a data analysis assistant.
Use file tools to read datasets and write analysis results.
Focus on statistical accuracy and clear visualizations."""

agent = StrandsFileAgent(system_prompt=custom_prompt)
```

### Using Strands Directly

For more control, use the Strands SDK directly:

```python
from strands import Agent
from strands.models import BedrockModel
from strands_tools import file_read, file_write

# Configure Bedrock model
model = BedrockModel(
    model_id="anthropic.claude-sonnet-4-5-v2:0",
    region_name="us-east-1",
    streaming=True
)

# Create agent with tools
agent = Agent(model=model, tools=[file_read, file_write])

# Run queries
response = agent("Read config.json and tell me what's in it")
print(response)
```

## Architecture

The agent is built using the Strands framework:

### Components

- **Strands SDK** (`strands-agents`):
  - Handles the agentic loop automatically
  - Manages tool invocation based on Claude's decisions
  - Provides model abstractions for various providers

- **Strands Tools** (`strands-agents-tools`):
  - `file_read`: Reads file contents with error handling
  - `file_write`: Writes content to files with confirmation
  - Tools are automatically discovered and invoked by the agent

- **AWS Bedrock Integration**:
  - `BedrockModel` class from Strands SDK
  - Uses boto3 under the hood
  - Handles authentication via AWS credentials
  - Supports streaming responses

### How It Works

1. User provides a natural language query
2. Strands SDK sends query to Claude via Bedrock
3. Claude analyzes the query and decides which tools to use
4. Strands automatically invokes the selected tools
5. Tool results are sent back to Claude
6. Claude generates a natural language response
7. Response is returned to the user

All of this happens automatically - you don't need to implement the agentic loop yourself.

## Project Structure

```
/app/
├── agent.py              # Strands agent wrapper class
├── main.py               # Entry point for interactive mode
├── prompts.py            # System prompts for the agent
├── requirements.txt      # Python dependencies
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Configuration

### Default Settings

- **Model**: `anthropic.claude-3-5-sonnet-20240620-v1:0`
- **Region**: `us-east-1`
- **Streaming**: Enabled
- **Auto-Approval**: Enabled (autonomous operation)
- **Tools**: `file_read`, `file_write`, `shell`, `editor`, `think`, `journal`

### Available Bedrock Models

Strands SDK supports various Claude models on Bedrock:
- `anthropic.claude-sonnet-4-5-v2:0` (default)
- `anthropic.claude-3-5-sonnet-20241022-v2:0`
- `anthropic.claude-3-5-sonnet-20240620-v1:0`
- Other Claude models available in your region

## Adding More Tools

The Strands tools package includes many pre-built tools. To add more:

```python
from strands import Agent
from strands.models import BedrockModel
from strands_tools import file_read, file_write, shell, web_search

model = BedrockModel(
    model_id="anthropic.claude-sonnet-4-5-v2:0",
    region_name="us-east-1"
)

agent = Agent(
    model=model,
    tools=[file_read, file_write, shell, web_search]
)
```

Available tools in `strands-agents-tools`:
- **File Operations**: `file_read`, `file_write`, `editor`
- **System**: `shell`, `execute_python`
- **Web**: `web_search`, `web_scrape`, `http_request`
- **And many more...**

See the [Strands Tools README](https://github.com/strands-agents/tools) for a complete list.

## Security Notes

- The agent has read/write access to the file system
- Be cautious with file paths and permissions
- Uses AWS IAM for authentication and authorization
- Always validate user inputs in production environments
- Consider adding path restrictions for production use
- The `shell` tool (if added) can execute arbitrary commands

### Required AWS Permissions

Minimum IAM permissions needed:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:*::foundation-model/anthropic.claude-*"
    }
  ]
}
```

## Troubleshooting

- **AWS Credentials Error**: Ensure AWS credentials are configured via IAM role, environment variables, or AWS CLI
- **Bedrock Access Denied**: Request model access in AWS Bedrock console
- **Region Error**: Verify Claude is available in your selected region (try us-east-1 or us-west-2)
- **Model Not Found**: Ensure you're using the correct model ID and have access enabled
- **Import Error**: Run `pip install -r requirements.txt`
- **File Permission Errors**: Check file/directory permissions

### Testing AWS Credentials

```bash
aws sts get-caller-identity
```

This should return your AWS account information if credentials are configured correctly.

### Verifying Bedrock Access

```bash
aws bedrock list-foundation-models --region us-east-1 --by-provider anthropic
```

This lists available Claude models in your account.

## Cost Considerations

AWS Bedrock charges per token:
- Input tokens
- Output tokens

Claude Sonnet 4.5 pricing varies by region. Monitor usage in AWS Cost Explorer and set up billing alerts as needed.

## Resources

- [Strands SDK Documentation](https://github.com/strands-agents/sdk-python)
- [Strands Tools Documentation](https://github.com/strands-agents/tools)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Anthropic Claude Models](https://www.anthropic.com/claude)

## License

MIT License - Feel free to modify and use as needed.
