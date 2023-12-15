#!/bin/bash
service nginx start
/root/.local/bin/poetry run uvicorn  start_service:app --host 0.0.0.0 --proxy-headers --port 12345


