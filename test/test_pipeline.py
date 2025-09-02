import pytest
from khmer_nlp_toolkits import pipeline


@pytest.fixture
def pipe():
    pipeline_obj = pipeline.Pipeline()
    pipeline_obj.add(str.lower)
    pipeline_obj.add(str.split, sep="\n", maxsplit=1)
    return pipeline_obj


"""
Pipeline.add()
"""
def test_pipeline_add(pipe):
    # Check given params to function
    assert pipe.info[0] == {"lower": {}}
    assert pipe.info[1] == {"split": {"sep": "\n", "maxsplit": 1}}

    # Check number of added function
    number_of_func = 2
    assert len(pipe) == number_of_func
    assert len(pipe.steps) == number_of_func
    assert len(pipe.info) == number_of_func
    assert len(pipe.desc) == number_of_func


"""
Pipeline.run()
"""
def test_pipeline_run(pipe):
    output = pipe.run("Example wi\nth enter.")
    assert output == ["example wi", "th enter."]

