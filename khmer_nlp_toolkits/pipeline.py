"""
Pipeline class
"""
import time
import logging
from typing import Callable, Any, Union
from collections.abc import Iterator

import queue
from itertools import islice
from threading import Thread
from multiprocessing import Process, Queue, cpu_count, Event, Value


# logging.basicConfig(level=logging.INFO)


class Pipeline:
    """
    Pipeline class for setup continue function execution action.
    """

    def __init__(self):
        self.steps = []
        self.info = []
        self.desc = []
        # For parallel running
        self.num_process = []
        self.queues = []
        self.processes = []
        self.qlogs = []
        self.qsize = None

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

    def add(self, step: Callable, num_process: int = 1, is_wrap: bool = False, desc: str = None, **step_params):
        """
        Add a step with its associated parameters.

        Parameters
        ----------
        step: Callable
            A function is added to pipeline.
        is_wrap: bool
            Set to true to wraped func in loop to execute as a batch. If False the data will pass to function directly.
            This is use to with run_parallel(). Set False if use with run().
            Ex: is_wrap=True => [func(obj) for obj in batch]
        **step_params: Any
            Any parameters are accepted by step.
        """
        def process_step(func: Callable, **step_params):
            """
            Wraps any function to add a `.process()` method and includes custom parameters.
            """
            def wrapped(data: Any):
                if not is_wrap:
                    return func(data, **step_params) if data else None
                return [func(obj, **step_params) if obj else None for obj in data]

            wrapped.process = wrapped  # Adds the .process() method
            wrapped.__name__ = func.__name__
            return wrapped

        if not callable(step):
            raise TypeError(f"{step} is not a valid pipeline step (must be callable)")
        wrapped_step = process_step(step, **step_params)
        self.steps.append(wrapped_step)
        self.num_process.append(num_process)
        self.info.append({step.__name__: step_params})
        self.desc.append(desc)

    def run(self, data: Any):
        """
        Pipeline execution function.
        """
        for step in self.steps:
            data = step.process(data)  # Call .process() with the correct parameters
        return data

    def get_queue_status(self):
        """
        Return a list of queue capacity status at a time of function being called.

        Example:
        - Pipeline: in_q -> s1 -> q1 -> s2 -> q2 -> s3 -> out_q (4 queue in total)
        - Result: [10, 10, 9, 0] (qsize=10)
        """
        if not self.queues:
            logging.info("No parallel are running!")
            return None
        return [queue.qsize() for queue in self.queues]

    def queue_backpressure(self):
        """
        Return a list of average percentage of queue fullness. This func should be call after run_parallel finished.
        To check queue capacity in real-time, see get_queue_status() function.

        Example
        =======
        - Pipeline: in_q -> s1 -> q1 -> s2 -> q2 -> s3 -> out_q (4 queue in total)
        - Resual: [84.67, 94.67, 96.48, 0.95]
        - Interpret: Most data Block in queue2 waiting for processed by state3.
        - Feedback: Consider increase state3 process number to reduce wait time.
        """
        if not self.qlogs:
            logging.info("No record of queue yet!")
            return None
        qlogs = [qlog for qlog in self.qlogs if sum(qlog) >= self.qsize]
        if not qlogs:
            return [0.0] * len(self.queues)
        return [round(sum(qlog)/len(qlogs)/self.qsize*100, 2) for qlog in zip(*qlogs)]

    # pylint: disable=all
    def run_parallel(self, data: Union[list, Iterator], batch_size: int = 100, timeout: int = 30, qsize: int = 10):
        """
        Data and State parallel processing function. This function use multiprocesser and threading to execute data
        in parallel. Each state have a number of process to run independently on prarallel when data are available.

        Parameters
        ==========
        data: list|Iterator
            Data to process. It must be a list or Iterator, since the data are process in chuck of batch_size.
        batch_size: int
            Number of data being processed at a time.
        qsize: int
            Batch waiting queue capacity. If the queue full, the process corresponding to that queue will be on halt until
            next state process pickup batch to free queue.
        timeout: int (second), default = 5s
            Maximum time to wait (in seconds) for data to be returned from the pipeline.
            If exceed the timeout, the process will end. This is to prevent logic break of Endless loop.
        """
        self.qsize = qsize
        count_data_in = 0
        count_data_out = 0
        # This is parallel controlling signal
        worker_stop = Event()
        data_feeder_stop = Event()
        count_finish_worker = Value('i', 0)
        try:
            # check system capacity
            logical_cpu = cpu_count()
            if sum(self.num_process) > logical_cpu:
                logging.warning("====================================================")
                logging.warning("Your machine have %d logical CPUs.", logical_cpu)
                logging.warning("You setup %d processes in total that is more than number of your logical CPUs.",
                                sum(self.num_process))
                logging.warning("This could lead to performance drop, stuck or crash (CPU overload).")
                logging.warning("====================================================")
                if sum(self.num_process) > logical_cpu+int(logical_cpu/2):
                    raise RuntimeError("You have too many processes. Consider combine a few \
                                       function together before add to Pipeline.")
            if not isinstance(data, list) and not isinstance(data, Iterator):
                raise ValueError("Data is not a List nor Iterator.")

            # Defined inner funciton to assisted
            def worker(input_queue: Queue, output_queue: Queue, func: Callable):
                while not worker_stop.is_set():
                    try:
                        batch = input_queue.get(timeout=0.2)
                    except queue.Empty:
                        continue
                    result = func(batch)
                    output_queue.put(result)
                # To count the worker that finish
                with count_finish_worker.get_lock():  # acquire lock
                    count_finish_worker.value += 1

            def data_feeder():
                nonlocal count_data_in
                first_q = self.queues[0]
                while not data_feeder_stop.is_set():
                    batch = list(islice(data, batch_size))
                    if not batch:
                        data_feeder_stop.set()
                        break
                    count_data_in += len(batch)
                    first_q.put(batch)

            # Function main logic
            if not self.queues and not self.processes:
                # create queues input_q -> p1 -> q1 -> p2 -> output_q
                self.queues.extend([Queue(maxsize=qsize) for _ in range(len(self.steps)+1)])
                # create process
                for i, n_process in enumerate(self.num_process):
                    self.processes.extend([
                        Process(
                            target=worker,
                            args=(self.queues[i], self.queues[i+1], self.steps[i]),
                            daemon=True
                        )
                        for _ in range(n_process)
                    ])
                # start process
                feed_thread = Thread(target=data_feeder, daemon=True)
                feed_thread.start()
                for process in self.processes:
                    process.start()

            while not worker_stop.is_set():
                try:
                    batch = self.queues[-1].get(timeout=timeout)
                    count_data_out += len(batch)
                    self.qlogs.append(self.get_queue_status())
                    yield batch
                    if count_data_in == count_data_out and data_feeder_stop.is_set():
                        worker_stop.set()
                except queue.Empty:
                    logging.warning("End process half way!! Exceed waiting time set by timeout (%ss).", timeout)
                    logging.warning("==> Consider increase timeout or reduce batch_size.")
                    worker_stop.set()
                    data_feeder_stop.set()

        except KeyboardInterrupt:
            logging.error("Main process interrupted... All parallel processes terminated!!")
            for process in self.processes:
                process.terminate()
        finally:
            logging.info("Start cleaning up....")
            # check and clean process, queue
            while sum(self.get_queue_status()) != 0 or count_finish_worker.value != sum(self.num_process):
                for que in self.queues:
                    while not que.empty():
                        que.get()
                time.sleep(0.3)
            logging.info("Clear all remnant data.... start join process!!!")
            # end process, queue and release resource
            feed_thread.join()
            for process in self.processes:
                process.join()
            for que in self.queues:
                que.close()
                que.join_thread()
            self.queues.clear()
            self.processes.clear()
            logging.info("Clean up completed!!")
    # pylint: enable=all


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
