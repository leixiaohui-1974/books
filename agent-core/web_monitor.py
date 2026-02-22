#!/usr/bin/env python3
"""
OpenClaw Agent Core - Web监控界面
简单的HTTP服务器，用于监控OCAC运行状态
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from datetime import datetime

class OCACWebHandler(BaseHTTPRequestHandler):
    """Web请求处理器"""
    
    def do_GET(self):
        """处理GET请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/':
            self._serve_dashboard()
        elif path == '/api/tasks':
            self._serve_api_tasks()
        elif path == '/api/status':
            self._serve_api_status()
        else:
            self._serve_404()
    
    def _serve_dashboard(self):
        """服务监控面板"""
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>OCAC 监控面板</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stat-card h3 { margin: 0 0 10px 0; color: #666; font-size: 14px; text-transform: uppercase; }
        .stat-card .value { font-size: 32px; font-weight: bold; color: #4CAF50; }
        .tasks { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-top: 20px; }
        .tasks h2 { margin-top: 0; color: #333; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f8f8f8; font-weight: 600; color: #666; }
        tr:hover { background: #f5f5f5; }
        .status { padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 500; }
        .status-completed { background: #e8f5e9; color: #2e7d32; }
        .status-running { background: #fff3e0; color: #ef6c00; }
        .status-prepared { background: #e3f2fd; color: #1565c0; }
        .status-failed { background: #ffebee; color: #c62828; }
        .refresh { float: right; background: #4CAF50; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
        .refresh:hover { background: #45a049; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 OCAC 监控面板 <button class="refresh" onclick="location.reload()">刷新</button></h1>
        
        <div class="stats">
            <div class="stat-card">
                <h3>总任务数</h3>
                <div class="value" id="total-tasks">-</div>
            </div>
            <div class="stat-card">
                <h3>已完成</h3>
                <div class="value" id="completed-tasks">-</div>
            </div>
            <div class="stat-card">
                <h3>运行中</h3>
                <div class="value" id="running-tasks">-</div>
            </div>
            <div class="stat-card">
                <h3>失败</h3>
                <div class="value" id="failed-tasks">-</div>
            </div>
        </div>
        
        <div class="tasks">
            <h2>📋 最近任务</h2>
            <table>
                <thead>
                    <tr>
                        <th>任务ID</th>
                        <th>描述</th>
                        <th>状态</th>
                        <th>子任务数</th>
                        <th>时间</th>
                    </tr>
                </thead>
                <tbody id="task-list">
                    <tr><td colspan="5">加载中...</td></tr>
                </tbody>
            </table>
        </div>
    </div>
    
    <script>
        // 加载任务数据
        fetch('/api/tasks')
            .then(r => r.json())
            .then(data => {
                document.getElementById('total-tasks').textContent = data.total;
                document.getElementById('completed-tasks').textContent = data.completed;
                document.getElementById('running-tasks').textContent = data.running;
                document.getElementById('failed-tasks').textContent = data.failed;
                
                const tbody = document.getElementById('task-list');
                tbody.innerHTML = data.tasks.map(t => `
                    <tr>
                        <td>${t.id}</td>
                        <td>${t.description}</td>
                        <td><span class="status status-${t.status}">${t.status}</span></td>
                        <td>${t.subtasks}</td>
                        <td>${t.time}</td>
                    </tr>
                `).join('');
            });
        
        // 自动刷新
        setInterval(() => location.reload(), 30000);
    </script>
</body>
</html>"""
        
        self._send_response(200, 'text/html', html.encode())
    
    def _serve_api_tasks(self):
        """API: 任务列表"""
        work_dir = "/root/.openclaw/workspace/books/agent-runs"
        
        tasks = []
        total = completed = running = failed = 0
        
        if os.path.exists(work_dir):
            for f in sorted(os.listdir(work_dir), reverse=True):
                if f.endswith('_result.json'):
                    try:
                        with open(f"{work_dir}/{f}") as fp:
                            data = json.load(fp)
                        
                        status = data.get('status', 'unknown')
                        total += 1
                        if status == 'completed':
                            completed += 1
                        elif status == 'running':
                            running += 1
                        elif status == 'failed':
                            failed += 1
                        
                        tasks.append({
                            "id": data.get('task_id', 'unknown')[:20],
                            "description": data.get('task_description', '')[:50] + '...',
                            "status": status,
                            "subtasks": data.get('subtask_count', 0),
                            "time": data.get('timestamp', 'N/A')[:19]
                        })
                    except:
                        pass
        
        response = {
            "total": total,
            "completed": completed,
            "running": running,
            "failed": failed,
            "tasks": tasks[:10]  # 最近10个
        }
        
        self._send_response(200, 'application/json', json.dumps(response).encode())
    
    def _serve_api_status(self):
        """API: 系统状态"""
        status = {
            "status": "running",
            "version": "2.0",
            "timestamp": datetime.now().isoformat(),
            "features": ["task_decomposition", "workflow", "sessions_spawn", "scheduler", "web_ui"]
        }
        self._send_response(200, 'application/json', json.dumps(status).encode())
    
    def _serve_404(self):
        """404页面"""
        self._send_response(404, 'text/plain', b'Not Found')
    
    def _send_response(self, code: int, content_type: str, data: bytes):
        """发送响应"""
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(data))
        self.end_headers()
        self.wfile.write(data)
    
    def log_message(self, format, *args):
        """覆盖日志方法"""
        pass  # 静默日志


class OCACWebServer:
    """OCAC Web服务器"""
    
    def __init__(self, port: int = 8080):
        self.port = port
        self.server: Optional[HTTPServer] = None
    
    def start(self):
        """启动Web服务器"""
        self.server = HTTPServer(('0.0.0.0', self.port), OCACWebHandler)
        print(f"🌐 OCAC Web监控界面已启动")
        print(f"   访问地址: http://localhost:{self.port}")
        print(f"   API地址: http://localhost:{self.port}/api/tasks")
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """停止Web服务器"""
        if self.server:
            self.server.shutdown()
            print("\n⏹️  Web服务器已停止")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='OCAC Web Monitor')
    parser.add_argument('--port', '-p', type=int, default=8080, help='端口号')
    
    args = parser.parse_args()
    
    server = OCACWebServer(port=args.port)
    server.start()
