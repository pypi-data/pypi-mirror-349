import os
import json
import uuid
import datetime
import asyncio
from typing import Dict, List, Optional, Any, Callable, Union, Awaitable, Tuple
from .prompt_manager import Prompt, PromptManager

class TestCase:
    """Represents a test case for a prompt."""
    def __init__(
        self,
        prompt_id: str,
        input_vars: Dict[str, Any],
        expected_output: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None
    ):
        self.id = str(uuid.uuid4())[:10]
        self.prompt_id = prompt_id
        self.input_vars = input_vars
        self.expected_output = expected_output
        self.name = name or f"Test case {self.id}"
        self.description = description or ""
        self.created_at = datetime.datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert test case to dictionary."""
        return {
            "id": self.id,
            "prompt_id": self.prompt_id,
            "input_vars": self.input_vars,
            "expected_output": self.expected_output,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TestCase":
        """Create test case from dictionary."""
        test_case = cls(
            prompt_id=data["prompt_id"],
            input_vars=data["input_vars"],
            expected_output=data.get("expected_output"),
            name=data.get("name"),
            description=data.get("description")
        )
        test_case.id = data["id"]
        test_case.created_at = data["created_at"]
        return test_case


class TestResult:
    """Represents the result of a test case execution."""
    def __init__(
        self,
        test_case_id: str,
        prompt_id: str,
        prompt_version: int,
        output: str,
        passed: Optional[bool] = None,
        metrics: Optional[Dict[str, float]] = None
    ):
        self.id = str(uuid.uuid4())[:10]
        self.test_case_id = test_case_id
        self.prompt_id = prompt_id
        self.prompt_version = prompt_version
        self.output = output
        self.passed = passed
        self.metrics = metrics or {}
        self.created_at = datetime.datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert test result to dictionary."""
        return {
            "id": self.id,
            "test_case_id": self.test_case_id,
            "prompt_id": self.prompt_id,
            "prompt_version": self.prompt_version,
            "output": self.output,
            "passed": self.passed,
            "metrics": self.metrics,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TestResult":
        """Create test result from dictionary."""
        return cls(
            test_case_id=data["test_case_id"],
            prompt_id=data["prompt_id"],
            prompt_version=data["prompt_version"],
            output=data["output"],
            passed=data.get("passed"),
            metrics=data.get("metrics", {})
        )


class ABTestResult:
    """Represents the result of an A/B test."""
    def __init__(
        self,
        prompt_a_id: str,
        prompt_b_id: str,
        prompt_a_version: int,
        prompt_b_version: int,
        metrics_a: Dict[str, float],
        metrics_b: Dict[str, float],
        winner: Optional[str] = None
    ):
        self.id = str(uuid.uuid4())[:10]
        self.prompt_a_id = prompt_a_id
        self.prompt_b_id = prompt_b_id
        self.prompt_a_version = prompt_a_version
        self.prompt_b_version = prompt_b_version
        self.metrics_a = metrics_a
        self.metrics_b = metrics_b
        self.winner = winner
        self.created_at = datetime.datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert A/B test result to dictionary."""
        return {
            "id": self.id,
            "prompt_a_id": self.prompt_a_id,
            "prompt_b_id": self.prompt_b_id,
            "prompt_a_version": self.prompt_a_version,
            "prompt_b_version": self.prompt_b_version,
            "metrics_a": self.metrics_a,
            "metrics_b": self.metrics_b,
            "winner": self.winner,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ABTestResult":
        """Create A/B test result from dictionary."""
        return cls(
            prompt_a_id=data["prompt_a_id"],
            prompt_b_id=data["prompt_b_id"],
            prompt_a_version=data["prompt_a_version"],
            prompt_b_version=data["prompt_b_version"],
            metrics_a=data["metrics_a"],
            metrics_b=data["metrics_b"],
            winner=data.get("winner")
        )


class PromptTesting:
    """Manages testing for prompts."""
    def __init__(self, prompt_manager: PromptManager):
        self.prompt_manager = prompt_manager
        self.storage_path = os.path.join(prompt_manager.storage_path, "tests")
        os.makedirs(self.storage_path, exist_ok=True)
        
        # Storage paths
        self.test_cases_path = os.path.join(self.storage_path, "test_cases")
        self.test_results_path = os.path.join(self.storage_path, "test_results")
        self.ab_test_results_path = os.path.join(self.storage_path, "ab_test_results")
        
        os.makedirs(self.test_cases_path, exist_ok=True)
        os.makedirs(self.test_results_path, exist_ok=True)
        os.makedirs(self.ab_test_results_path, exist_ok=True)
        
        self.test_cases: Dict[str, TestCase] = {}
        self.test_results: Dict[str, TestResult] = {}
        self.ab_test_results: Dict[str, ABTestResult] = {}
        
        self._load_test_cases()
        self._load_test_results()
        self._load_ab_test_results()

    def _load_test_cases(self) -> None:
        """Load test cases from storage."""
        for filename in os.listdir(self.test_cases_path):
            if filename.endswith(".json"):
                with open(os.path.join(self.test_cases_path, filename), "r") as f:
                    data = json.load(f)
                    test_case = TestCase.from_dict(data)
                    self.test_cases[test_case.id] = test_case

    def _load_test_results(self) -> None:
        """Load test results from storage."""
        for filename in os.listdir(self.test_results_path):
            if filename.endswith(".json"):
                with open(os.path.join(self.test_results_path, filename), "r") as f:
                    data = json.load(f)
                    test_result = TestResult.from_dict(data)
                    self.test_results[test_result.id] = test_result

    def _load_ab_test_results(self) -> None:
        """Load A/B test results from storage."""
        for filename in os.listdir(self.ab_test_results_path):
            if filename.endswith(".json"):
                with open(os.path.join(self.ab_test_results_path, filename), "r") as f:
                    data = json.load(f)
                    ab_test_result = ABTestResult.from_dict(data)
                    self.ab_test_results[ab_test_result.id] = ab_test_result

    def _save_test_case(self, test_case: TestCase) -> None:
        """Save test case to storage."""
        file_path = os.path.join(self.test_cases_path, f"{test_case.id}.json")
        with open(file_path, "w") as f:
            json.dump(test_case.to_dict(), f, indent=2)

    def _save_test_result(self, test_result: TestResult) -> None:
        """Save test result to storage."""
        file_path = os.path.join(self.test_results_path, f"{test_result.id}.json")
        with open(file_path, "w") as f:
            json.dump(test_result.to_dict(), f, indent=2)

    def _save_ab_test_result(self, ab_test_result: ABTestResult) -> None:
        """Save A/B test result to storage."""
        file_path = os.path.join(self.ab_test_results_path, f"{ab_test_result.id}.json")
        with open(file_path, "w") as f:
            json.dump(ab_test_result.to_dict(), f, indent=2)

    def create_test_case(
        self,
        prompt_id: str,
        input_vars: Dict[str, Any],
        expected_output: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> TestCase:
        """Create a test case for a prompt."""
        test_case = TestCase(
            prompt_id=prompt_id,
            input_vars=input_vars,
            expected_output=expected_output,
            name=name,
            description=description
        )
        self.test_cases[test_case.id] = test_case
        self._save_test_case(test_case)
        return test_case

    def get_test_case(self, test_case_id: str) -> Optional[TestCase]:
        """Get a test case by ID."""
        return self.test_cases.get(test_case_id)

    def list_test_cases(self, prompt_id: Optional[str] = None) -> List[TestCase]:
        """List test cases, optionally filtered by prompt ID."""
        if prompt_id:
            return [tc for tc in self.test_cases.values() if tc.prompt_id == prompt_id]
        return list(self.test_cases.values())

    def delete_test_case(self, test_case_id: str) -> bool:
        """Delete a test case by ID."""
        if test_case_id in self.test_cases:
            del self.test_cases[test_case_id]
            file_path = os.path.join(self.test_cases_path, f"{test_case_id}.json")
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        return False

    async def run_test_case(
        self,
        test_case_id: str,
        llm_callback: Callable[[str, Dict[str, Any]], Union[str, Awaitable[str]]],
        metrics_callbacks: Optional[List[Callable[[str, str], Dict[str, float]]]] = None
    ) -> TestResult:
        """Run a test case with the given LLM callback."""
        test_case = self.get_test_case(test_case_id)
        if not test_case:
            raise ValueError(f"Test case with ID {test_case_id} not found")

        prompt = self.prompt_manager.get(test_case.prompt_id)
        if not prompt:
            raise ValueError(f"Prompt with ID {test_case.prompt_id} not found")

        # Render the prompt with the input variables
        rendered_prompt = prompt.render(**test_case.input_vars)

        # Call the LLM with the rendered prompt
        if asyncio.iscoroutinefunction(llm_callback):
            output = await llm_callback(rendered_prompt, test_case.input_vars)
        else:
            output = llm_callback(rendered_prompt, test_case.input_vars)

        # Determine if the test passed
        passed = None
        if test_case.expected_output:
            passed = output.strip() == test_case.expected_output.strip()

        # Calculate metrics if callbacks are provided
        metrics = {}
        if metrics_callbacks:
            for metric_callback in metrics_callbacks:
                metrics.update(metric_callback(output, test_case.expected_output or ""))

        # Create and save the test result
        test_result = TestResult(
            test_case_id=test_case.id,
            prompt_id=test_case.prompt_id,
            prompt_version=prompt.version,
            output=output,
            passed=passed,
            metrics=metrics
        )
        self.test_results[test_result.id] = test_result
        self._save_test_result(test_result)

        return test_result

    async def run_test_cases(
        self,
        prompt_id: str,
        llm_callback: Callable[[str, Dict[str, Any]], Union[str, Awaitable[str]]],
        metrics_callbacks: Optional[List[Callable[[str, str], Dict[str, float]]]] = None
    ) -> List[TestResult]:
        """Run all test cases for a prompt."""
        test_cases = self.list_test_cases(prompt_id)
        results = []

        for test_case in test_cases:
            result = await self.run_test_case(test_case.id, llm_callback, metrics_callbacks)
            results.append(result)

        return results

    async def run_ab_test(
        self,
        prompt_a_id: str,
        prompt_b_id: str,
        llm_callback: Callable[[str, Dict[str, Any]], Union[str, Awaitable[str]]],
        metrics_callbacks: List[Callable[[str, str], Dict[str, float]]],
        test_cases: Optional[List[str]] = None
    ) -> ABTestResult:
        """Run an A/B test with two prompts."""
        prompt_a = self.prompt_manager.get(prompt_a_id)
        prompt_b = self.prompt_manager.get(prompt_b_id)

        if not prompt_a or not prompt_b:
            raise ValueError("Both prompts must exist")

        # Get test cases to use
        if test_cases:
            # Use specified test cases
            test_case_objs = [self.get_test_case(tc_id) for tc_id in test_cases]
            test_case_objs = [tc for tc in test_case_objs if tc]
        else:
            # Use all test cases for prompt A
            test_case_objs = self.list_test_cases(prompt_a_id)

        if not test_case_objs:
            raise ValueError("No test cases found for the A/B test")

        # Run test cases for both prompts
        results_a = []
        results_b = []

        for test_case in test_case_objs:
            # Create a copy of the test case for prompt B
            if test_case.prompt_id != prompt_b_id:
                test_case_b = self.create_test_case(
                    prompt_id=prompt_b_id,
                    input_vars=test_case.input_vars,
                    expected_output=test_case.expected_output,
                    name=f"Copy of {test_case.name} for B",
                    description=test_case.description
                )
            else:
                test_case_b = test_case

            # Run the test cases
            result_a = await self.run_test_case(test_case.id, llm_callback, metrics_callbacks)
            result_b = await self.run_test_case(test_case_b.id, llm_callback, metrics_callbacks)

            results_a.append(result_a)
            results_b.append(result_b)

        # Calculate aggregate metrics
        metrics_a = self._aggregate_metrics([r.metrics for r in results_a])
        metrics_b = self._aggregate_metrics([r.metrics for r in results_b])

        # Determine winner
        winner = self._determine_winner(metrics_a, metrics_b)

        # Create and save the A/B test result
        ab_test_result = ABTestResult(
            prompt_a_id=prompt_a_id,
            prompt_b_id=prompt_b_id,
            prompt_a_version=prompt_a.version,
            prompt_b_version=prompt_b.version,
            metrics_a=metrics_a,
            metrics_b=metrics_b,
            winner=winner
        )
        self.ab_test_results[ab_test_result.id] = ab_test_result
        self._save_ab_test_result(ab_test_result)

        return ab_test_result

    def _aggregate_metrics(self, metrics_list: List[Dict[str, float]]) -> Dict[str, float]:
        """Aggregate metrics from multiple test results."""
        if not metrics_list:
            return {}

        aggregated = {}
        for key in metrics_list[0].keys():
            values = [m.get(key, 0) for m in metrics_list]
            aggregated[key] = sum(values) / len(values)  # Simple average

        return aggregated

    def _determine_winner(self, metrics_a: Dict[str, float], metrics_b: Dict[str, float]) -> Optional[str]:
        """Determine winner of A/B test based on metrics."""
        if not metrics_a or not metrics_b:
            return None

        # Assume higher values are better for all metrics
        a_wins = 0
        b_wins = 0

        for key in metrics_a.keys():
            if key in metrics_b:
                if metrics_a[key] > metrics_b[key]:
                    a_wins += 1
                elif metrics_b[key] > metrics_a[key]:
                    b_wins += 1

        if a_wins > b_wins:
            return "A"
        elif b_wins > a_wins:
            return "B"
        else:
            return None  # Tie

    def get_test_results(self, test_case_id: Optional[str] = None, prompt_id: Optional[str] = None) -> List[TestResult]:
        """Get test results, optionally filtered by test case ID or prompt ID."""
        results = list(self.test_results.values())
        
        if test_case_id:
            results = [r for r in results if r.test_case_id == test_case_id]
        
        if prompt_id:
            results = [r for r in results if r.prompt_id == prompt_id]
        
        return sorted(results, key=lambda r: r.created_at, reverse=True)

    def get_ab_test_results(self, prompt_id: Optional[str] = None) -> List[ABTestResult]:
        """Get A/B test results, optionally filtered by prompt ID."""
        results = list(self.ab_test_results.values())
        
        if prompt_id:
            results = [r for r in results if r.prompt_a_id == prompt_id or r.prompt_b_id == prompt_id]
        
        return sorted(results, key=lambda r: r.created_at, reverse=True)
