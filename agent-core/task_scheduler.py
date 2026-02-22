#!/usr/bin/env python3
"""
OpenClaw Agent Core - 任务调度器
支持定时任务、批量调度、任务依赖管理
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from threading import Thread, Event

class TaskScheduler:
    """任务调度器 - 支持定时和周期性任务"""
    
    def __init__(self, work_dir: str = "/root/.openclaw/workspace/books/agent-scheduler"):
        self.work_dir = work_dir
        self.scheduled_tasks: Dict[str, Dict] = {}
        self.running = False
        self.scheduler_thread: Optional[Thread] = None
        self.stop_event = Event()
        os.makedirs(work_dir, exist_ok=True)
        self._load_scheduled_tasks()
    
    def schedule_once(self, task_id: str, task_description: str, 
                      run_at: datetime, callback: Optional[Callable] = None) -> Dict:
        """
        调度一次性任务
        
        Args:
            task_id: 任务ID
            task_description: 任务描述
            run_at: 执行时间
            callback: 回调函数
        """
        task = {
            "id": task_id,
            "description": task_description,
            "type": "once",
            "run_at": run_at.isoformat(),
            "status": "scheduled",
            "created_at": datetime.now().isoformat(),
            "callback": callback
        }
        
        self.scheduled_tasks[task_id] = task
        self._save_scheduled_tasks()
        
        print(f"⏰ 任务已调度: {task_id}")
        print(f"   执行时间: {run_at}")
        
        return task
    
    def schedule_recurring(self, task_id: str, task_description: str,
                          interval_minutes: int, callback: Optional[Callable] = None) -> Dict:
        """
        调度周期性任务
        
        Args:
            task_id: 任务ID
            task_description: 任务描述
            interval_minutes: 间隔（分钟）
            callback: 回调函数
        """
        task = {
            "id": task_id,
            "description": task_description,
            "type": "recurring",
            "interval_minutes": interval_minutes,
            "last_run": None,
            "next_run": (datetime.now() + timedelta(minutes=interval_minutes)).isoformat(),
            "status": "scheduled",
            "created_at": datetime.now().isoformat(),
            "callback": callback
        }
        
        self.scheduled_tasks[task_id] = task
        self._save_scheduled_tasks()
        
        print(f"🔄 周期性任务已调度: {task_id}")
        print(f"   间隔: {interval_minutes}分钟")
        print(f"   下次执行: {task['next_run']}")
        
        return task
    
    def start(self):
        """启动调度器"""
        if self.running:
            print("调度器已在运行")
            return
        
        self.running = True
        self.stop_event.clear()
        self.scheduler_thread = Thread(target=self._scheduler_loop)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        
        print("✅ 任务调度器已启动")
    
    def stop(self):
        """停止调度器"""
        if not self.running:
            return
        
        self.stop_event.set()
        self.running = False
        
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        
        print("⏹️  任务调度器已停止")
    
    def _scheduler_loop(self):
        """调度器主循环"""
        while not self.stop_event.is_set():
            now = datetime.now()
            
            for task_id, task in list(self.scheduled_tasks.items()):
                if task["status"] != "scheduled":
                    continue
                
                if task["type"] == "once":
                    run_at = datetime.fromisoformat(task["run_at"])
                    if now >= run_at:
                        self._execute_task(task_id)
                
                elif task["type"] == "recurring":
                    next_run = datetime.fromisoformat(task["next_run"])
                    if now >= next_run:
                        self._execute_task(task_id)
                        # 更新下次执行时间
                        task["last_run"] = now.isoformat()
                        task["next_run"] = (now + timedelta(
                            minutes=task["interval_minutes"]
                        )).isoformat()
                        self._save_scheduled_tasks()
            
            # 每秒检查一次
            time.sleep(1)
    
    def _execute_task(self, task_id: str):
        """执行任务"""
        task = self.scheduled_tasks.get(task_id)
        if not task:
            return
        
        print(f"\n🚀 执行调度任务: {task_id}")
        print(f"   描述: {task['description']}")
        
        task["status"] = "running"
        task["started_at"] = datetime.now().isoformat()
        
        try:
            # 调用回调函数或默认执行
            if task.get("callback"):
                result = task["callback"](task)
            else:
                # 默认：调用OCAC执行
                result = self._default_execute(task)
            
            task["status"] = "completed"
            task["result"] = result
            task["completed_at"] = datetime.now().isoformat()
            
            print(f"   ✅ 任务完成")
            
        except Exception as e:
            task["status"] = "failed"
            task["error"] = str(e)
            print(f"   ❌ 任务失败: {e}")
        
        # 一次性任务完成后移除
        if task["type"] == "once":
            task["status"] = "completed"
        
        self._save_scheduled_tasks()
    
    def _default_execute(self, task: Dict) -> Dict:
        """默认执行方式 - 调用OCAC"""
        # 导入OCAC
        from ocac_v2 import OCAC
        
        ocac = OCAC()
        result = ocac.run(
            task_description=task["description"],
            task_id=task["id"],
            execute=True
        )
        
        return result
    
    def list_tasks(self) -> List[Dict]:
        """列出所有调度任务"""
        return [
            {
                "id": tid,
                "description": t["description"],
                "type": t["type"],
                "status": t["status"],
                "next_run": t.get("next_run", t.get("run_at", "N/A"))
            }
            for tid, t in self.scheduled_tasks.items()
        ]
    
    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        if task_id in self.scheduled_tasks:
            self.scheduled_tasks[task_id]["status"] = "cancelled"
            self._save_scheduled_tasks()
            print(f"🚫 任务已取消: {task_id}")
            return True
        return False
    
    def _save_scheduled_tasks(self):
        """保存调度任务到文件"""
        # 移除不可序列化的callback
        save_data = {}
        for tid, task in self.scheduled_tasks.items():
            save_data[tid] = {k: v for k, v in task.items() if k != "callback"}
        
        filepath = f"{self.work_dir}/scheduled_tasks.json"
        with open(filepath, 'w') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
    
    def _load_scheduled_tasks(self):
        """从文件加载调度任务"""
        filepath = f"{self.work_dir}/scheduled_tasks.json"
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                self.scheduled_tasks = json.load(f)


# 命令行接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='OCAC Task Scheduler')
    parser.add_argument('action', choices=['schedule', 'list', 'cancel', 'daemon'], help='操作')
    parser.add_argument('--id', '-i', help='任务ID')
    parser.add_argument('--task', '-t', help='任务描述')
    parser.add_argument('--at', help='执行时间 (格式: YYYY-MM-DD HH:MM)')
    parser.add_argument('--interval', '-n', type=int, help='间隔（分钟）')
    
    args = parser.parse_args()
    
    scheduler = TaskScheduler()
    
    if args.action == 'schedule':
        if not args.id or not args.task:
            print("错误: 需要 --id 和 --task 参数")
            exit(1)
        
        if args.at:
            # 一次性任务
            run_at = datetime.strptime(args.at, "%Y-%m-%d %H:%M")
            scheduler.schedule_once(args.id, args.task, run_at)
        elif args.interval:
            # 周期性任务
            scheduler.schedule_recurring(args.id, args.task, args.interval)
        else:
            print("错误: 需要 --at 或 --interval 参数")
            exit(1)
    
    elif args.action == 'list':
        tasks = scheduler.list_tasks()
        print(f"\n📋 调度任务列表 ({len(tasks)}个)\n")
        for t in tasks:
            icon = "⏰" if t["type"] == "once" else "🔄"
            print(f"{icon} {t['id']}: {t['description'][:40]}...")
            print(f"   状态: {t['status']} | 下次: {t['next_run']}\n")
    
    elif args.action == 'cancel':
        if not args.id:
            print("错误: 需要 --id 参数")
            exit(1)
        scheduler.cancel_task(args.id)
    
    elif args.action == 'daemon':
        # 启动守护进程
        scheduler.start()
        print("按 Ctrl+C 停止调度器")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            scheduler.stop()
