"""
FileTools — 文件操作工具集

提供给 Agent 使用的文件读写工具，适配 CHS 书目体系的目录结构。
"""

import json
import os
from typing import Any, Dict, Optional

from pydantic import Field


class ReadChapterTool:
    """读取指定书目的章节内容"""

    name: str = "read_chapter"
    description: str = "读取指定书目的章节内容。参数: book_id(str), chapter_id(str), version(str='latest')"

    def __init__(self, books_root: str = "/home/user/books"):
        self.books_root = books_root

    def execute(self, book_id: str, chapter_id: str, version: str = "latest") -> Dict[str, Any]:
        base = os.path.join(self.books_root, "books", book_id)
        if not os.path.exists(base):
            return {"success": False, "error": f"书目目录不存在: {base}"}

        if version == "latest":
            # 按优先级查找: final > v2 > v1 > 无版本号
            for suffix in ["_final.md", "_v2.md", "_v1.md", ".md"]:
                path = os.path.join(base, f"{chapter_id}{suffix}")
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    return {
                        "success": True,
                        "path": path,
                        "content": content,
                        "word_count": len(content),
                        "version": suffix.replace(".md", "").lstrip("_") or "base",
                    }
        else:
            path = os.path.join(base, f"{chapter_id}_{version}.md")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                return {"success": True, "path": path, "content": content, "word_count": len(content)}

        return {"success": False, "error": f"章节文件不存在: {book_id}/{chapter_id}"}


class WriteChapterTool:
    """写入章节内容"""

    name: str = "write_chapter"
    description: str = "写入章节内容到指定书目。参数: book_id(str), chapter_id(str), content(str), version(str='v1')"

    def __init__(self, books_root: str = "/home/user/books"):
        self.books_root = books_root

    def execute(
        self, book_id: str, chapter_id: str, content: str, version: str = "v1"
    ) -> Dict[str, Any]:
        dir_path = os.path.join(self.books_root, "books", book_id)
        os.makedirs(dir_path, exist_ok=True)

        filename = f"{chapter_id}_{version}.md" if version != "final" else f"{chapter_id}_final.md"
        path = os.path.join(dir_path, filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "success": True,
            "path": path,
            "word_count": len(content),
            "version": version,
        }


class ReadProgressTool:
    """读取书目进度"""

    name: str = "read_progress"
    description: str = "读取指定书目的写作进度。参数: book_id(str)"

    def __init__(self, books_root: str = "/home/user/books"):
        self.books_root = books_root

    def execute(self, book_id: str) -> Dict[str, Any]:
        path = os.path.join(self.books_root, "progress", f"BK{book_id}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return {"success": True, "progress": json.load(f)}
        return {"success": False, "error": f"进度文件不存在: {path}"}


class UpdateProgressTool:
    """更新书目进度"""

    name: str = "update_progress"
    description: str = "更新书目的章节进度。参数: book_id(str), chapter_id(str), status(str), word_count(int)"

    def __init__(self, books_root: str = "/home/user/books"):
        self.books_root = books_root

    def execute(
        self, book_id: str, chapter_id: str,
        status: str = "completed", word_count: int = 0,
        review_scores: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        path = os.path.join(self.books_root, "progress", f"BK{book_id}.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"book_id": book_id, "book_title": "", "total_chapters": 0, "chapters": {}}

        from datetime import datetime
        data["chapters"][chapter_id] = {
            "status": status,
            "word_count": word_count,
            "review_passed": status == "completed",
            "review_scores": review_scores or {},
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
        }

        # 更新总进度
        total = data.get("total_chapters", 16) or 16
        completed = sum(1 for ch in data["chapters"].values() if ch.get("status") == "completed")
        data["overall_progress"] = f"{completed / total * 100:.1f}%"

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return {"success": True, "overall_progress": data["overall_progress"]}


class ReadGlossaryTool:
    """读取术语表"""

    name: str = "read_glossary"
    description: str = "读取术语表或符号表。参数: type('cn'|'en'|'symbols')"

    def __init__(self, books_root: str = "/home/user/books"):
        self.books_root = books_root

    def execute(self, type: str = "cn") -> Dict[str, Any]:
        file_map = {
            "cn": "terminology/glossary_cn.md",
            "en": "terminology/glossary_en.md",
            "symbols": "terminology/symbols.md",
        }
        rel_path = file_map.get(type, file_map["cn"])
        path = os.path.join(self.books_root, rel_path)

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return {"success": True, "content": f.read(), "path": path}
        return {"success": False, "error": f"文件不存在: {path}"}
