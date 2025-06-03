# 劳动法智能问答系统

基于国产向量检索 + 智谱GLM-4大模型智能问答，支持劳动法领域专业知识问答。

---

## 🚀 项目架构

- 后端：FastAPI
- 知识库：FAISS 向量数据库
- 大模型：GLM-4 API（可切换通义千问、百川等国产大模型）
- 前端：简单版 ChatGPT 风格网页
- 部署：Nginx + Systemd
- 支持 HTTPS (Let’s Encrypt 免费证书)

---

## 📦 快速部署指南

### 克隆项目
```
git clone https://github.com/RoyZhang2022/labor-law-RAG.git
```

1. 到hugging face去下载moka-ai/m3e-base向量检索模型，将其放置于m3e-base目录下。

2. 安装依赖
创建虚拟环境并安装：

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. 配置环境变量
新建 .env 文件（推荐），或者直接编辑：

```
sudo nano /etc/qa-api.env
```

写入你的智谱API Key：

GLM4_API_KEY=你的真实APIKey

4. 配置 Systemd 服务
新建 qa-api.service 文件：
```
sudo nano /etc/systemd/system/qa-api.service
```

填入以下内容（注意路径根据实际情况调整）：
```
[Unit]
Description=QA API Service
After=network.target

[Service]
User=你的Linux用户名
WorkingDirectory=/home/你的用户名/项目路径/labor-law-qa-project
ExecStart=/home/你的用户名/项目路径/venv/bin/uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 1
EnvironmentFile=/etc/qa-api.env
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

5. 配置 Nginx
```
sudo apt update
sudo apt install nginx -y
```

创建 Nginx 配置文件：
```
sudo nano /etc/nginx/sites-available/qa-api
```

内容如下：
```
server {
    listen 80;
    server_name _;

    location / {
        root /var/www/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /qa/ {
        proxy_pass http://127.0.0.1:8000/qa/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

启用站点并重启 Nginx：
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/qa-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

6. 部署前端网页
```
sudo mkdir -p /var/www/html
sudo cp frontend/simple_ui.html /var/www/html/index.html
```

7. 启动后端服务
```
sudo systemctl daemon-reload
sudo systemctl enable qa-api
sudo systemctl start qa-api
```

8. 浏览器访问
打开浏览器，访问你的服务器公网IP：
http://你的服务器IP/
输入问题，比如：

```
劳动合同最长可以签多久？
```

✅ 即可返回专业回答。

常见问题 FAQ
```
问题 | 解决办法
500 Internal Server Error | 确认 .env 配置了正确的 API Key，确认服务器能出网
网页提交没响应	| 检查浏览器 Network 请求，确认返回 200
向量检索无结果 | 确认知识库已构建完成，FAISS index 正常
```

TODO List
```
 支持本地部署版 Qwen2-1.5B 微型模型

 支持聊天历史记录上下文

 支持Docker一键打包部署

 后台管理界面：上传新知识文件，自动增量向量更新
```

作者
RoyZhang2022
高级版劳动法智能问答系统
