"""
LLMPromptKit - A comprehensive LLM Prompt Management System

LLMPromptKit is a Python library that provides tools for managing, versioning,
testing, and evaluating prompts for Large Language Models.

Features:
- Prompt management with versioning
- A/B testing for prompt optimization
- Evaluation framework with customizable metrics
- Command-line interface for easy integration
"""

from .core.prompt_manager import PromptManager, Prompt
from .core.version_control import VersionControl, PromptVersion
from .core.testing import PromptTesting, TestCase, TestResult, ABTestResult
from .core.evaluation import Evaluator, EvaluationMetric, ExactMatchMetric, ContainsKeywordsMetric, LengthMetric
from .utils.metrics import create_default_metrics_set
from .utils.templating import PromptTemplate, template_registry

__version__ = "0.1.0"
__all__ = [
    "PromptManager",
    "Prompt",
    "VersionControl",
    "PromptVersion",
    "PromptTesting",
    "TestCase",
    "TestResult",
    "ABTestResult",
    "Evaluator",
    "EvaluationMetric",
    "ExactMatchMetric",
    "ContainsKeywordsMetric",
    "LengthMetric",
    "create_default_metrics_set",
    "PromptTemplate",
    "template_registry"
]