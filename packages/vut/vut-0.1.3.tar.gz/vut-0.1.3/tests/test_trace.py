import io
import sys

from pytest_mock import MockFixture

from vut.trace import disable_trace, enable_trace, trace_module


def test_trace_module__calls_filtered(mocker: MockFixture):
    frame_pyenv = mocker.Mock()
    frame_pyenv.f_code.co_filename = (
        "/home/user/.pyenv/versions/3.9.0/lib/python3.9/site-packages/pytest.py"
    )

    frame_cache = mocker.Mock()
    frame_cache.f_code.co_filename = "/home/user/.cache/pip/wheels/some_package.py"

    frame_special = mocker.Mock()
    frame_special.f_code.co_filename = "<stdin>"

    with mocker.patch("sys.stdout", new=io.StringIO()) as fake_out:
        result1 = trace_module(frame_pyenv, "call", None)
        result2 = trace_module(frame_cache, "call", None)
        result3 = trace_module(frame_special, "call", None)

        assert fake_out.getvalue() == ""

    assert result1 is trace_module
    assert result2 is trace_module
    assert result3 is trace_module


def test_trace_module__displays_module(mocker: MockFixture):
    frame = mocker.Mock()
    frame.f_code.co_filename = "/home/user/project/mymodule.py"

    with mocker.patch("sys.stdout", new=io.StringIO()) as fake_out:
        result = trace_module(frame, "call", None)

        assert f"Module loaded: {frame.f_code.co_filename}" in fake_out.getvalue()

    assert result is trace_module


def test_trace_module__ignores_non_call_events(mocker: MockFixture):
    frame = mocker.Mock()
    frame.f_code.co_filename = "/home/user/project/mymodule.py"

    with mocker.patch("sys.stdout", new=io.StringIO()) as fake_out:
        for event in ["line", "return", "exception"]:
            fake_out.truncate(0)
            fake_out.seek(0)
            result = trace_module(frame, event, None)
            assert fake_out.getvalue() == ""
            assert result is trace_module


def test_enable_trace():
    try:
        old_trace = sys.gettrace()
        enable_trace()
        assert sys.gettrace() is trace_module
    finally:
        sys.settrace(old_trace)


def test_disable_trace():
    enable_trace()
    assert sys.gettrace() is trace_module

    disable_trace()
    assert sys.gettrace() is None
