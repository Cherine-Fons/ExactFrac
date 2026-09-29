"""Guarded source-tree entry point for the separate irregular follow-up."""

if __name__ == "__main__":
    import sys
    from pathlib import Path

    root = Path(__file__).absolute().parents[1]
    original_path = list(sys.path)
    try:
        sys.path.insert(0, str(root))
        from exactfrac import experiments_irregular

        expected = str(root / "exactfrac/experiments_irregular.py")
        if (experiments_irregular.__file__ != expected
                or experiments_irregular.__spec__.origin != expected):
            raise RuntimeError("irregular entry point resolved outside the source tree")
        raise SystemExit(experiments_irregular.main())
    finally:
        sys.path[:] = original_path
