# 拿到m3e-base向量模型吗，置于工程目录m3e-base目录下
# 劳动法智能问答系统

基于向量检索+中文大模型的企业智能问答系统。

## 启动方式

1. 安装依赖
   pip install -r requirements.txt

2. 启动开发服务器
   uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 1

3. 后台运行（部署）
   nohup uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 1 > app.log 2>&1 &

4. 配置 Systemd 服务 (参考 deploy/qa-api.service)

5. 配置 Nginx 反向代理 (参考 deploy/nginx.conf)

6. 使用前端
   - 打开 frontend/simple_ui.html 文件，输入你的服务器IP。

## 接口说明

- POST /qa/ ： 提交问题，返回答案。# 劳动法智能问答系统

