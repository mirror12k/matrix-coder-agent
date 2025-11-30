"""
Strands Bedrock Agent - Autonomous development agent using AWS Bedrock and Strands SDK.

This package provides a fully autonomous development and program solving agent
built on the Strands framework with AWS Bedrock backend.
"""

from .agent import StrandsFileAgent, AutoApprovalHook
from .prompts import DEVELOPMENT_AGENT_SYSTEM_PROMPT

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "StrandsFileAgent",
    "AutoApprovalHook",
    "DEVELOPMENT_AGENT_SYSTEM_PROMPT",
]
