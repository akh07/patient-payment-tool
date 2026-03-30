#!/bin/bash
cd "$(dirname "$0")"
python3 -c "import pypdf" 2>/dev/null     || pip3 install pypdf --break-system-packages -q
python3 -c "import reportlab" 2>/dev/null || pip3 install reportlab --break-system-packages -q
python3 app.py
