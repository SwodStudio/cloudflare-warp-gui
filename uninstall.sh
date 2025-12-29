#!/bin/bash

set -e

APP_NAME="CloudflareWarpGUI"
VENV_DIR=".venv"
DESKTOP_FILE="${HOME}/.local/share/applications/${APP_NAME}.desktop"
ICON_PATH_DEST="${HOME}/.local/share/icons/${APP_NAME}.png"

echo "Starting uninstallation for ${APP_NAME}..."

if [ -d "${VENV_DIR}" ]; then
  echo "Removing virtual environment '${VENV_DIR}'..."
  deactivate 2>/dev/null || true
  rm -rf "${VENV_DIR}"
else
  echo "Virtual environment '${VENV_DIR}' not found, skipping removal."
fi

if [ -f "${DESKTOP_FILE}" ]; then
  echo "Removing desktop entry '${DESKTOP_FILE}'..."
  rm "${DESKTOP_FILE}"
  echo "Updating desktop database..."
  update-desktop-database "${HOME}/.local/share/applications/"
else
  echo "Desktop entry '${DESKTOP_FILE}' not found, skipping removal."
fi

if [ -f "${ICON_PATH_DEST}" ]; then
  echo "Removing icon '${ICON_PATH_DEST}'..."
  rm "${ICON_PATH_DEST}"
else
  echo "Icon '${ICON_PATH_DEST}' not found, skipping removal."
fi

echo "Uninstallation script completed."
echo "${APP_NAME} has been uninstalled."
