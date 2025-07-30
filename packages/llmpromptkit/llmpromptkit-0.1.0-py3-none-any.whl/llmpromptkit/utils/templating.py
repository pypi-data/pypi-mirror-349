import re
import json
from typing import Dict, Any, List, Optional, Union, Callable
from string import Formatter

class TemplateError(Exception):
    """Exception raised for errors in template rendering."""
    pass

class PromptTemplate:
    """Advanced templating system for prompts."""
    def __init__(self, template: str):
        self.template = template
        self._validate_template()
    
    def _validate_template(self) -> None:
        """Validate template syntax."""
        try:
            # Check for basic placeholder syntax
            list(Formatter().parse(self.template))
            
            # Check for conditional syntax
            self._validate_conditionals()
            
            # Check for loop syntax
            self._validate_loops()
        except Exception as e:
            raise TemplateError(f"Invalid template syntax: {str(e)}")
    
    def _validate_conditionals(self) -> None:
        """Validate conditional blocks in the template."""
        # Simple validation to ensure if/endif blocks match
        if_count = len(re.findall(r'\{\s*if\s+.*?\s*\}', self.template))
        endif_count = len(re.findall(r'\{\s*endif\s*\}', self.template))
        
        if if_count != endif_count:
            raise TemplateError(f"Mismatched conditional blocks: {if_count} 'if' and {endif_count} 'endif'")
    
    def _validate_loops(self) -> None:
        """Validate loop blocks in the template."""
        # Simple validation to ensure for/endfor blocks match
        for_count = len(re.findall(r'\{\s*for\s+.*?\s*\}', self.template))
        endfor_count = len(re.findall(r'\{\s*endfor\s*\}', self.template))
        
        if for_count != endfor_count:
            raise TemplateError(f"Mismatched loop blocks: {for_count} 'for' and {endfor_count} 'endfor'")
    
    def _render_conditionals(self, template: str, variables: Dict[str, Any]) -> str:
        """Process conditional blocks in the template."""
        # Handle if-else-endif blocks
        pattern = r'\{\s*if\s+(.*?)\s*\}(.*?)(?:\{\s*else\s*\}(.*?))?\{\s*endif\s*\}'
        
        def replace_conditional(match):
            condition = match.group(1)
            if_block = match.group(2)
            else_block = match.group(3) or ""
            
            # Evaluate condition
            try:
                # Replace variables in condition
                for var_name, var_value in variables.items():
                    if isinstance(var_value, str):
                        # For strings, replace with quoted value
                        condition = condition.replace(var_name, f'"{var_value}"')
                    else:
                        # For other types, replace directly
                        condition = condition.replace(var_name, str(var_value))
                
                result = eval(condition, {"__builtins__": {}}, variables)
                return if_block if result else else_block
            except Exception as e:
                raise TemplateError(f"Error evaluating condition '{condition}': {str(e)}")
        
        # Use re.DOTALL to match across multiple lines
        return re.sub(pattern, replace_conditional, template, flags=re.DOTALL)
    
    def _render_loops(self, template: str, variables: Dict[str, Any]) -> str:
        """Process loop blocks in the template."""
        # Handle for loops
        pattern = r'\{\s*for\s+(.*?)\s+in\s+(.*?)\s*\}(.*?)\{\s*endfor\s*\}'
        
        def replace_loop(match):
            var_name = match.group(1)
            iterable_expr = match.group(2)
            loop_body = match.group(3)
            
            try:
                # Get the iterable from variables
                if iterable_expr in variables and hasattr(variables[iterable_expr], '__iter__'):
                    iterable = variables[iterable_expr]
                else:
                    # Try to evaluate the expression
                    iterable = eval(iterable_expr, {"__builtins__": {}}, variables)
                
                if not hasattr(iterable, '__iter__'):
                    raise TemplateError(f"'{iterable_expr}' is not iterable")
                
                # Process the loop body for each item
                result = []
                for item in iterable:
                    # Create a copy of variables with loop variable
                    loop_vars = variables.copy()
                    loop_vars[var_name] = item
                    
                    # Process the loop body with the new variables
                    body_content = loop_body
                    for k, v in loop_vars.items():
                        placeholder = f"{{{k}}}"
                        if placeholder in body_content:
                            body_content = body_content.replace(placeholder, str(v))
                    
                    result.append(body_content)
                
                return "".join(result)
            except Exception as e:
                raise TemplateError(f"Error processing loop '{match.group(0)}': {str(e)}")
        
        # Use re.DOTALL to match across multiple lines
        return re.sub(pattern, replace_loop, template, flags=re.DOTALL)
    
    def _apply_filters(self, value: Any, filters: List[str]) -> str:
        """Apply filters to a value."""
        result = value
        for filter_name in filters:
            if filter_name == "upper":
                result = str(result).upper()
            elif filter_name == "lower":
                result = str(result).lower()
            elif filter_name == "title":
                result = str(result).title()
            elif filter_name == "capitalize":
                result = str(result).capitalize()
            elif filter_name == "strip":
                result = str(result).strip()
            elif filter_name == "json":
                result = json.dumps(result)
            else:
                raise TemplateError(f"Unknown filter: {filter_name}")
        return result
    
    def _render_variables(self, template: str, variables: Dict[str, Any]) -> str:
        """Replace variables in the template with their values."""
        result = template
        
        # Process variables with filters
        pattern = r'\{(.*?)(?:\|(.*?))?\}'
        
        def replace_var(match):
            var_expr = match.group(1).strip()
            filters_expr = match.group(2)
            
            # Extract filters
            filters = []
            if filters_expr:
                filters = [f.strip() for f in filters_expr.split('|')]
            
            try:
                # Simple variable
                if var_expr in variables:
                    value = variables[var_expr]
                else:
                    # Try to evaluate as an expression
                    try:
                        value = eval(var_expr, {"__builtins__": {}}, variables)
                    except:
                        return match.group(0)  # Keep as is if evaluation fails
                
                # Apply filters
                return str(self._apply_filters(value, filters))
            except Exception as e:
                raise TemplateError(f"Error processing variable '{var_expr}': {str(e)}")
        
        return re.sub(pattern, replace_var, result)
    
    def render(self, **kwargs) -> str:
        """Render the template with provided variables."""
        result = self.template
        
        # Process templates in multiple passes
        # First, handle conditional blocks
        result = self._render_conditionals(result, kwargs)
        
        # Then, handle loops
        result = self._render_loops(result, kwargs)
        
        # Finally, handle simple variable substitution
        result = self._render_variables(result, kwargs)
        
        return result


