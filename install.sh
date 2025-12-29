#!/bin/bash

set -e

APP_NAME="CloudflareWarpGUI"
VENV_DIR=".venv"
DESKTOP_FILE="${HOME}/.local/share/applications/${APP_NAME}.desktop"
ICON_PATH_SOURCE="./screenshot/Cloudflare Warp.png"
ICON_PATH_DEST="${HOME}/.local/share/icons/${APP_NAME}.png"

echo "Starting installation for ${APP_NAME}..."

echo "Checking Python 3 and venv ..."
if ! command -v python3 &>/dev/null; then
  echo "Error: python3 is not installed. Please install Python 3 to proceed."
  exit 1
fi

if ! python3 -c "import venv" &>/dev/null; then
  echo "Error: Python venv module is not available. Please ensure it's installed"
  exit 1
fi

# venv
echo "Creating virtual environment in ${VENV_DIR}..."
python3 -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"

echo "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Virtual environment created and dependencies installed."

INSTALL_DIR="$(pwd)"

echo "Copying icon to ${ICON_PATH_DEST}..."
mkdir -p "$(dirname "${ICON_PATH_DEST}")"
cp "${ICON_PATH_SOURCE}" "${ICON_PATH_DEST}"

echo "Creating desktop entry at ${DESKTOP_FILE}..."
mkdir -p "$(dirname "${DESKTOP_FILE}")"
cat >"${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=${APP_NAME}
Comment=Cloudflare Warp GUI
Exec=${INSTALL_DIR}/${VENV_DIR}/bin/python ${INSTALL_DIR}/main.py
Icon=${ICON_PATH_DEST}
Terminal=false
Type=Application
Categories=Internet;
EOF

chmod +x "${DESKTOP_FILE}"

echo "Updating desktop database..."
update-desktop-database "${HOME}/.local/share/applications/"

echo "Installation script completed."
echo "${APP_NAME} is installed. You should find it in your applications menu."
