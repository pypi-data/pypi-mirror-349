#!/usr/bin/env bash

PYTHONPATH="$(git rev-parse --show-toplevel)/src" python -m tests.scripts.test_queue_processor
