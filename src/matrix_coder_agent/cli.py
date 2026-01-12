"""
Command-line interface for the Matrix Coder Agent.

This module provides the CLI entry point for running the agent in either
interactive mode or with direct command-line prompts.
"""

import argparse
import logging
from matrix_coder_agent.agent import MatrixCoderAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the Matrix Coder Agent CLI."""
    parser = argparse.ArgumentParser(
        description='Matrix Coder Agent - Autonomous development agent using AWS Bedrock'
    )
    parser.add_argument(
        '-q', '--query',
        type=str,
        help='Run a single query and exit (instead of interactive mode)'
    )
    parser.add_argument(
        '-m', '--model',
        type=str,
        default=None,
        help='Bedrock model ID to use (e.g., us.anthropic.claude-sonnet-4-5-20250929-v1:0)'
    )

    args = parser.parse_args()

    logger.info("Starting Matrix Coder Agent")

    try:
        # Create agent with optional model parameter
        logger.debug(f"Creating MatrixCoderAgent instance with model={args.model}")
        agent = MatrixCoderAgent(model_id=args.model)
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}", exc_info=True)
        print(f"Error initializing agent: {e}")
        return 1

    # If query is provided via -q flag, run it and exit
    if args.query:
        logger.info(f"Running single query mode")
        try:
            response = agent(args.query)
            print(f"\nAgent: {response}\n")
            return 0
        except Exception as e:
            logger.error(f"Error running query: {e}", exc_info=True)
            print(f"\nError: {e}\n")
            return 1

    # Otherwise, run interactive mode
    logger.info("Starting interactive mode")
    print("Matrix Coder Agent - Interactive Mode")
    print("Type 'quit', 'exit', or 'q' to exit\n")

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

    return 0


if __name__ == "__main__":
    exit(main())
