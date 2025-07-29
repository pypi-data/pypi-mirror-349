"""
🔴 App
🔵 DB
🟢 ROUTING
💪 SERVICE
⚠️ WARN
❌ ERROR
✅ CHECK
"""

from datetime import datetime

ICON = {
    "App": "🟣",
    "DB": "🔵",
    "ROUTING": "⚪️",
    "SERVICE": "🛠️",
    "WARN": "⚠️",
    "ERROR": "❌",
    "CHECK": "✅"
}

def log(icon: str, message: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{icon} [{now}] {message}", flush=True)