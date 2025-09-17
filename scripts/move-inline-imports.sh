#!/bin/bash
autoimport "$@"
git diff --exit-code --quiet || exit 1

