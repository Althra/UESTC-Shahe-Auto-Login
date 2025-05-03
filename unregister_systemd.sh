#!/bin/bash
SERVICE_NAME="uestc-auto-login"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root or use sudo."
    exit 1
fi

if [ -f "$SERVICE_FILE" ]; then
    systemctl stop "$SERVICE_NAME"
    systemctl disable "$SERVICE_NAME"
    echo "Deleting service files: $SERVICE_FILE"
    rm "$SERVICE_FILE"
else
    echo "Service file does not exist: $SERVICE_FILE"
fi

systemctl daemon-reload

echo "Service was successfully deleted: $SERVICE_NAME"
