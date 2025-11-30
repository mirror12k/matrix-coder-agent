"""
Strands Agent with File Read and Write Tools using AWS Bedrock

This agent provides basic file system operations using the Strands framework
and AWS Bedrock for Claude model invocation.
"""

import os
import logging
import boto3
from strands import Agent
from strands.models import BedrockModel
from strands.hooks import BeforeToolCallEvent, HookProvider, HookRegistry
from strands_tools import file_read, file_write, shell, editor, think, journal
from prompts import DEVELOPMENT_AGENT_SYSTEM_PROMPT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set botocore and related AWS loggers to INFO level
logging.getLogger('botocore').setLevel(logging.INFO)
logging.getLogger('boto3').setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.INFO)


os.environ["BYPASS_TOOL_CONSENT"] = "true"

class AutoApprovalHook(HookProvider):
    def register_hooks(self, registry, **kwargs):
        registry.add_callback(BeforeToolCallEvent, self.approve)
    def approve(self, event):
        return


class StrandsFileAgent:
    """A Strands agent with file read and write capabilities using AWS Bedrock."""

    def __init__(self, region_name: str = None, model_id: str = None, streaming: bool = True, system_prompt: str = None, auto_approve: bool = True):
        """
        Initialize the Strands agent with AWS Bedrock.

        Args:
            region_name: AWS region for Bedrock. If not provided, will check
                        AWS_REGION, AWS_DEFAULT_REGION, DEFAULT_BEDROCK_REGION
                        environment variables, then default to us-east-1.
            model_id: Bedrock model ID. Defaults to Claude 3.5 Sonnet.
            streaming: Enable streaming responses. Defaults to True.
            system_prompt: Custom system prompt. If not provided, uses the default
                          development agent system prompt from prompts.py.
            auto_approve: Automatically approve all tool calls without human intervention.
                         Defaults to True for autonomous operation.
        """
        # Resolve region from environment variables or default
        if region_name is None:
            region_name = 'us-east-1'

        logger.debug(f"Region resolved to: {region_name}")

        # Configure default model
        if model_id is None:
            model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

        logger.debug(f"Model ID set to: {model_id}")

        # Store configuration
        self.region_name = region_name
        self.model_id = model_id

        print(f"Initializing Strands agent with:")
        print(f"  Region: {region_name}")
        print(f"  Model: {model_id}")

        logger.info(f"Initializing agent with region={region_name}, model={model_id}, streaming={streaming}")

        # Create a boto3 session with explicit region
        self.session = boto3.Session(region_name=region_name)
        logger.debug(f"Created boto3 session with region: {self.session.region_name}")

        # Configure Bedrock model with explicit boto session
        # This ensures the region is properly respected
        logger.debug(f"Creating BedrockModel with boto_session (region={self.session.region_name}), model_id={model_id}, streaming={streaming}")
        self.model = BedrockModel(
            boto_session=self.session,
            model_id=model_id,
            streaming=streaming
        )
        logger.debug("BedrockModel created successfully")

        # Use provided system prompt or default to development agent prompt
        if system_prompt is None:
            system_prompt = DEVELOPMENT_AGENT_SYSTEM_PROMPT
            logger.debug("Using default DEVELOPMENT_AGENT_SYSTEM_PROMPT")
        else:
            logger.debug(f"Using custom system prompt (length: {len(system_prompt)} chars)")

        # Initialize Strands agent with file tools and system prompt
        logger.debug("Initializing Strands Agent with tools: file_read, file_write, shell, editor, think, journal")

        self.agent = Agent(
            model=self.model,
            tools=[file_read, file_write, shell, editor, think, journal],
            system_prompt=system_prompt,
            hooks=[]
        )
        logger.info("Strands agent initialized successfully")

    def run(self, query: str) -> str:
        """
        Run the agent with a query.

        Args:
            query: The user's query or instruction

        Returns:
            The agent's response as a string
        """
        logger.debug(f"Running agent with query: {query[:100]}{'...' if len(query) > 100 else ''}")
        try:
            result = self.agent(query)
            logger.debug(f"Agent returned result of type: {type(result).__name__}")

            # Convert AgentResult to string
            if hasattr(result, 'output'):
                response = str(result.output)
            else:
                response = str(result)

            logger.debug(f"Agent response (length: {len(response)} chars)")
            return response
        except Exception as e:
            logger.error(f"Error running agent: {e}", exc_info=True)
            raise

    def __call__(self, query: str) -> str:
        """
        Allow the agent to be called directly.

        Args:
            query: The user's query or instruction

        Returns:
            The agent's response
        """
        return self.run(query)


def main():
    """Example usage of the Strands agent with AWS Bedrock."""
    logger.info("Starting Strands File Agent interactive mode")
    try:
        # Create agent (uses current AWS credentials)
        logger.debug("Creating StrandsFileAgent instance")
        agent = StrandsFileAgent()
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}", exc_info=True)
        print(f"Error initializing agent: {e}")
        return

    # Interactive loop
    while True:
        try:
            user_input = input("> ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                logger.info("User requested exit")
                print("Goodbye!")
                break

            if not user_input:
                continue

            logger.debug(f"User input: {user_input}")
            # Run agent
            response = agent(user_input)
            print(f"\nAgent: {response}\n")

        except KeyboardInterrupt:
            logger.info("Interrupted by user (Ctrl+C)")
            print("\n\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error in interactive loop: {e}", exc_info=True)
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
