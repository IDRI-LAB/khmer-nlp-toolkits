"""
Pipeline class
"""
from typing import Callable, Any


class Pipeline:
    """
    Pipeline class for setup continue function execution action.
    """

    def __init__(self):
        self.steps = []
        self.info = []
        self.desc = []

    def __str__(self):
        description = [
            "==============================",
            "All function flow in pipeline.",
            "=============================="
        ]
        for i, (element, func_desc) in enumerate(zip(self.info, self.desc), 1):
            func_name, params = list(element.items())[0]
            formatted_str = f"{i}. {func_name}(" + ", ".join(f"{key}={value}" for key, value in params.items()) + ")"
            description.append(formatted_str)
            if func_desc is not None:
                description.append("\t" + func_desc)
        return "\n".join(description) + "\n"

    def __len__(self):
        return len(self.info)

    def add(self, step: Callable, desc: str = None, **step_params):
        """
        Add a step with its associated parameters.

        Parameters
        ----------
        step: Callable
            A function is added to pipeline.
        **step_params: Any
            Any parameters are accepted by step.
        """
        def process_step(func: Callable, **step_params):
            """
            Wraps any function to add a `.process()` method and includes custom parameters.
            """
            def wrapped(data: Any):
                return func(data, **step_params)

            wrapped.process = wrapped  # Adds the .process() method
            return wrapped

        if not callable(step):
            raise TypeError(f"{step} is not a valid pipeline step (must be callable)")
        wrapped_step = process_step(step, **step_params)
        self.steps.append(wrapped_step)
        self.info.append({step.__name__: step_params})
        self.desc.append(desc)

    def run(self, data: Any, **kwargs):
        """
        Pipeline execution function.
        """
        for step in self.steps:
            data = step.process(data, **kwargs)  # Call .process() with the correct parameters
        return data


if __name__ == "__main__":
    # Example custom function
    def func_a(text: str, is_upper: bool = False) -> str:
        """A function that conditionally capitalizes text."""
        return text.upper() if is_upper else text.lower()

    def func_b(text: str, times: int = 1) -> str:
        """Repeat the text a specified number of times."""
        return text * times

    # Create the pipeline
    pipeline = Pipeline()

    # Add func_a and func_b to the pipeline with its parameters
    pipeline.add(func_a, is_upper=True, desc="lower or upper text.")  # Pass `is_upper=True` to func_a
    pipeline.add(func_b, times=3)  # Pass `times=3` to func_b

    # List function added to pipeline.
    print(str(pipeline))

    # Run the pipeline with input text
    INPUT_TEXT = "hello world"
    output_text = pipeline.run(INPUT_TEXT)
    print(output_text)
