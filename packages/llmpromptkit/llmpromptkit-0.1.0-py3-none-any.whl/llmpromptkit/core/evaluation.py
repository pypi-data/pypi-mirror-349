import os
import json
import datetime
from typing import Dict, List, Optional, Any, Callable, Union, Awaitable
import asyncio
from .prompt_manager import PromptManager, Prompt

class EvaluationMetric:
    """Base class for evaluation metrics."""
    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description or ""

    def compute(self, generated_output: str, expected_output: Optional[str] = None, **kwargs) -> float:
        """Compute the metric. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement compute method")

class ExactMatchMetric(EvaluationMetric):
    """Evaluates exact match between generated and expected output."""
    def __init__(self):
        super().__init__("exact_match", "Exact match between generated and expected output")

    def compute(self, generated_output: str, expected_output: Optional[str] = None, **kwargs) -> float:
        """Return 1.0 if generated matches expected exactly, 0.0 otherwise."""
        if not expected_output:
            return 0.0
        return 1.0 if generated_output.strip() == expected_output.strip() else 0.0

class ContainsKeywordsMetric(EvaluationMetric):
    """Evaluates if the generated output contains specified keywords."""
    def __init__(self, keywords: List[str], case_sensitive: bool = False):
        super().__init__(
            "contains_keywords", 
            f"Check if output contains keywords: {', '.join(keywords)}"
        )
        self.keywords = keywords
        self.case_sensitive = case_sensitive

    def compute(self, generated_output: str, expected_output: Optional[str] = None, **kwargs) -> float:
        """Return percentage of keywords found in the output."""
        if not self.keywords:
            return 0.0

        if not self.case_sensitive:
            generated_output = generated_output.lower()
            keywords = [k.lower() for k in self.keywords]
        else:
            keywords = self.keywords

        matches = sum(1 for k in keywords if k in generated_output)
        return matches / len(keywords)

class LengthMetric(EvaluationMetric):
    """Evaluates if the generated output length is within the desired range."""
    def __init__(self, min_length: Optional[int] = None, max_length: Optional[int] = None, target_length: Optional[int] = None):
        description = "Evaluate output length"
        if target_length is not None:
            description = f"Evaluate if output length is close to {target_length} characters"
        elif min_length is not None and max_length is not None:
            description = f"Evaluate if output length is between {min_length} and {max_length} characters"
        elif min_length is not None:
            description = f"Evaluate if output length is at least {min_length} characters"
        elif max_length is not None:
            description = f"Evaluate if output length is at most {max_length} characters"
        
        super().__init__("length", description)
        self.min_length = min_length
        self.max_length = max_length
        self.target_length = target_length

    def compute(self, generated_output: str, expected_output: Optional[str] = None, **kwargs) -> float:
        """Return score based on length conditions."""
        length = len(generated_output)
        
        if self.target_length is not None:
            # Score inversely proportional to the distance from target
            max_distance = self.target_length  # Normalize to a max distance
            distance = abs(length - self.target_length)
            return max(0, 1 - (distance / max_distance))
        
        # Check if within bounds
        within_min = self.min_length is None or length >= self.min_length
        within_max = self.max_length is None or length <= self.max_length
        
        if within_min and within_max:
            return 1.0
        elif within_min and self.max_length:
            # Over max length, calculate proportional penalty
            return max(0, 1 - ((length - self.max_length) / self.max_length))
        elif within_max and self.min_length:
            # Under min length, calculate proportional penalty
            return max(0, length / self.min_length)
        return 0.0

class Evaluator:
    """Manages evaluation metrics and evaluation runs."""
    def __init__(self, prompt_manager: PromptManager):
        self.prompt_manager = prompt_manager
        self.metrics: Dict[str, EvaluationMetric] = {}
        self.storage_path = os.path.join(prompt_manager.storage_path, "evaluations")
        os.makedirs(self.storage_path, exist_ok=True)
        
        # Register built-in metrics
        self.register_metric(ExactMatchMetric())
        self.register_metric(ContainsKeywordsMetric(["important", "critical", "necessary"]))
        self.register_metric(LengthMetric(min_length=50, max_length=500))

    def register_metric(self, metric: EvaluationMetric) -> None:
        """Register a new evaluation metric."""
        self.metrics[metric.name] = metric

    def get_metric(self, name: str) -> Optional[EvaluationMetric]:
        """Get a registered metric by name."""
        return self.metrics.get(name)

    def list_metrics(self) -> List[EvaluationMetric]:
        """List all registered metrics."""
        return list(self.metrics.values())

    async def evaluate_prompt(
        self,
        prompt_id: str,
        inputs: List[Dict[str, Any]],
        llm_callback: Callable[[str, Dict[str, Any]], Union[str, Awaitable[str]]],
        expected_outputs: Optional[List[Optional[str]]] = None,
        metric_names: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Evaluate a prompt with the given inputs and metrics."""
        prompt = self.prompt_manager.get(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt with ID {prompt_id} not found")

        # Use all registered metrics if none specified
        if not metric_names:
            metrics_to_use = list(self.metrics.values())
        else:
            metrics_to_use = [self.get_metric(name) for name in metric_names if self.get_metric(name)]

        if not metrics_to_use:
            raise ValueError("No valid metrics specified")

        # Ensure expected_outputs is the same length as inputs
        if expected_outputs is None:
            expected_outputs = [None] * len(inputs)
        elif len(expected_outputs) != len(inputs):
            raise ValueError("Expected outputs must be the same length as inputs")

        results = []
        for i, (input_vars, expected) in enumerate(zip(inputs, expected_outputs)):
            # Render the prompt
            rendered_prompt = prompt.render(**input_vars)
            
            # Generate output
            if asyncio.iscoroutinefunction(llm_callback):
                output = await llm_callback(rendered_prompt, input_vars)
            else:
                output = llm_callback(rendered_prompt, input_vars)
            
            # Compute metrics
            metrics_results = {}
            for metric in metrics_to_use:
                metrics_results[metric.name] = metric.compute(output, expected, **input_vars)
            
            results.append({
                "input": input_vars,
                "output": output,
                "expected": expected,
                "metrics": metrics_results
            })

        # Aggregate metrics
        aggregated_metrics = {}
        for metric in metrics_to_use:
            values = [r["metrics"][metric.name] for r in results]
            aggregated_metrics[metric.name] = sum(values) / len(values) if values else 0

        evaluation_result = {
            "prompt_id": prompt_id,
            "prompt_version": prompt.version,
            "num_samples": len(inputs),
            "aggregated_metrics": aggregated_metrics,
            "individual_results": results
        }

        # Save evaluation result
        timestamp = datetime.datetime.now().isoformat().replace(":", "-").replace(".", "-")
        file_path = os.path.join(self.storage_path, f"eval_{prompt_id}_{timestamp}.json")
        with open(file_path, "w") as f:
            json.dump(evaluation_result, f, indent=2)

        return evaluation_result