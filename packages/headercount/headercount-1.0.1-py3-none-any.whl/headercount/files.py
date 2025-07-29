# SPDX-FileCopyrightText: 2025 Broken Pen
#
# SPDX-License-Identifier: Apache-2.0

"""Contains the functions for input file collection."""

from pathlib import Path

TYPE_CHECKING = False

if TYPE_CHECKING:
    from collections.abc import Iterator

__all__ = (
    "CPP_SUFFIXES",
    "HEADER_SUFFIXES",
    "SOURCE_SUFFIXES",
    "iter_input_files",
)

HEADER_SUFFIXES = frozenset(
    [".h", ".H", ".hh", ".hp", ".hpp", ".HPP", ".hxx", ".h++", ".inl", ".tcc", ".icc"]
)

SOURCE_SUFFIXES = frozenset(
    [".c", ".C", ".cc", ".cp", ".cpp", ".CPP", ".cxx", ".c++", ".i", ".ii"]
)

CPP_SUFFIXES = HEADER_SUFFIXES | SOURCE_SUFFIXES


def iter_input_files(
    args: list[str],
    *,
    recursive: bool,
    exclude: list[str],
    exclude_dir: list[str],
) -> "Iterator[Path]":
    """Iterate over all input files specified by the given arguments.

    Args:
        args: An iterable of file and directory names.
        recursive: If `True`, recursively search directories for input
            files. If `False`, ignore directory names.
        exclude: A list of shell-like glob patterns. If an input file
            name matches any of these patterns, it is ignored.
        exclude_dir: As `exclude`, but applied to directory names. If
            `recursive` is `False`, this has no effect.

    Returns:
        An iterator over all input file names. Input files must have a
        file suffix given in `CPP_SUFFIXES`.
    """
    if recursive:
        return _iter_input_files_deep(args, exclude=exclude, exclude_dir=exclude_dir)
    return _iter_input_files_flat(args, exclude=exclude)


def _iter_input_files_flat(args: list[str], *, exclude: list[str]) -> "Iterator[Path]":
    """Non-recursive version of `iter_input_files`."""
    for arg in args:
        path = Path(arg)
        if path.is_dir():
            pass
            # log
        elif path.suffix in CPP_SUFFIXES and not _any_match(path, exclude):
            yield path


def _iter_input_files_deep(
    args: list[str],
    *,
    exclude: list[str],
    exclude_dir: list[str],
) -> "Iterator[Path]":
    """Recursive version of `iter_input_files`."""
    stack = [Path(arg) for arg in reversed(args)]
    while stack:
        path = stack.pop()
        if path.is_dir():
            if not _any_match(path, exclude_dir):
                stack.extend(path.iterdir())
        elif path.suffix in CPP_SUFFIXES and not _any_match(path, exclude):
            yield path


def _any_match(path: Path, patterns: list[str]) -> bool:
    """True if any of the given patterns match `path`."""
    return any(path.match(pattern) for pattern in patterns)


del TYPE_CHECKING
