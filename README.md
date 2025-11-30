# Strands File Agent (AWS Bedrock)

A Strands agent with file read and write capabilities, built using the Strands SDK with AWS Bedrock backend.

## Features

- **Strands SDK Integration**: Built on the official Strands agents framework
- **AWS Bedrock Backend**: Uses AWS Bedrock for Claude model invocation
- **File Operations**: Read and write files using built-in Strands tools
- **Automatic Agentic Loop**: Strands handles tool use and multi-turn conversations automatically
- **Streaming Responses**: Real-time output from Claude
- **IAM Authentication**: Uses current AWS credentials from environment

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
├── agent.py           # Strands agent wrapper class
├── main.py           # Entry point for interactive mode
├── requirements.txt  # Python dependencies
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

## Configuration

### Default Settings

- **Model**: `anthropic.claude-sonnet-4-5-v2:0`
- **Region**: `us-east-1`
- **Streaming**: Enabled
- **Tools**: `file_read`, `file_write`

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
