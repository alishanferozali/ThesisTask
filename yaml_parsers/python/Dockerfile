FROM python:3.8-slim
    
WORKDIR /app

COPY parser.py /app/parser.py

RUN pip install pyyaml

ENTRYPOINT ["python", "/app/parser.py"]
    
    