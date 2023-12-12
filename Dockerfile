#!/usr/bin/env -S docker image build -t wbm-exclusion-tool .

FROM        python:3.11-slim-bullseye

ENV         STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
WORKDIR     /app
CMD         ["streamlit", "run", "main.py"]

COPY        requirements.txt ./requirements.txt
RUN         pip install -r requirements.txt
COPY        . ./
