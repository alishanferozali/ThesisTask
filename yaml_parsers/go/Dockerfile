FROM golang:1.23.1
    
WORKDIR /app

COPY parser.go /app/parser.go

RUN go mod init gin

RUN go mod tidy

RUN go get gopkg.in/yaml.v3

ENTRYPOINT ["go", "run", "/app/parser.go"]
    