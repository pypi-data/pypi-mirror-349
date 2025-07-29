# SPDX-FileCopyrightText: 2025 Broken Pen
#
# SPDX-License-Identifier: Apache-2.0

"""Functions that search files for include directives."""

import itertools
from pathlib import Path

__all__ = (
    "AmbiguousNameError",
    "Include",
    "get_flat_includes_lists",
    "get_includes_lists",
)

TYPE_CHECKING = False

if TYPE_CHECKING:
    from collections.abc import Collection, Iterable, Iterator


class AmbiguousNameError(Exception):
    """There is more than one matching file for an include directive."""


class Include(str):
    """Type representing `#include` directives.

    For speed and ease of implementation, this inherits from `str`.
    """

    __slots__ = ()

    def __new__(cls: type["Include"], *args: object, **kwargs: object) -> "Include":
        """Create a new instance.

        Examples:
            >>> Include('<vector>')
            >>> Include('"MyHeader.hpp"')

        Raises:
            ValueError if the given string is not wrapped by
                `#include`-style quotes (either double quotes or angle
                brackets).
        """
        result = super().__new__(cls, *args, **kwargs)
        is_system = result[0] == "<" and result[-1] == ">"
        is_regular = result[0] == '"' == result[-1]
        if not (is_system or is_regular):
            raise ValueError("cannot find quotes: " + repr(result))
        return result

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self!s})"

    def is_system(self) -> bool:
        """Return `True` if this directive uses angle brackets."""
        return self[0] == "<"

    def unquoted(self) -> str:
        """Remove quotes around the included file."""
        return self[1:-1]


def get_includes_lists(
    paths: "Iterable[Path]",
    *,
    inclusive: bool,
) -> dict[Path, list[Include]]:
    """For each path in `paths`, return a list of included files.

    Args:
        paths: An iterable of `pathlib.Path`s to search.
        inclusive: If `True`, this lists not only a file's direct
            includes, but also its includes' includes, etc. Only files
            that are passed via `paths` are search recursively. If
            `False`, only direct includes are listed.

    Returns:
        A mapping from a file's path to the files included by said
        file (either directly or indirectly).
    """
    flat_lists = get_flat_includes_lists(paths)
    return _get_deep_includes_lists(flat_lists) if inclusive else flat_lists


def get_flat_includes_lists(paths: "Iterable[Path]") -> dict[Path, list[Include]]:
    """For each path in `paths`, return a list of included files.

    Returns:
        A mapping from a file's path to the files directly included by
        said file.
    """
    includes = {}
    for path in paths:
        with path.open("r") as file_:
            includes[path] = list(iter_includes(file_))
    return includes


def _get_deep_includes_lists(
    flat_lists: dict[Path, list[Include]],
) -> dict[Path, list[Include]]:
    """Takes the result of `get_includes_lists` and expands it."""
    include_map = _build_include_map(
        includes=set(itertools.chain.from_iterable(flat_lists.values())),
        available_files=flat_lists.keys(),
    )

    # The dict in which we collect our results.
    inclusive_lists: dict[Path, list[Include]] = {}

    def _iter_direct_includes(path: Path) -> "Iterator[Include]":
        """Iterate direct includes, skip those not to be searched."""
        return iter(flat_lists[path])

    def _collect_all_includes(path: Path) -> list[Include]:
        """Put together the direct and indirect includes of a file."""
        direct_includes = flat_lists[path]
        direct_include_files = (
            include_map.get(direct_include) for direct_include in direct_includes
        )
        indirect_includes = (
            inclusive_lists.get(path, []) for path in direct_include_files if path
        )
        return list(itertools.chain(direct_includes, *indirect_includes))

    # Iterative depth-first search with a stack of iterators.
    stack = [(path, _iter_direct_includes(path)) for path in flat_lists]
    files_being_searched = set(flat_lists.keys())
    while stack:
        path, includes_to_handle = stack[-1]
        include = next(includes_to_handle, None)
        if include is None:
            # We have collected all direct+indirect includes for every
            # direct include of `path`. Now we can put them together.
            inclusive_lists[path] = _collect_all_includes(path)
            files_being_searched.remove(path)
            stack.pop()
            continue
        # Guess which file this include directive references.
        include_file = include_map.get(include)
        if (
            include_file
            and include_file not in inclusive_lists
            and include_file not in files_being_searched
        ):
            # The included file is to be searched and we have not
            # searched it already _and_ it is not included in a
            # circular manner. Thus, we descend into it.
            stack.append((include_file, _iter_direct_includes(include_file)))
            files_being_searched.add(include_file)

    return inclusive_lists


def _build_include_map(
    includes: "Iterable[Include]",
    available_files: "Collection[Path]",
) -> dict[Include, Path]:
    """Build a map of which include directive maps to which file.

    Args:
        includes: An iterable of `Include` objects.
        available_files: A list of files that the include directives
            could possibly map to.

    Returns:
        A mapping `include => available_file` of all `include`s for
        which a file could be found.

    Raises:
        `AmbiguousNameError`: if there are several candidates for
            a given `include`.
    """
    result = {}
    for include in includes:
        candidates = [
            path for path in available_files if path.name == include.unquoted()
        ]
        if len(candidates) > 1:
            raise AmbiguousNameError(str(include))
        if candidates:
            [result[include]] = candidates
    return result


def iter_includes(file_: "Iterable[str]") -> "Iterator[Include]":
    """Iterate over include directives in a file.

    Args:
        file_: A file object to read from.
        ignore_system: If `True`, "#include <...>" lines are ignored.

    Returns:
        An iterator over files included by `file_`. Inclusion is
        determined by searching for #include directives.
    """
    for line in file_:
        line = line.lstrip()
        if not line.startswith("#"):
            continue
        parts = line[1:].split()
        if parts[0] != "include":
            continue
        yield Include(parts[1])


del TYPE_CHECKING
