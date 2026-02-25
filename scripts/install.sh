#!/usr/bin/env bash
set -euo pipefail

# ── SomeNotify Installer ─────────────────────────────────────
# curl -fsSL <raw-url>/install.sh | sudo bash
# ──────────────────────────────────────────────────────────────

REPO_URL="https://github.com/RP38/SomeNotify.git"
INSTALL_DIR="/opt/somenotify"
SERVICE_USER="somenotify"
SERVICE_NAME="somenotify"
VENV_DIR="${INSTALL_DIR}/venv"

# ── Helpers ───────────────────────────────────────────────────

info()  { printf '\033[1;34m[INFO]\033[0m  %s\n' "$*"; }
warn()  { printf '\033[1;33m[WARN]\033[0m  %s\n' "$*"; }
error() { printf '\033[1;31m[ERROR]\033[0m %s\n' "$*" >&2; exit 1; }

require_root() {
    if [[ $EUID -ne 0 ]]; then
        error "This script must be run as root (use sudo)."
    fi
}

require_cmd() {
    command -v "$1" &>/dev/null || error "'$1' is required but not found. Please install it first."
}

# ── Pre-flight checks ────────────────────────────────────────

require_root
require_cmd git
require_cmd python3

info "Starting SomeNotify installation..."

# ── Create service user ──────────────────────────────────────

if id "$SERVICE_USER" &>/dev/null; then
    info "User '${SERVICE_USER}' already exists, skipping."
else
    info "Creating system user '${SERVICE_USER}'..."
    useradd --system --no-create-home --shell /usr/sbin/nologin "$SERVICE_USER"
fi

# ── Clone repository ─────────────────────────────────────────

if [[ -d "$INSTALL_DIR" ]]; then
    info "Directory ${INSTALL_DIR} already exists, pulling latest changes..."
    git -C "$INSTALL_DIR" pull --ff-only || warn "Could not fast-forward; keeping existing code."
else
    info "Cloning repository into ${INSTALL_DIR}..."
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# ── Set up Python virtual environment ────────────────────────

info "Creating virtual environment..."
python3 -m venv "$VENV_DIR"

info "Installing dependencies..."
"${VENV_DIR}/bin/pip" install --upgrade pip --quiet
"${VENV_DIR}/bin/pip" install -r "${INSTALL_DIR}/requirements.txt" --quiet

# ── Configuration ─────────────────────────────────────────────

if [[ ! -f "${INSTALL_DIR}/.env" ]]; then
    info "Creating default .env from .env.example..."
    cp "${INSTALL_DIR}/.env.example" "${INSTALL_DIR}/.env"
    warn "Edit ${INSTALL_DIR}/.env to configure your backend credentials."
else
    info ".env already exists, keeping current configuration."
fi

# ── Permissions ───────────────────────────────────────────────

info "Setting ownership to ${SERVICE_USER}..."
chown -R "${SERVICE_USER}:${SERVICE_USER}" "$INSTALL_DIR"
chmod 600 "${INSTALL_DIR}/.env"

# ── Systemd unit ──────────────────────────────────────────────

UNIT_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

info "Installing systemd service..."
cat > "$UNIT_FILE" <<EOF
[Unit]
Description=SomeNotify — HTTP notification gateway
After=network.target

[Service]
Type=simple
User=${SERVICE_USER}
Group=${SERVICE_USER}
WorkingDirectory=${INSTALL_DIR}
ExecStart=${VENV_DIR}/bin/python3 ${INSTALL_DIR}/server.py
Restart=on-failure
RestartSec=5

# Security hardening
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=${INSTALL_DIR}
PrivateTmp=true

# Allow binding to privileged ports (< 1024) without running as root
AmbientCapabilities=CAP_NET_BIND_SERVICE
CapabilityBoundingSet=CAP_NET_BIND_SERVICE

# Environment
EnvironmentFile=${INSTALL_DIR}/.env

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable "$SERVICE_NAME"

# ── Done ──────────────────────────────────────────────────────

info "Installation complete!"
info ""
info "Next steps:"
info "  1. Edit configuration:  sudo nano ${INSTALL_DIR}/.env"
info "  2. Start the service:   sudo systemctl start ${SERVICE_NAME}"
info "  3. Check status:        sudo systemctl status ${SERVICE_NAME}"
info "  4. View logs:           sudo journalctl -u ${SERVICE_NAME} -f"
