#!/usr/bin/env python3
"""
Script to run the CrewAI agent.
"""

import logging
from dotenv import load_dotenv

from aiagent.core.agent import run_crew_agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

load_dotenv()

if __name__ == "__main__":
    run_crew_agent()