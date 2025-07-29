#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2025 Broken Pen
#
# SPDX-License-Identifier: Apache-2.0

"""Launcher for `headercount`."""

import sys

import headercount


def main() -> None:
    """The main function."""
    headercount.main(sys.argv[1:])


if __name__ == "__main__":
    main()
