"""
Strands Agent with File Read and Write Tools using AWS Bedrock

This agent provides basic file system operations using the Strands framework
and AWS Bedrock for Claude model invocation.
"""

import os
import boto3
from strands import Agent
from strands.models import BedrockModel
from strands_tools import file_read, file_write


class StrandsFileAgent:
    """A Strands agent with file read and write capabilities using AWS Bedrock."""

    def __init__(self, region_name: str = None, model_id: str = None, streaming: bool = True):
        """
        Initialize the Strands agent with AWS Bedrock.

        Args:
            region_name: AWS region for Bedrock. If not provided, will check
                        AWS_REGION, AWS_DEFAULT_REGION, DEFAULT_BEDROCK_REGION
                        environment variables, then default to us-east-1.
            model_id: Bedrock model ID. Defaults to Claude Opus 4.
            streaming: Enable streaming responses. Defaults to True.
        """
        # Resolve region from environment variables or default
        if region_name is None:
            region_name = 'us-east-1'

        # Configure default model
        if model_id is None:
            model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

        # Store configuration
        self.region_name = region_name
        self.model_id = model_id

        print(f"Initializing Strands agent with:")
        print(f"  Region: {region_name}")
        print(f"  Model: {model_id}")

        # Create a boto3 session with explicit region
        self.session = boto3.Session(region_name=region_name)

        # Configure Bedrock model with explicit boto session
        # This ensures the region is properly respected
        self.model = BedrockModel(
            boto_session=self.session,
            model_id=model_id,
            streaming=streaming
        )

        # Initialize Strands agent with file tools
        self.agent = Agent(
            model=self.model,
            tools=[file_read, file_write]
        )

    def run(self, query: str) -> str:
        """
        Run the agent with a query.

        Args:
            query: The user's query or instruction

        Returns:
            The agent's response
        """
        return self.agent(query)

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
    print("Strands File Agent (AWS Bedrock) initialized!")
    print("\nExample usage:")
    print("  - 'Read the file test.txt'")
    print("  - 'Write Hello World to output.txt'")
    print("  - Type 'quit' to exit\n")

    try:
        # Create agent (uses current AWS credentials)
        agent = StrandsFileAgent()
    except Exception as e:
        print(f"Error initializing agent: {e}")
        print("Make sure you have AWS credentials configured and Bedrock access enabled.")
        return

    # Interactive loop
    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if not user_input:
                continue

            # Run agent
            response = agent(user_input)
            print(f"\nAgent: {response}\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
