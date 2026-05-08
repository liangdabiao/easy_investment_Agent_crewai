#!/bin/bash
# Build script for A股智能分析系统 UI

echo "Building A股智能分析系统 UI..."

# Build for current platform
echo "Building for current platform..."
go build -o stock-analysis-ui

# Build for Windows (64-bit)
echo "Building for Windows (64-bit)..."
GOOS=windows GOARCH=amd64 go build -o stock-analysis-ui-windows-amd64.exe

# Build for Linux (64-bit)
echo "Building for Linux (64-bit)..."
GOOS=linux GOARCH=amd64 go build -o stock-analysis-ui-linux-amd64

# Build for macOS (64-bit Intel)
echo "Building for macOS (Intel)..."
GOOS=darwin GOARCH=amd64 go build -o stock-analysis-ui-darwin-amd64

# Build for macOS (ARM64/M1)
echo "Building for macOS (Apple Silicon)..."
GOOS=darwin GOARCH=arm64 go build -o stock-analysis-ui-darwin-arm64

echo "Build complete! Executables:"
ls -lh stock-analysis-ui*
