#!/bin/bash

set -e

# 检查是否传入参数
if [ -z "$1" ]; then
  echo "❌ 错误: 你需要在执行时提供 GLM4_API_KEY！"
  echo "正确用法: bash setup.sh YOUR_GLM4_API_KEY"
  exit 1
fi

API_KEY="$1"

# 安装必要组件
sudo apt update
sudo apt install nginx -y

# 配置 Nginx
NGINX_CONF=/etc/nginx/sites-available/qa-api
if [ ! -f "$NGINX_CONF" ]; then
    echo "🔧 正在创建 Nginx 配置..."
    sudo tee "$NGINX_CONF" > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location / {
        root /var/www/html;
        index index.html;
        try_files \$uri \$uri/ /index.html;
    }

    location /qa/ {
        proxy_pass http://127.0.0.1:8000/qa/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
fi

# 禁用默认站点
if [ -e /etc/nginx/sites-enabled/default ]; then
    sudo rm -f /etc/nginx/sites-enabled/default
fi

# 建立新的软链接
if [ ! -L /etc/nginx/sites-enabled/qa-api ]; then
    sudo ln -s /etc/nginx/sites-available/qa-api /etc/nginx/sites-enabled/
fi

# 部署前端网页
sudo mkdir -p /var/www/html
sudo cp -f ../frontend/simple_ui.html /var/www/html/index.html

# 重启 Nginx
sudo nginx -t && sudo systemctl restart nginx

# 配置环境变量文件
echo "🔧 写入 API Key 到 /etc/qa-api.env..."
echo "GLM4_API_KEY=$API_KEY" | sudo tee /etc/qa-api.env > /dev/null

# 配置 Systemd
SYSTEMD_CONF=/etc/systemd/system/qa-api.service
if [ ! -f "$SYSTEMD_CONF" ]; then
    echo "🔧 正在创建 Systemd 配置..."
    sudo tee "$SYSTEMD_CONF" > /dev/null <<EOF
[Unit]
Description=QA API Service
After=network.target

[Service]
User=$USER
WorkingDirectory=$(pwd)/..
ExecStart=$(pwd)/../venv/bin/uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 1
EnvironmentFile=/etc/qa-api.env
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
fi

# 启动并设置开机自启
sudo systemctl daemon-reload
sudo systemctl enable qa-api
sudo systemctl restart qa-api

echo "✅ 部署完成！请访问 http://你的服务器IP/"

