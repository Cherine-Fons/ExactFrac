"""Guarded source-tree entry point for the fixed Unit 21 campaign."""

if __name__ == "__main__":
    import sys
    from pathlib import Path

    root = Path(__file__).absolute().parents[1]
    original_path = list(sys.path)
    try:
        sys.path.insert(0, str(root))
        from exactfrac import experiments

        expected = str(root / "exactfrac/experiments.py")
        if experiments.__file__ != expected or experiments.__spec__.origin != expected:
            raise RuntimeError("experiment entry point resolved outside the source tree")
        raise SystemExit(experiments.main())
    finally:
        sys.path[:] = original_path
