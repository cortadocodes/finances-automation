#!/usr/bin/env bash

# Auto generate API documentation
project="finances_automation"
repo_root="$(git rev-parse --show-toplevel)"
package_root="$repo_root/$project"
docs="$repo_root/api-docs"

version="0.0"
author="Marcus Lugg"

# Generate documentation outline
sphinx-apidoc -F -H "$project" -V "$version" -A "$author" -o "$docs" "$package_root"

# Change theme to ReadTheDocs theme
sed -i 's/alabaster/sphinx_rtd_theme/' "$docs/conf.py"

# Generate html files from the outlines
cd "$docs"
make html
