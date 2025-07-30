from typing import Dict, List, Optional, Any, Union, Callable
import re
import numpy as np
from difflib import SequenceMatcher

def exact_match(generated: str, expected: str) -> float:
    """Calculate exact match score (1.0 if exact match, 0.0 otherwise)."""
    if not expected or not generated:
        return 0.0
    return 1.0 if generated.strip() == expected.strip() else 0.0

def contains_all(generated: str, items: List[str], case_sensitive: bool = False) -> float:
    """Check if generated text contains all items in the list."""
    if not items:
        return 0.0
    
    if not case_sensitive:
        generated = generated.lower()
        items = [item.lower() for item in items]
    
    matches = sum(1 for item in items if item in generated)
    return matches / len(items)

def similarity_score(str1: str, str2: str) -> float:
    """Calculate string similarity using difflib."""
    if not str1 or not str2:
        return 0.0
    return SequenceMatcher(None, str1, str2).ratio()

def word_count(text: str) -> int:
    """Count words in text."""
    return len(re.findall(r'\w+', text))

def length_ratio(generated: str, expected: str) -> float:
    """Calculate ratio of generated text length to expected text length."""
    if not expected:
        return 0.0
    
    gen_length = len(generated)
    exp_length = len(expected)
    
    # Avoid division by zero
    if exp_length == 0:
        return 0.0 if gen_length > 0 else 1.0
    
    # Return value between 0 and 1, with 1 being perfect match
    # and decreasing as the ratio diverges from 1
    ratio = gen_length / exp_length
    return min(ratio, 1/ratio) if ratio > 0 else 0.0

def word_overlap(generated: str, expected: str) -> float:
    """Calculate the word overlap between generated and expected text."""
    if not expected or not generated:
        return 0.0
    
    gen_words = set(re.findall(r'\w+', generated.lower()))
    exp_words = set(re.findall(r'\w+', expected.lower()))
    
    if not exp_words:
        return 0.0
    
    intersection = gen_words.intersection(exp_words)
    return len(intersection) / len(exp_words)

def keyword_presence(text: str, keywords: List[str], weight: Optional[Dict[str, float]] = None) -> Dict[str, float]:
    """Check for presence of keywords with optional weights."""
    if not keywords:
        return {"keyword_score": 0.0}
    
    text = text.lower()
    result = {}
    
    total_weight = 0
    weighted_score = 0
    
    for keyword in keywords:
        keyword_lower = keyword.lower()
        presence = 1.0 if keyword_lower in text else 0.0
        
        # Apply weight if provided
        kw_weight = weight.get(keyword, 1.0) if weight else 1.0
        total_weight += kw_weight
        weighted_score += presence * kw_weight
        
        result[f"keyword_{keyword}"] = presence
    
    # Calculate overall weighted score
    if total_weight > 0:
        result["keyword_score"] = weighted_score / total_weight
    else:
        result["keyword_score"] = 0.0
    
    return result

class MetricsSet:
    """A collection of evaluation metrics functions."""
    def __init__(self):
        self.metrics = {}
    
    def add_metric(self, name: str, func: Callable, description: Optional[str] = None) -> None:
        """Add a metric function to the set."""
        self.metrics[name] = {
            "function": func,
            "description": description or ""
        }
    
    def evaluate(self, generated: str, expected: Optional[str] = None, **kwargs) -> Dict[str, float]:
        """Evaluate all metrics on the given text."""
        results = {}
        
        for name, metric in self.metrics.items():
            try:
                # Different metrics may require different arguments
                if expected is not None:
                    if "keywords" in kwargs and name == "keyword_presence":
                        result = metric["function"](generated, kwargs["keywords"])
                    else:
                        result = metric["function"](generated, expected)
                else:
                    result = metric["function"](generated)
                
                # Handle both single values and dictionaries
                if isinstance(result, dict):
                    results.update(result)
                else:
                    results[name] = result
            except Exception as e:
                results[name] = 0.0
                print(f"Error calculating metric {name}: {e}")
        
        return results

def create_default_metrics_set() -> MetricsSet:
    """Create a MetricsSet with default metrics."""
    metrics = MetricsSet()
    
    metrics.add_metric(
        "exact_match", 
        exact_match, 
        "Exact string match between expected and generated"
    )
    
    metrics.add_metric(
        "similarity", 
        similarity_score, 
        "String similarity using difflib's SequenceMatcher"
    )
    
    metrics.add_metric(
        "word_overlap", 
        word_overlap, 
        "Ratio of words in expected that appear in generated"
    )
    
    metrics.add_metric(
        "length_ratio", 
        length_ratio, 
        "Ratio of generated text length to expected text length"
    )
    
    return metrics