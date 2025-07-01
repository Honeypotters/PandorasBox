# Stage 1: The builder
# This stage uses the Go SDK to build the application
FROM golang:1.24-alpine AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy the go mod and sum files
COPY go.mod go.sum ./

# Download all dependencies. Dependencies will be cached if the go.mod and go.sum files are not changed
RUN go mod download

# Copy the local package files to the container's workspace
COPY . .

# Build the Go app as a static binary to ensure it runs in a minimal container
RUN CGO_ENABLED=0 go build -o /pandora-backend .

# Stage 2: The runner
# Use a minimal image to run the application
FROM alpine:latest

# Set the working directory
WORKDIR /app

# Run as a non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# Copy the built binary from the 'builder' stage
COPY --from=builder /pandora-backend .

COPY .env .env
COPY *.mmdb .

# Expose port 80 for the honeypot and 8080 for the website
EXPOSE 80
EXPOSE 8080

ENV GIN_MODE=release

# Command to run the executable
CMD ["./pandora-backend"]

