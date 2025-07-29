from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from judgeval.evaluation_run import EvaluationRun
import json
from datetime import datetime, timezone

class TraceSpan(BaseModel):
    span_id: str
    trace_id: str
    function: Optional[str] = None
    depth: int
    created_at: Optional[Any] = None
    parent_span_id: Optional[str] = None
    span_type: Optional[str] = "span"
    inputs: Optional[Dict[str, Any]] = None
    output: Optional[Any] = None
    duration: Optional[float] = None
    annotation: Optional[List[Dict[str, Any]]] = None
    evaluation_runs: Optional[List[EvaluationRun]] = []
    expected_tools: Optional[List[Dict[str, Any]]] = None
    additional_metadata: Optional[Dict[str, Any]] = None

    def model_dump(self, **kwargs):
        return {
            "span_id": self.span_id,
            "trace_id": self.trace_id,
            "depth": self.depth,
#             "created_at": datetime.fromtimestamp(self.created_at).isoformat(),
            "created_at": datetime.fromtimestamp(self.created_at, tz=timezone.utc).isoformat(),
            "inputs": self._serialize_inputs(),
            "output": self._serialize_output(),
            "evaluation_runs": [run.model_dump() for run in self.evaluation_runs] if self.evaluation_runs else [],
            "parent_span_id": self.parent_span_id,
            "function": self.function,
            "duration": self.duration,
            "span_type": self.span_type
        }
    
    def print_span(self):
        """Print the span with proper formatting and parent relationship information."""
        indent = "  " * self.depth
        parent_info = f" (parent_id: {self.parent_span_id})" if self.parent_span_id else ""
        print(f"{indent}→ {self.function} (id: {self.span_id}){parent_info}")
    
    def _serialize_inputs(self) -> dict:
        """Helper method to serialize input data safely."""
        if self.inputs is None:
            return {}
            
        serialized_inputs = {}
        for key, value in self.inputs.items():
            if isinstance(value, BaseModel):
                serialized_inputs[key] = value.model_dump()
            elif isinstance(value, (list, tuple)):
                # Handle lists/tuples of arguments
                serialized_inputs[key] = [
                    item.model_dump() if isinstance(item, BaseModel)
                    else None if not self._is_json_serializable(item)
                    else item
                    for item in value
                ]
            else:
                if self._is_json_serializable(value):
                    serialized_inputs[key] = value
                else:
                    serialized_inputs[key] = self.safe_stringify(value, self.function)
        return serialized_inputs

    def _is_json_serializable(self, obj: Any) -> bool:
        """Helper method to check if an object is JSON serializable."""
        try:
            json.dumps(obj)
            return True
        except (TypeError, OverflowError, ValueError):
            return False

    def safe_stringify(self, output, function_name):
        """
        Safely converts an object to a string or repr, handling serialization issues gracefully.
        """
        try:
            return str(output)
        except (TypeError, OverflowError, ValueError):
            pass
    
        try:
            return repr(output)
        except (TypeError, OverflowError, ValueError):
            pass

        warnings.warn(
            f"Output for function {function_name} is not JSON serializable and could not be converted to string. Setting to None."
        )
        return None
        
    def _serialize_output(self) -> Any:
        """Helper method to serialize output data safely."""
        if self.output is None:
            return None
            
        def serialize_value(value):
            if isinstance(value, BaseModel):
                return value.model_dump()
            elif isinstance(value, dict):
                # Recursively serialize dictionary values
                return {k: serialize_value(v) for k, v in value.items()}
            elif isinstance(value, (list, tuple)):
                # Recursively serialize list/tuple items
                return [serialize_value(item) for item in value]
            else:
                # Try direct JSON serialization first
                try:
                    json.dumps(value)
                    return value
                except (TypeError, OverflowError, ValueError):
                    # Fallback to safe stringification
                    return self.safe_stringify(value, self.function)

        # Start serialization with the top-level output
        return serialize_value(self.output)

class Trace(BaseModel):
    trace_id: str
    name: str
    created_at: str
    duration: float
    entries: List[TraceSpan]
    overwrite: bool = False
    offline_mode: bool = False
    rules: Optional[Dict[str, Any]] = None
    has_notification: Optional[bool] = False
    