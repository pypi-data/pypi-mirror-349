from ..types import Sample


def does_compile(sample: Sample) -> int:  # 1 = pass, 0 = fail
    try:
        compile(sample.output["content"], "<parser>", "exec")
        return 1
    except Exception:
        return 0
