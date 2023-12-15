#!/bin/bash
cd backend
/root/.local/bin/poetry run uvicorn  start_service:app --reload

