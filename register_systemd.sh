#!/bin/bash
SERVICE_NAME="uestc-auto-login"
SCRIPT_NAME="always_online.py"

if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root or use sudo."
    exit 1
fi

PYTHON_PATH=$(which python3)
if [ -z "$PYTHON_PATH" ]; then
    echo "Python 3 is not detected, please install it first."
    exit 1
fi

SCRIPT_PATH="$(realpath "$(dirname "$0")/$SCRIPT_NAME")"
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Script file not found: $SCRIPT_PATH"
    exit 1
fi

WORK_DIR=$(dirname "$SCRIPT_PATH")
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

if [ -f "$SERVICE_FILE" ]; then
    echo "Service file ${SERVICE_FILE} already exists."
    exit 1
fi


echo "Creating systemd service file: ${SERVICE_FILE}..."

cat > "$SERVICE_FILE" << EOF
[Unit]
Description=UESTC Auto Network Login Service
After=network.target

[Service]
Type=simple
ExecStart=${PYTHON_PATH} ${SCRIPT_PATH}
WorkingDirectory=${WORK_DIR}
Restart=always
RestartSec=5
TimeoutStopSec=1

[Install]
WantedBy=multi-user.target
EOF

echo "Reloading systemd..."
systemctl daemon-reload

echo "Starting the service and setting it to auto-start..."
systemctl enable "$SERVICE_NAME"
systemctl restart "$SERVICE_NAME"

echo "Use the command to check the running status: sudo systemctl status $SERVICE_NAME"