class PromptTemplateRegistry:
    """Registry for prompt templates."""
    def __init__(self):
        self.templates: Dict[str, PromptTemplate] = {}
    
    def register(self, name: str, template: Union[str, PromptTemplate]) -> None:
        """Register a template."""
        if isinstance(template, str):
            template = PromptTemplate(template)
        self.templates[name] = template
    
    def get(self, name: str) -> Optional[PromptTemplate]:
        """Get a template by name."""
        return self.templates.get(name)
    
    def render(self, name: str, **kwargs) -> str:
        """Render a template by name."""
        template = self.get(name)
        if not template:
            raise ValueError(f"Template '{name}' not found")
        return template.render(**kwargs)
    
    def list_templates(self) -> List[str]:
        """List all registered templates."""
        return list(self.templates.keys())


# Create a singleton instance
template_registry = PromptTemplateRegistry()

# Register some common templates
template_registry.register(
    "basic_completion",
    """
    {system_message}
    
    {user_message}
    """
)

template_registry.register(
    "chat_template",
    """
    {system_message}
    
    {for message in conversation}
    {if message.role == "user"}Human: {message.content}
    {else}Assistant: {message.content}
    {endif}
    {endfor}
    """
)

template_registry.register(
    "few_shot",
    """
    {system_message}
    
    Here are some examples:
    {for example in examples}
    Input: {example.input}
    Output: {example.output}
    {endfor}
    
    Input: {input}
    Output:
    """
)