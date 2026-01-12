"""
Matrix Coder Agent - Autonomous development agent using AWS Bedrock and Strands SDK.

This package provides a fully autonomous development and program solving agent
built on the Strands framework with AWS Bedrock backend.
"""

from .agent import MatrixCoderAgent
from .prompts import DEVELOPMENT_AGENT_SYSTEM_PROMPT

__version__ = "0.2.1"
