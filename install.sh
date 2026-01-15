#!/bin/bash
# Boopster install script for Termux (Android)

set -e

echo "🐍 Installing Python..."
pkg update -y
pkg install -y python

echo "📦 Installing dependencies..."
pip install websockets pystun3

echo "📥 Downloading boopster..."
curl -sL https://raw.githubusercontent.com/benthayer/tcp-hole-punch/master/boopster.py -o boopster.py

echo "✅ Done! Run with: python boopster.py"

