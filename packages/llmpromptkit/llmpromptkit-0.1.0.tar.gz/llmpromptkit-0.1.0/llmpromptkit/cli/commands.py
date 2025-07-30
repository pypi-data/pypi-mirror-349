import argparse
import sys
import os
import json
from typing import List, Optional, Dict, Any
import asyncio

from ..core.prompt_manager import PromptManager
from ..core.version_control import VersionControl
from ..core.testing import PromptTesting
from ..core.evaluation import Evaluator, ContainsKeywordsMetric, LengthMetric


class CLI:
    """Command-line interface for LLMPromptKit."""
    def __init__(self):
        self.prompt_manager = PromptManager()
        self.version_control = VersionControl(self.prompt_manager)
        self.testing = PromptTesting(self.prompt_manager)
        self.evaluator = Evaluator(self.prompt_manager)
        
        self.parser = argparse.ArgumentParser(description="LLMPromptKit - LLM Prompt Management System")
        self._setup_commands()
    
    def _setup_commands(self) -> None:
        """Set up command-line arguments."""
        subparsers = self.parser.add_subparsers(dest="command", help="Command")
        
        # Prompt commands
        prompt_parser = subparsers.add_parser("prompt", help="Prompt management")
        prompt_subparsers = prompt_parser.add_subparsers(dest="subcommand", help="Prompt subcommand")
        
        # Create prompt
        create_parser = prompt_subparsers.add_parser("create", help="Create a new prompt")
        create_parser.add_argument("name", help="Prompt name")
        create_parser.add_argument("--content", help="Prompt content")
        create_parser.add_argument("--file", help="File containing prompt content")
        create_parser.add_argument("--description", help="Prompt description")
        create_parser.add_argument("--tags", help="Comma-separated list of tags")
        
        # List prompts
        # List prompts
        list_parser = prompt_subparsers.add_parser("list", help="List prompts")
        list_parser.add_argument("--tags", help="Filter by comma-separated list of tags")
        
        # Get prompt
        get_parser = prompt_subparsers.add_parser("get", help="Get a prompt")
        get_parser.add_argument("id", help="Prompt ID")
        
        # Update prompt
        update_parser = prompt_subparsers.add_parser("update", help="Update a prompt")
        update_parser.add_argument("id", help="Prompt ID")
        update_parser.add_argument("--content", help="New prompt content")
        update_parser.add_argument("--file", help="File containing new prompt content")
        update_parser.add_argument("--name", help="New prompt name")
        update_parser.add_argument("--description", help="New prompt description")
        update_parser.add_argument("--tags", help="New comma-separated list of tags")
        
        # Delete prompt
        delete_parser = prompt_subparsers.add_parser("delete", help="Delete a prompt")
        delete_parser.add_argument("id", help="Prompt ID")
        
        # Version control commands
        version_parser = subparsers.add_parser("version", help="Version control")
        version_subparsers = version_parser.add_subparsers(dest="subcommand", help="Version subcommand")
        
        # Commit
        commit_parser = version_subparsers.add_parser("commit", help="Create a new version")
        commit_parser.add_argument("id", help="Prompt ID")
        commit_parser.add_argument("--message", help="Commit message")
        
        # List versions
        list_versions_parser = version_subparsers.add_parser("list", help="List versions")
        list_versions_parser.add_argument("id", help="Prompt ID")
        
        # Checkout
        checkout_parser = version_subparsers.add_parser("checkout", help="Checkout a version")
        checkout_parser.add_argument("id", help="Prompt ID")
        checkout_parser.add_argument("version", type=int, help="Version number")
        
        # Diff
        diff_parser = version_subparsers.add_parser("diff", help="Compare versions")
        diff_parser.add_argument("id", help="Prompt ID")
        diff_parser.add_argument("version1", type=int, help="First version")
        diff_parser.add_argument("version2", type=int, help="Second version")
        
        # Testing commands
        test_parser = subparsers.add_parser("test", help="Testing")
        test_subparsers = test_parser.add_subparsers(dest="subcommand", help="Test subcommand")
        
        # Create test case
        create_test_parser = test_subparsers.add_parser("create", help="Create a test case")
        create_test_parser.add_argument("prompt_id", help="Prompt ID")
        create_test_parser.add_argument("--input", help="JSON string of input variables")
        create_test_parser.add_argument("--input-file", help="File containing JSON input variables")
        create_test_parser.add_argument("--expected", help="Expected output")
        create_test_parser.add_argument("--expected-file", help="File containing expected output")
        create_test_parser.add_argument("--name", help="Test case name")
        create_test_parser.add_argument("--description", help="Test case description")
        
        # List test cases
        list_tests_parser = test_subparsers.add_parser("list", help="List test cases")
        list_tests_parser.add_argument("--prompt-id", help="Filter by prompt ID")
        
        # Run test case
        run_test_parser = test_subparsers.add_parser("run", help="Run a test case")
        run_test_parser.add_argument("test_id", help="Test case ID")
        run_test_parser.add_argument("--llm", help="LLM callback function to use")
        
        # Run all test cases for a prompt
        run_all_parser = test_subparsers.add_parser("run-all", help="Run all test cases for a prompt")
        run_all_parser.add_argument("prompt_id", help="Prompt ID")
        run_all_parser.add_argument("--llm", help="LLM callback function to use")
        
        # A/B test
        ab_test_parser = test_subparsers.add_parser("ab", help="Run an A/B test")
        ab_test_parser.add_argument("prompt_a", help="Prompt A ID")
        ab_test_parser.add_argument("prompt_b", help="Prompt B ID")
        ab_test_parser.add_argument("--llm", help="LLM callback function to use")
        ab_test_parser.add_argument("--test-cases", help="Comma-separated list of test case IDs")
        
        # Evaluation commands
        eval_parser = subparsers.add_parser("eval", help="Evaluation")
        eval_subparsers = eval_parser.add_subparsers(dest="subcommand", help="Evaluation subcommand")
        
        # List metrics
        list_metrics_parser = eval_subparsers.add_parser("metrics", help="List evaluation metrics")
        
        # Register metric
        register_metric_parser = eval_subparsers.add_parser("register", help="Register a custom metric")
        register_metric_parser.add_argument("name", help="Metric name")
        register_metric_parser.add_argument("--keywords", help="Keywords for ContainsKeywordsMetric")
        register_metric_parser.add_argument("--min-length", type=int, help="Minimum length for LengthMetric")
        register_metric_parser.add_argument("--max-length", type=int, help="Maximum length for LengthMetric")
        register_metric_parser.add_argument("--target-length", type=int, help="Target length for LengthMetric")
        
        # Evaluate prompt
        evaluate_parser = eval_subparsers.add_parser("run", help="Evaluate a prompt")
        evaluate_parser.add_argument("prompt_id", help="Prompt ID")
        evaluate_parser.add_argument("--inputs", help="JSON string of input variables list")
        evaluate_parser.add_argument("--inputs-file", help="File containing JSON input variables list")
        evaluate_parser.add_argument("--expected", help="JSON string of expected outputs list")
        evaluate_parser.add_argument("--expected-file", help="File containing JSON expected outputs list")
        evaluate_parser.add_argument("--metrics", help="Comma-separated list of metrics to use")
        evaluate_parser.add_argument("--llm", help="LLM callback function to use")
    
    def run(self, args: Optional[List[str]] = None) -> None:
        """Run the CLI with the given arguments."""
        args = self.parser.parse_args(args)
        
        if not args.command:
            self.parser.print_help()
            return
        
        # Handle commands
        if args.command == "prompt":
            self._handle_prompt_command(args)
        elif args.command == "version":
            self._handle_version_command(args)
        elif args.command == "test":
            self._handle_test_command(args)
        elif args.command == "eval":
            self._handle_eval_command(args)
    
    def _handle_prompt_command(self, args) -> None:
        """Handle prompt commands."""
        if not args.subcommand:
            return
        
        if args.subcommand == "create":
            # Get content from file or argument
            content = ""
            if args.file:
                with open(args.file, "r") as f:
                    content = f.read()
            elif args.content:
                content = args.content
            else:
                print("Error: Must provide either --content or --file")
                return
            
            # Parse tags
            tags = []
            if args.tags:
                tags = [tag.strip() for tag in args.tags.split(",")]
            
            # Create prompt
            prompt = self.prompt_manager.create(
                content=content,
                name=args.name,
                description=args.description,
                tags=tags
            )
            
            print(f"Created prompt with ID: {prompt.id}")
        
        elif args.subcommand == "list":
            # Parse tags
            tags = None
            if args.tags:
                tags = [tag.strip() for tag in args.tags.split(",")]
            
            # List prompts
            prompts = self.prompt_manager.list(tags)
            
            if not prompts:
                print("No prompts found")
                return
            
            # Print prompts
            print(f"Found {len(prompts)} prompts:")
            for prompt in prompts:
                tags_str = ", ".join(prompt.tags) if prompt.tags else ""
                print(f"ID: {prompt.id} | Name: {prompt.name} | Tags: {tags_str}")
        
        elif args.subcommand == "get":
            # Get prompt
            prompt = self.prompt_manager.get(args.id)
            
            if not prompt:
                print(f"Prompt with ID {args.id} not found")
                return
            
            # Print prompt
            print(f"ID: {prompt.id}")
            print(f"Name: {prompt.name}")
            print(f"Description: {prompt.description}")
            print(f"Tags: {', '.join(prompt.tags)}")
            print(f"Version: {prompt.version}")
            print(f"Created: {prompt.created_at}")
            print(f"Updated: {prompt.updated_at}")
            print("\nContent:")
            print(prompt.content)
        
        elif args.subcommand == "update":
            # Get prompt
            prompt = self.prompt_manager.get(args.id)
            
            if not prompt:
                print(f"Prompt with ID {args.id} not found")
                return
            
            # Update kwargs
            kwargs = {}
            
            if args.name:
                kwargs["name"] = args.name
            
            if args.description:
                kwargs["description"] = args.description
            
            if args.tags:
                kwargs["tags"] = [tag.strip() for tag in args.tags.split(",")]
            
            # Get content from file or argument
            if args.file:
                with open(args.file, "r") as f:
                    kwargs["content"] = f.read()
            elif args.content:
                kwargs["content"] = args.content
            
            # Update prompt
            prompt = self.prompt_manager.update(args.id, **kwargs)
            
            print(f"Updated prompt with ID: {prompt.id}")
        
        elif args.subcommand == "delete":
            # Delete prompt
            success = self.prompt_manager.delete(args.id)
            
            if success:
                print(f"Deleted prompt with ID: {args.id}")
            else:
                print(f"Prompt with ID {args.id} not found")
    
    def _handle_version_command(self, args) -> None:
        """Handle version control commands."""
        if not args.subcommand:
            return
        
        if args.subcommand == "commit":
            # Commit version
            version = self.version_control.commit(
                prompt_id=args.id,
                commit_message=args.message
            )
            
            if not version:
                print(f"Prompt with ID {args.id} not found")
                return
            
            print(f"Committed version {version.version} for prompt {args.id}")
        
        elif args.subcommand == "list":
            # List versions
            versions = self.version_control.list_versions(args.id)
            
            if not versions:
                print(f"No versions found for prompt {args.id}")
                return
            
            # Print versions
            print(f"Found {len(versions)} versions for prompt {args.id}:")
            for version in versions:
                message = version.commit_message or "No commit message"
                print(f"Version: {version.version} | Created: {version.created_at} | Message: {message}")
        
        elif args.subcommand == "checkout":
            # Checkout version
            prompt = self.version_control.checkout(
                prompt_id=args.id,
                version=args.version
            )
            
            if not prompt:
                print(f"Prompt with ID {args.id} or version {args.version} not found")
                return
            
            print(f"Checked out version {args.version} for prompt {args.id}")
        
        elif args.subcommand == "diff":
            # Diff versions
            diff = self.version_control.diff(
                prompt_id=args.id,
                version1=args.version1,
                version2=args.version2
            )
            
            if not diff:
                print(f"Could not compare versions {args.version1} and {args.version2} for prompt {args.id}")
                return
            
            # Print diff
            print(f"Diff between version {args.version1} and {args.version2} for prompt {args.id}:")
            for line in diff["diff"]:
                print(line)
    
    def _handle_test_command(self, args) -> None:
        """Handle testing commands."""
        if not args.subcommand:
            return
        
        if args.subcommand == "create":
            # Parse input variables
            input_vars = {}
            if args.input:
                input_vars = json.loads(args.input)
            elif args.input_file:
                with open(args.input_file, "r") as f:
                    input_vars = json.loads(f.read())
            else:
                print("Error: Must provide either --input or --input-file")
                return
            
            # Parse expected output
            expected = None
            if args.expected:
                expected = args.expected
            elif args.expected_file:
                with open(args.expected_file, "r") as f:
                    expected = f.read()
            
            # Create test case
            test_case = self.testing.create_test_case(
                prompt_id=args.prompt_id,
                input_vars=input_vars,
                expected_output=expected,
                name=args.name,
                description=args.description
            )
            
            print(f"Created test case with ID: {test_case.id}")
        
        elif args.subcommand == "list":
            # List test cases
            test_cases = self.testing.list_test_cases(args.prompt_id)
            
            if not test_cases:
                print("No test cases found")
                return
            
            # Print test cases
            print(f"Found {len(test_cases)} test cases:")
            for tc in test_cases:
                print(f"ID: {tc.id} | Name: {tc.name} | Prompt ID: {tc.prompt_id}")
        
        elif args.subcommand == "run":
            # Get LLM callback
            llm_callback = self._get_llm_callback(args.llm)
            
            # Run test case
            asyncio.run(self._run_test_case(args.test_id, llm_callback))
        
        elif args.subcommand == "run-all":
            # Get LLM callback
            llm_callback = self._get_llm_callback(args.llm)
            
            # Run all test cases
            asyncio.run(self._run_all_test_cases(args.prompt_id, llm_callback))
        
        elif args.subcommand == "ab":
            # Get LLM callback
            llm_callback = self._get_llm_callback(args.llm)
            
            # Parse test case IDs
            test_cases = None
            if args.test_cases:
                test_cases = [tc.strip() for tc in args.test_cases.split(",")]
            
            # Run A/B test
            asyncio.run(self._run_ab_test(args.prompt_a, args.prompt_b, llm_callback, test_cases))
    
    async def _run_test_case(self, test_case_id, llm_callback) -> None:
        """Run a test case."""
        try:
            metrics_callbacks = [
                self._create_metrics_callback("exact_match"),
                self._create_metrics_callback("similarity"),
                self._create_metrics_callback("length")
            ]
            
            result = await self.testing.run_test_case(
                test_case_id=test_case_id,
                llm_callback=llm_callback,
                metrics_callbacks=metrics_callbacks
            )
            
            print(f"Test result ID: {result.id}")
            print(f"Test case ID: {result.test_case_id}")
            print(f"Prompt ID: {result.prompt_id}")
            print(f"Prompt version: {result.prompt_version}")
            print(f"Passed: {result.passed}")
            
            if result.metrics:
                print("\nMetrics:")
                for name, value in result.metrics.items():
                    print(f"{name}: {value}")
            
            print("\nOutput:")
            print(result.output)
        except Exception as e:
            print(f"Error running test case: {e}")
    
    async def _run_all_test_cases(self, prompt_id, llm_callback) -> None:
        """Run all test cases for a prompt."""
        try:
            metrics_callbacks = [
                self._create_metrics_callback("exact_match"),
                self._create_metrics_callback("similarity"),
                self._create_metrics_callback("length")
            ]
            
            results = await self.testing.run_test_cases(
                prompt_id=prompt_id,
                llm_callback=llm_callback,
                metrics_callbacks=metrics_callbacks
            )
            
            print(f"Ran {len(results)} test cases for prompt {prompt_id}")
            
            # Calculate aggregate metrics
            if results:
                passed = sum(1 for r in results if r.passed)
                print(f"Passed: {passed}/{len(results)} ({passed/len(results)*100:.2f}%)")
                
                # Aggregate metrics
                metrics = {}
                for r in results:
                    for name, value in r.metrics.items():
                        if name not in metrics:
                            metrics[name] = []
                        metrics[name].append(value)
                
                print("\nAggregate metrics:")
                for name, values in metrics.items():
                    avg = sum(values) / len(values)
                    print(f"{name}: {avg:.4f}")
        except Exception as e:
            print(f"Error running test cases: {e}")
    
    async def _run_ab_test(self, prompt_a_id, prompt_b_id, llm_callback, test_cases) -> None:
        """Run an A/B test."""
        try:
            metrics_callbacks = [
                self._create_metrics_callback("exact_match"),
                self._create_metrics_callback("similarity"),
                self._create_metrics_callback("length")
            ]
            
            result = await self.testing.run_ab_test(
                prompt_a_id=prompt_a_id,
                prompt_b_id=prompt_b_id,
                llm_callback=llm_callback,
                metrics_callbacks=metrics_callbacks,
                test_cases=test_cases
            )
            
            print(f"A/B test result ID: {result.id}")
            print(f"Prompt A ID: {result.prompt_a_id}")
            print(f"Prompt B ID: {result.prompt_b_id}")
            print(f"Winner: {result.winner or 'Tie'}")
            
            print("\nPrompt A metrics:")
            for name, value in result.metrics_a.items():
                print(f"{name}: {value:.4f}")
            
            print("\nPrompt B metrics:")
            for name, value in result.metrics_b.items():
                print(f"{name}: {value:.4f}")
        except Exception as e:
            print(f"Error running A/B test: {e}")
    
    def _handle_eval_command(self, args) -> None:
        """Handle evaluation commands."""
        if not args.subcommand:
            return
        
        if args.subcommand == "metrics":
            # List metrics
            metrics = self.evaluator.list_metrics()
            
            if not metrics:
                print("No metrics registered")
                return
            
            # Print metrics
            print(f"Found {len(metrics)} metrics:")
            for metric in metrics:
                print(f"Name: {metric.name} | Description: {metric.description}")
        
        elif args.subcommand == "register":
            # Register custom metric
            if args.keywords:
                # Register ContainsKeywordsMetric
                keywords = [k.strip() for k in args.keywords.split(",")]
                metric = ContainsKeywordsMetric(keywords)
                self.evaluator.register_metric(metric)
                print(f"Registered ContainsKeywordsMetric with name: {metric.name}")
            elif args.min_length is not None or args.max_length is not None or args.target_length is not None:
                # Register LengthMetric
                metric = LengthMetric(
                    min_length=args.min_length,
                    max_length=args.max_length,
                    target_length=args.target_length
                )
                self.evaluator.register_metric(metric)
                print(f"Registered LengthMetric with name: {metric.name}")
            else:
                print("Error: Must provide either --keywords, --min-length, --max-length, or --target-length")
        
        elif args.subcommand == "run":
            # Parse inputs
            inputs = []
            if args.inputs:
                inputs = json.loads(args.inputs)
            elif args.inputs_file:
                with open(args.inputs_file, "r") as f:
                    inputs = json.loads(f.read())
            else:
                print("Error: Must provide either --inputs or --inputs-file")
                return
            
            # Parse expected outputs
            expected_outputs = None
            if args.expected:
                expected_outputs = json.loads(args.expected)
            elif args.expected_file:
                with open(args.expected_file, "r") as f:
                    expected_outputs = json.loads(f.read())
            
            # Parse metrics
            metric_names = None
            if args.metrics:
                metric_names = [m.strip() for m in args.metrics.split(",")]
            
            # Get LLM callback
            llm_callback = self._get_llm_callback(args.llm)
            
            # Run evaluation
            asyncio.run(self._run_evaluation(
                args.prompt_id,
                inputs,
                expected_outputs,
                metric_names,
                llm_callback
            ))
    
    async def _run_evaluation(self, prompt_id, inputs, expected_outputs, metric_names, llm_callback) -> None:
        """Run an evaluation."""
        try:
            result = await self.evaluator.evaluate_prompt(
                prompt_id=prompt_id,
                inputs=inputs,
                llm_callback=llm_callback,
                expected_outputs=expected_outputs,
                metric_names=metric_names
            )
            
            print(f"Evaluated prompt {prompt_id} with {result['num_samples']} samples")
            
            # Print aggregated metrics
            print("\nAggregated metrics:")
            for name, value in result["aggregated_metrics"].items():
                print(f"{name}: {value:.4f}")
            
            # Print individual results
            print("\nIndividual results:")
            for i, r in enumerate(result["individual_results"]):
                print(f"\nSample {i+1}:")
                print(f"Input: {json.dumps(r['input'])}")
                print(f"Output: {r['output']}")
                if r["expected"]:
                    print(f"Expected: {r['expected']}")
                
                print("Metrics:")
                for name, value in r["metrics"].items():
                    print(f"{name}: {value:.4f}")
        except Exception as e:
            print(f"Error running evaluation: {e}")
    
    def _get_llm_callback(self, llm_name: Optional[str]) -> callable:
        """Get an LLM callback function."""
        # Default to a simple echo function for testing
        if not llm_name or llm_name == "echo":
            async def echo_callback(prompt, vars):
                return f"Echo: {prompt}"
            return echo_callback
        
        # Add more LLM callbacks as needed
        if llm_name == "openai":
            # Example implementation using OpenAI
            try:
                import openai
                
                async def openai_callback(prompt, vars):
                    response = await openai.Completion.acreate(
                        model="text-davinci-003",
                        prompt=prompt,
                        max_tokens=1000
                    )
                    return response.choices[0].text.strip()
                
                return openai_callback
            except ImportError:
                print("Error: OpenAI package not installed. Run `pip install openai` to use this LLM.")
                sys.exit(1)
        
        # Add more LLM implementations as needed
        
        print(f"Error: Unknown LLM callback: {llm_name}")
        sys.exit(1)
    
    def _create_metrics_callback(self, metric_type: str) -> callable:
        """Create a metrics callback function."""
        # Simple metrics
        if metric_type == "exact_match":
            def exact_match_callback(output, expected):
                if not expected:
                    return {"exact_match": 0.0}
                return {"exact_match": 1.0 if output.strip() == expected.strip() else 0.0}
            return exact_match_callback
        
        elif metric_type == "similarity":
            from difflib import SequenceMatcher
            
            def similarity_callback(output, expected):
                if not expected:
                    return {"similarity": 0.0}
                return {"similarity": SequenceMatcher(None, output, expected).ratio()}
            return similarity_callback
        
        elif metric_type == "length":
            def length_callback(output, expected):
                out_len = len(output)
                if not expected:
                    return {"length": 1.0 if out_len > 0 else 0.0}
                
                exp_len = len(expected)
                if exp_len == 0:
                    return {"length": 1.0 if out_len == 0 else 0.0}
                
                # Return score inversely proportional to the difference
                ratio = min(out_len / exp_len, exp_len / out_len)
                return {"length": ratio}
            return length_callback
        
        # Default no-op metric
        return lambda output, expected: {}


def main():
    """Main entry point for the CLI."""
    CLI().run()


if __name__ == "__main__":
    main()