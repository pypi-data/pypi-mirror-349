from typing import Any, Dict, Callable, Optional

class DspySignature:
    """
    Declarative signature for agent actions/tools.
    Describes the action name, input/output schema, and handler.
    """
    def __init__(
        self,
        name: str,
        input_schema: Dict[str, Any],
        output_schema: Dict[str, Any],
        handler: Optional[Callable] = None,
        description: Optional[str] = None,
    ):
        self.name = name
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.handler = handler
        self.description = description

    def __call__(self, *args, **kwargs):
        if self.handler is None:
            raise NotImplementedError("No handler assigned for this signature.")
        return self.handler(*args, **kwargs)
