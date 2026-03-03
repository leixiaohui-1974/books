#!/usr/bin/env python3
"""
通用 AI 图片生成框架 v2.0
========================
支持多 API 提供商（插件式），所有配置外置，跨项目通用。

用法:
  python generate_images_api.py --all                        # 跳过已有图片
  python generate_images_api.py --all --mode overwrite       # 覆盖（旧图备份为 _old）
  python generate_images_api.py --all --mode regenerate      # 强制重新生成（不备份）
  python generate_images_api.py --chapter 01                 # 只生成第1章
  python generate_images_api.py --keys fig_ch01_1            # 只生成指定 key
  python generate_images_api.py --list                       # 列出所有图片状态
  python generate_images_api.py --all --dry-run              # 预览，不实际生成
  python generate_images_api.py --all --update-md            # 生成后更新 Markdown
  python generate_images_api.py --project-dir ../T1-CN       # 指定项目目录
  python generate_images_api.py --manifest custom.json --all # 指定清单文件
  python generate_images_api.py --type opener --all          # 只生成扉页/只生成内图
  python generate_images_api.py --status missing --all       # 只生成缺失的图片
  python generate_images_api.py --init-project               # 初始化项目配置模板

配置优先级:
  命令行参数 > 项目配置(image_project.json) > .env文件 > 环境变量 > 默认值

.env 配置:
  NB_API_KEY   = sk-xxx 或 AIzaSy...
  NB_API_BASE  = https://api.kie.ai | https://generativelanguage.googleapis.com/v1beta
  NB_MODEL     = nano-banana-pro | gemini-3-pro-image-preview
  NB_STYLE     = 自定义风格前缀（可选）
  NB_RETRIES   = 3
  NB_TIMEOUT   = 180
  NB_POLL_MAX  = 300
  NB_COOLDOWN  = 2
"""

import os, sys, json, time, base64, argparse, shutil, abc, re
from pathlib import Path
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# 第一层：配置加载（支持多来源、分层优先级）
# ═══════════════════════════════════════════════════════════════════════════════

def _load_env_file(env_path):
    """加载 .env 文件到环境变量（不覆盖已有）"""
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k not in os.environ:
                os.environ[k] = v


def _load_project_config(project_dir):
    """加载项目配置文件"""
    config_file = project_dir / "image_project.json"
    if config_file.exists():
        try:
            return json.load(open(config_file, encoding="utf-8"))
        except Exception as e:
            print(f"⚠️  加载项目配置失败: {e}")
    return {}


# 默认风格模板库
STYLE_TEMPLATES = {
    "chinese_engineering": (
        "Clean flat infographic illustration for a Chinese engineering textbook "
        "(print and digital). Color palette: white (#FFFFFF) or very light gray "
        "(#F7F9FC) background, deep navy blue (#0A2558) for primary text and "
        "structural elements, teal/cyan (#0096C7) for highlights and data, amber "
        "(#F5A623) for warnings and emphasis. All body text and labels must be "
        "large enough to read clearly when printed at A4 size. No dark or colored "
        "backgrounds behind main content areas. Chinese water engineering context. "
        "All text labels must be in Simplified Chinese, minimum readable font size. "
        "Professional Chinese technical publication quality, suitable for both "
        "screen and print. "
    ),
    "academic_neutral": (
        "Clean professional academic illustration suitable for textbook publication. "
        "White or light gray background, navy blue primary elements, clear labels "
        "in the appropriate language. Professional quality for both screen and print. "
    ),
    "modern_tech": (
        "Modern technology-themed illustration with dark navy background, "
        "cyan and electric blue accents, clean geometric shapes. "
        "Futuristic but professional tone. "
    ),
    "minimal": "",
}


class Config:
    """集中配置，支持多来源叠加"""
    # 以下为运行时动态设置的属性
    API_KEY = ""
    API_BASE = "https://api.kie.ai"
    MODEL = "nano-banana-pro"
    RETRIES = 3
    TIMEOUT = 180
    POLL_MAX = 300
    COOLDOWN = 2
    RETRY_DELAY = 5
    STYLE_PREFIX = ""

    # 项目相关（由 init() 动态设置）
    PROJECT_DIR = Path(".")
    MANIFEST_FILE = Path("image_manifest.json")
    OPENERS_FILE = Path("chapter_openers.json")
    OUTPUT_DIR = Path("H")
    GITHUB_RAW_BASE = ""
    ASPECT_RATIO = "16:9"
    RESOLUTION = "1K"
    OUTPUT_FORMAT = "png"

    @classmethod
    def init(cls, args=None):
        """
        初始化配置，优先级：命令行 > 项目配置 > .env > 环境变量 > 默认值
        """
        # 1. 确定项目目录
        if args and args.project_dir:
            cls.PROJECT_DIR = Path(args.project_dir).resolve()
        else:
            cls.PROJECT_DIR = Path(__file__).parent.resolve()

        # 2. 加载 .env（先项目目录，再脚本目录）
        _load_env_file(cls.PROJECT_DIR / ".env")
        script_dir = Path(__file__).parent.resolve()
        if script_dir != cls.PROJECT_DIR:
            _load_env_file(script_dir / ".env")

        # 3. 加载项目配置
        proj = _load_project_config(cls.PROJECT_DIR)

        # 4. 合并配置（项目配置 > 环境变量 > 默认值）
        def _get(key, env_key, default, cast=str):
            # 命令行参数最高优先（由调用者后续覆盖）
            val = proj.get(key)
            if val is not None:
                return cast(val)
            val = os.environ.get(env_key)
            if val is not None:
                return cast(val)
            return cast(default) if not isinstance(default, cast) else default

        cls.API_KEY = _get("api_key", "NB_API_KEY", "")
        cls.API_BASE = _get("api_base", "NB_API_BASE", "https://api.kie.ai")
        cls.MODEL = _get("model", "NB_MODEL", "nano-banana-pro")
        cls.RETRIES = _get("retries", "NB_RETRIES", 3, int)
        cls.TIMEOUT = _get("timeout", "NB_TIMEOUT", 180, int)
        cls.POLL_MAX = _get("poll_max", "NB_POLL_MAX", 300, int)
        cls.COOLDOWN = _get("cooldown", "NB_COOLDOWN", 2, int)
        cls.ASPECT_RATIO = _get("aspect_ratio", "NB_ASPECT_RATIO", "16:9")
        cls.RESOLUTION = _get("resolution", "NB_RESOLUTION", "1K")
        cls.OUTPUT_FORMAT = _get("output_format", "NB_OUTPUT_FORMAT", "png")

        # 风格：支持模板名或自定义
        style_raw = _get("style", "NB_STYLE", "chinese_engineering")
        cls.STYLE_PREFIX = STYLE_TEMPLATES.get(style_raw, style_raw)

        # 路径配置
        cls.OUTPUT_DIR = cls.PROJECT_DIR / _get("output_dir", "NB_OUTPUT_DIR", "H")
        cls.GITHUB_RAW_BASE = _get("github_raw_base", "NB_GITHUB_RAW", "")

        # 清单文件（支持命令行覆盖）
        manifest_name = _get("manifest_file", "NB_MANIFEST", "image_manifest.json")
        if args and args.manifest:
            manifest_name = args.manifest
        cls.MANIFEST_FILE = cls.PROJECT_DIR / manifest_name

        openers_name = _get("openers_file", "NB_OPENERS", "chapter_openers.json")
        cls.OPENERS_FILE = cls.PROJECT_DIR / openers_name

    @classmethod
    def summary(cls):
        provider = ProviderRegistry.detect()
        return (
            f"   项目:    {cls.PROJECT_DIR.name}\n"
            f"   API:     {cls.API_BASE} ({provider})\n"
            f"   模型:    {cls.MODEL}\n"
            f"   重试:    网络错误自动重试 {cls.RETRIES} 次\n"
            f"   超时:    {cls.TIMEOUT}s / 轮询上限 {cls.POLL_MAX}s\n"
            f"   冷却:    每张间隔 {cls.COOLDOWN}s\n"
            f"   画幅:    {cls.ASPECT_RATIO} / {cls.RESOLUTION}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# 第二层：HTTP 工具（带自动重试）
# ═══════════════════════════════════════════════════════════════════════════════
def _http(method, url, *, json_data=None, params=None, headers=None, timeout=None):
    """统一 HTTP 请求，自动重试 SSL/网络错误"""
    import requests
    from requests.exceptions import SSLError, ConnectionError, Timeout

    timeout = timeout or Config.TIMEOUT
    for attempt in range(1, Config.RETRIES + 1):
        try:
            if method == "GET":
                resp = requests.get(url, params=params, headers=headers, timeout=timeout)
            else:
                resp = requests.post(url, json=json_data, headers=headers, timeout=timeout)
            return resp.json()
        except (SSLError, ConnectionError, Timeout) as e:
            if attempt < Config.RETRIES:
                wait = Config.RETRY_DELAY * attempt
                print(f"  ⚠️  {type(e).__name__}，{wait}s后重试 ({attempt}/{Config.RETRIES})...")
                time.sleep(wait)
            else:
                print(f"  ❌ {type(e).__name__}，已重试{Config.RETRIES}次仍失败")
                return None
        except Exception as e:
            print(f"  ❌ 请求异常: {e}")
            return None
    return None


def _download(url, output_path, timeout=60):
    """下载文件，带重试"""
    import requests
    for attempt in range(1, Config.RETRIES + 1):
        try:
            resp = requests.get(url, timeout=timeout)
            if resp.status_code == 200 and len(resp.content) > 1000:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(resp.content)
                return True
            print(f"  ❌ 下载失败: HTTP {resp.status_code}, {len(resp.content)} bytes")
            return False
        except Exception as e:
            if attempt < Config.RETRIES:
                print(f"  ⚠️  下载重试 ({attempt}/{Config.RETRIES})...")
                time.sleep(Config.RETRY_DELAY)
            else:
                print(f"  ❌ 下载失败: {e}")
                return False
    return False


# ═══════════════════════════════════════════════════════════════════════════════
# 第三层：API 提供商插件系统
# ═══════════════════════════════════════════════════════════════════════════════
class Provider(abc.ABC):
    name: str = "base"

    @staticmethod
    @abc.abstractmethod
    def match(api_base: str) -> bool: ...

    @staticmethod
    @abc.abstractmethod
    def generate(prompt: str, output_path: Path) -> bool: ...


class KieAiProvider(Provider):
    """kie.ai 异步任务 API"""
    name = "kie.ai 异步任务"

    @staticmethod
    def match(api_base): return "kie.ai" in api_base

    @staticmethod
    def generate(prompt, output_path):
        base = Config.API_BASE.rstrip("/")
        hdrs = {"Content-Type": "application/json", "Authorization": f"Bearer {Config.API_KEY}"}

        data = _http("POST", f"{base}/api/v1/jobs/createTask", json_data={
            "model": Config.MODEL,
            "input": {"prompt": prompt, "image_input": [],
                      "aspect_ratio": Config.ASPECT_RATIO,
                      "resolution": Config.RESOLUTION,
                      "output_format": Config.OUTPUT_FORMAT}
        }, headers=hdrs, timeout=30)

        if not data or data.get("code") != 200:
            print(f"  ❌ 提交任务: {(data or {}).get('msg', '请求失败')}")
            return False

        task_id = data.get("data", {}).get("taskId", "")
        if not task_id:
            print(f"  ❌ 未返回 taskId")
            return False
        print(f"  📤 taskId: {task_id}")

        poll_url = f"{base}/api/v1/jobs/recordInfo"
        start, tick = time.time(), 0
        while True:
            elapsed = time.time() - start
            if elapsed > Config.POLL_MAX:
                print(f"  ❌ 超时 ({Config.POLL_MAX}s)")
                return False
            time.sleep(3 if elapsed < 30 else 8)
            tick += 1

            result = _http("GET", poll_url, params={"taskId": task_id}, headers=hdrs, timeout=15)
            if not result or result.get("code") != 200:
                continue

            state = result["data"].get("state", "")
            if state == "success":
                try:
                    urls = json.loads(result["data"]["resultJson"]).get("resultUrls", [])
                except:
                    urls = []
                if not urls:
                    print(f"  ❌ 无图片 URL")
                    return False
                print(f"  ⬇️  下载 ({int(elapsed)}s)...")
                return _download(urls[0], output_path)
            elif state == "fail":
                print(f"  ❌ {result['data'].get('failMsg', '未知错误')}")
                return False
            elif tick % 3 == 0:
                print(f"  ⏳ {state}... ({int(elapsed)}s)")


class GoogleDirectProvider(Provider):
    """Google 官方 Gemini API"""
    name = "Google 官方"

    @staticmethod
    def match(api_base): return "googleapis" in api_base

    @staticmethod
    def generate(prompt, output_path):
        base = Config.API_BASE.rstrip("/")
        model = Config.MODEL
        hdrs = {"Content-Type": "application/json"}

        if "imagen" in model.lower():
            url = f"{base}/models/{model}:predict?key={Config.API_KEY}"
            data = _http("POST", url, json_data={
                "instances": [{"prompt": prompt}],
                "parameters": {"sampleCount": 1, "aspectRatio": Config.ASPECT_RATIO,
                               "outputMimeType": f"image/{Config.OUTPUT_FORMAT}"}
            }, headers=hdrs)
            if not data or "error" in data:
                err = (data or {}).get("error", {})
                print(f"  ❌ API: {err.get('code','')} {str(err.get('message',''))[:200]}")
                return False
            try:
                b64 = data["predictions"][0]["bytesBase64Encoded"]
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(base64.b64decode(b64))
                return True
            except (KeyError, IndexError) as e:
                print(f"  ❌ 解析失败: {e}")
                return False
        else:
            url = f"{base}/models/{model}:generateContent?key={Config.API_KEY}"
            data = _http("POST", url, json_data={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}
            }, headers=hdrs)
            if not data or "error" in data:
                err = (data or {}).get("error", {})
                print(f"  ❌ API: {err.get('code','')} {str(err.get('message',''))[:200]}")
                return False
            try:
                for part in data["candidates"][0]["content"]["parts"]:
                    if "inlineData" in part:
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        output_path.write_bytes(base64.b64decode(part["inlineData"]["data"]))
                        return True
                print(f"  ⚠️  返回成功但无图片")
                return False
            except (KeyError, IndexError) as e:
                print(f"  ❌ 解析失败: {e}")
                return False


class OpenAICompatProvider(Provider):
    """通用 OpenAI 兼容接口 (/v1/images/generations)"""
    name = "OpenAI 兼容"

    @staticmethod
    def match(api_base): return True  # 兜底

    @staticmethod
    def generate(prompt, output_path):
        url = f"{Config.API_BASE.rstrip('/')}/images/generations"
        hdrs = {"Content-Type": "application/json", "Authorization": f"Bearer {Config.API_KEY}"}
        data = _http("POST", url, json_data={
            "model": Config.MODEL, "prompt": prompt, "n": 1, "response_format": "b64_json"
        }, headers=hdrs)

        if not data or "error" in data:
            print(f"  ❌ {(data or {}).get('error', '请求失败')}")
            return False
        if "data" not in data:
            print(f"  ❌ 无 data 字段: {str(data)[:200]}")
            return False
        try:
            b64 = data["data"][0].get("b64_json")
            if b64:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(base64.b64decode(b64))
                return True
            img_url = data["data"][0].get("url")
            if img_url:
                return _download(img_url, output_path)
        except (KeyError, IndexError):
            pass
        print(f"  ❌ 无可用图片数据")
        return False


class ProviderRegistry:
    """提供商注册表，按优先级匹配"""
    _providers = [KieAiProvider, GoogleDirectProvider, OpenAICompatProvider]

    @classmethod
    def register(cls, provider_class):
        cls._providers.insert(-1, provider_class)

    @classmethod
    def get(cls):
        for p in cls._providers:
            if p.match(Config.API_BASE):
                return p
        return OpenAICompatProvider

    @classmethod
    def detect(cls): return cls.get().name


# ═══════════════════════════════════════════════════════════════════════════════
# 第四层：清单加载与提示词构建
# ═══════════════════════════════════════════════════════════════════════════════
def load_manifest():
    """加载图片清单，支持多文件合并"""
    data = {}
    if Config.MANIFEST_FILE.exists():
        try:
            data = json.load(open(Config.MANIFEST_FILE, encoding="utf-8"))
        except Exception as e:
            print(f"⚠️  加载清单失败 {Config.MANIFEST_FILE.name}: {e}")
    if Config.OPENERS_FILE.exists():
        try:
            data.update(json.load(open(Config.OPENERS_FILE, encoding="utf-8")))
        except Exception as e:
            print(f"⚠️  加载扉页清单失败: {e}")
    return data


def build_prompt(item):
    """构建完整提示词：风格前缀 + 图片描述"""
    if "prompt_en" in item:
        return Config.STYLE_PREFIX + item["prompt_en"]
    if "prompt_zh" in item:
        return Config.STYLE_PREFIX + "Draw this infographic: " + item["prompt_zh"]
    # 兼容：直接用 prompt 字段
    if "prompt" in item:
        return Config.STYLE_PREFIX + item["prompt"]
    return Config.STYLE_PREFIX + item.get("title", "untitled illustration")


def get_image_status(item):
    """获取单张图片状态"""
    fp = Config.PROJECT_DIR / item["file"]
    if not fp.exists():
        return "missing", 0
    sz = fp.stat().st_size
    if sz > 20 * 1024:
        return "ok", sz
    elif sz > 0:
        return "placeholder", sz
    return "empty", 0


# ═══════════════════════════════════════════════════════════════════════════════
# 第五层：生成控制
# ═══════════════════════════════════════════════════════════════════════════════
MODE_SKIP       = "skip"
MODE_OVERWRITE  = "overwrite"
MODE_REGENERATE = "regenerate"


def _backup_old(output_path):
    if not output_path.exists() or output_path.stat().st_size < 1024:
        return
    if output_path.stem.endswith("_old"):
        return
    old_path = output_path.with_name(f"{output_path.stem}_old{output_path.suffix}")
    if not old_path.exists():
        shutil.copy2(output_path, old_path)
        print(f"  📦 备份 → {old_path.name}")


def generate_image(key, item, mode):
    output_path = Config.PROJECT_DIR / item["file"]

    if output_path.exists() and output_path.stat().st_size > 20 * 1024:
        if mode == MODE_SKIP:
            print(f"  ⏭️  跳过 (已有 {output_path.stat().st_size // 1024}KB)")
            return True
        elif mode == MODE_OVERWRITE:
            _backup_old(output_path)

    prompt = build_prompt(item)
    print(f"  🎨 {item.get('title', key)}")
    print(f"     提示词: {prompt[:80]}...")

    provider = ProviderRegistry.get()
    ok = provider.generate(prompt, output_path)

    if ok and output_path.exists():
        print(f"  ✅ {item['file']} ({output_path.stat().st_size // 1024}KB)")

    time.sleep(Config.COOLDOWN)
    return ok


# ═══════════════════════════════════════════════════════════════════════════════
# 第六层：Markdown 更新
# ═══════════════════════════════════════════════════════════════════════════════
def update_chapter_md(chapter, manifest):
    ch_num = chapter.lstrip("0") or "0"
    patterns = [f"ch{chapter}*.md", f"ch{ch_num}*.md", f"ch{ch_num}_*.md"]
    ch_files = []
    for pat in patterns:
        ch_files.extend(
            f for f in Config.PROJECT_DIR.glob(pat)
            if not any(x in f.name for x in ["_v1", "_backup", "_old", "_images"])
        )
    ch_files = list(dict.fromkeys(ch_files))

    images_for_ch = {k: v for k, v in manifest.items() if v.get("chapter") == chapter}
    if not images_for_ch:
        return

    if not ch_files:
        idx_file = Config.PROJECT_DIR / f"ch{chapter.zfill(2)}_images.md"
        lines = [f"# 第{int(chapter)}章 图片索引\n\n"]
        for key, item in sorted(images_for_ch.items()):
            fig_id = item.get("fig_id", key)
            title = item["title"]
            rel_path = f"H/{Path(item['file']).name}"
            lines.append(f"\n**{fig_id}　{title}**\n\n![{fig_id} {title}]({rel_path})\n*{title}*\n")
        idx_file.write_text("".join(lines), encoding="utf-8")
        print(f"  📄 创建索引 {idx_file.name} ({len(images_for_ch)} 张)")
        return

    ch_file = ch_files[0]
    text = ch_file.read_text(encoding="utf-8")
    changed = False
    for key, item in images_for_ch.items():
        fig_id = item.get("fig_id", key)
        title = item["title"]
        filename = Path(item["file"]).name

        # 使用项目配置的 GitHub 地址，如果没有则用相对路径
        if Config.GITHUB_RAW_BASE:
            img_ref = f"{Config.GITHUB_RAW_BASE.rstrip('/')}/{filename}"
        else:
            img_ref = f"H/{filename}"

        new_img = f"\n**{fig_id}　{title}**\n\n![{fig_id} {title}]({img_ref})\n*{title}*\n"

        # 尝试替换已有引用
        for old_pattern in [
            f"![图{fig_id.replace('图', '')}](H/{filename})",
            f"![图{fig_id.replace('图', '')}]({img_ref})",
        ]:
            if old_pattern in text:
                text = text.replace(old_pattern, new_img)
                changed = True

    if changed:
        ch_file.write_text(text, encoding="utf-8")
        print(f"  💾 更新 {ch_file.name}")
    else:
        print(f"  ℹ️  {ch_file.name} 无需更新")


# ═══════════════════════════════════════════════════════════════════════════════
# 第七层：项目初始化
# ═══════════════════════════════════════════════════════════════════════════════
def init_project(project_dir):
    """在指定目录初始化项目配置模板"""
    config_file = project_dir / "image_project.json"
    if config_file.exists():
        print(f"⚠️  {config_file} 已存在，跳过初始化")
        return

    template = {
        "_comment": "图片生成项目配置 — 所有字段均可选，未设置则使用 .env 或默认值",
        "style": "chinese_engineering",
        "output_dir": "H",
        "aspect_ratio": "16:9",
        "resolution": "1K",
        "output_format": "png",
        "manifest_file": "image_manifest.json",
        "openers_file": "chapter_openers.json",
        "github_raw_base": "",
        "_style_options": "可选: chinese_engineering, academic_neutral, modern_tech, minimal, 或直接写自定义风格文本"
    }
    config_file.write_text(json.dumps(template, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ 已创建项目配置模板: {config_file}")

    manifest_file = project_dir / "image_manifest.json"
    if not manifest_file.exists():
        sample = {
            "fig_ch01_1": {
                "fig_id": "图1-1",
                "title": "示例图片标题",
                "prompt_zh": "示例提示词：描述你想要生成的图片内容...",
                "file": "H/fig_ch01_1.png",
                "chapter": "01",
                "type": "inline"
            }
        }
        manifest_file.write_text(json.dumps(sample, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"✅ 已创建示例清单: {manifest_file}")

    output_dir = project_dir / "H"
    output_dir.mkdir(exist_ok=True)
    print(f"✅ 已创建输出目录: {output_dir}")


# ═══════════════════════════════════════════════════════════════════════════════
# 第八层：日志记录
# ═══════════════════════════════════════════════════════════════════════════════
def write_generation_log(targets, results, mode):
    """写入生成日志"""
    log_dir = Config.PROJECT_DIR / "H"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "generation_log.jsonl"

    entry = {
        "timestamp": datetime.now().isoformat(),
        "mode": mode,
        "provider": ProviderRegistry.detect(),
        "model": Config.MODEL,
        "total": len(targets),
        "success": len([k for k, v in results.items() if v]),
        "failed": [k for k, v in results.items() if not v],
    }
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ═══════════════════════════════════════════════════════════════════════════════
# 第九层：CLI
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    p = argparse.ArgumentParser(
        description="通用 AI 图片生成框架 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "覆盖模式 (--mode):\n"
            "  skip        已有图片(>20KB)就跳过（默认）\n"
            "  overwrite   备份旧图为 _old.png，再重新生成\n"
            "  regenerate  直接覆盖，不备份\n"
            "\n"
            "示例:\n"
            "  python generate_images_api.py --all                         # 只生成缺失的\n"
            "  python generate_images_api.py --all --mode overwrite        # 全部重新生成\n"
            "  python generate_images_api.py --chapter 03                  # 只第3章\n"
            "  python generate_images_api.py --keys fig_ch01_1 fig_ch01_2  # 指定图片\n"
            "  python generate_images_api.py --list                        # 查看状态\n"
            "  python generate_images_api.py --project-dir ../T1-CN --all  # 指定项目\n"
            "  python generate_images_api.py --type opener --all           # 只生成扉页\n"
            "  python generate_images_api.py --status missing --all        # 只生成缺失的\n"
            "  python generate_images_api.py --init-project                # 初始化项目\n"
        )
    )

    # 范围选择
    scope = p.add_mutually_exclusive_group(required=True)
    scope.add_argument("--all",     action="store_true",      help="生成全部图片")
    scope.add_argument("--chapter", metavar="CH",             help="章节号，如 01、02")
    scope.add_argument("--keys",    nargs="+", metavar="KEY", help="指定 key（空格分隔）")
    scope.add_argument("--list",    action="store_true",      help="列出所有图片状态")
    scope.add_argument("--init-project", action="store_true", help="初始化项目配置模板")

    # 生成选项
    p.add_argument("--mode", choices=["skip", "overwrite", "regenerate"],
                   default="skip", help="已有图片处理方式（默认: skip）")
    p.add_argument("--update-md", action="store_true", help="生成后更新 Markdown")
    p.add_argument("--dry-run",   action="store_true", help="只打印提示词，不生成")

    # 过滤选项
    p.add_argument("--type", choices=["opener", "inline", "all"],
                   default="all", help="图片类型过滤（默认: all）")
    p.add_argument("--status", choices=["missing", "placeholder", "ok", "all"],
                   default="all", help="按状态过滤（默认: all）")

    # 项目选项
    p.add_argument("--project-dir", metavar="DIR",
                   help="项目目录路径（默认: 脚本所在目录）")
    p.add_argument("--manifest", metavar="FILE",
                   help="清单文件名（默认: image_manifest.json）")

    # 兼容旧参数
    p.add_argument("--force", action="store_true", help=argparse.SUPPRESS)

    args = p.parse_args()

    # 初始化配置
    Config.init(args)

    mode = args.mode
    if args.force and mode == "skip":
        mode = MODE_OVERWRITE

    # 初始化项目
    if args.init_project:
        init_project(Config.PROJECT_DIR)
        return

    if not Config.API_KEY and not args.list and not args.dry_run:
        print("❌ 未设置 NB_API_KEY\n")
        print("方法一：在 .env 文件中添加：")
        print("  NB_API_KEY  = 你的API密钥")
        print("  NB_API_BASE = https://api.kie.ai")
        print("  NB_MODEL    = nano-banana-pro")
        print("\n方法二：在 image_project.json 中配置")
        print("\n方法三：设置环境变量 NB_API_KEY")
        sys.exit(1)

    manifest = load_manifest()

    if not manifest:
        print(f"❌ 未找到图片清单文件: {Config.MANIFEST_FILE}")
        print(f"   运行 --init-project 初始化项目配置")
        sys.exit(1)

    # ── 列出状态 ──
    if args.list:
        print(f"📁 项目: {Config.PROJECT_DIR.name}")
        print(f"共 {len(manifest)} 张图片：\n")
        by_ch = {}
        for k, v in sorted(manifest.items()):
            by_ch.setdefault(v.get("chapter", "??"), []).append((k, v))

        stats = {"ok": 0, "missing": 0, "placeholder": 0}
        for ch in sorted(by_ch):
            label = int(ch) if ch.isdigit() else ch
            print(f"  ── 第{label}章 ({len(by_ch[ch])} 张) ──")
            for k, v in by_ch[ch]:
                status, sz = get_image_status(v)
                stats[status] = stats.get(status, 0) + 1
                if status == "ok":
                    st = f"✅{sz//1024}KB"
                elif status == "placeholder":
                    st = "📄占位"
                else:
                    st = "❌缺失"
                type_tag = f"[{v.get('type','?'):6s}]" if v.get('type') else ""
                print(f"    {st:10s} {type_tag} {k:30s} {v.get('title','')[:28]}")
            print()

        print(f"统计: ✅完成 {stats['ok']}  ❌缺失 {stats['missing']}  📄占位 {stats.get('placeholder',0)}")
        return

    # ── 筛选目标 ──
    if args.all:
        targets = dict(manifest)
    elif args.chapter:
        ch = args.chapter.zfill(2)
        targets = {k: v for k, v in manifest.items() if v.get("chapter") == ch}
    else:
        targets = {k: manifest[k] for k in args.keys if k in manifest}
        missing = [k for k in (args.keys or []) if k not in manifest]
        if missing:
            print(f"⚠️  未找到: {missing}")

    # 类型过滤
    if args.type != "all":
        targets = {k: v for k, v in targets.items() if v.get("type") == args.type}

    # 状态过滤
    if args.status != "all":
        filtered = {}
        for k, v in targets.items():
            s, _ = get_image_status(v)
            if s == args.status:
                filtered[k] = v
        targets = filtered

    if not targets:
        print("没有匹配的目标图片。")
        return

    mode_label = {"skip": "跳过已有", "overwrite": "覆盖（备份旧图）", "regenerate": "强制覆盖"}
    print(f"📁 项目: {Config.PROJECT_DIR.name}")
    print(f"📋 待处理：{len(targets)} 张 | 模式: {mode_label.get(mode, mode)}")
    print(Config.summary())
    print()

    ok_n, fail = 0, []
    results = {}
    for i, (key, item) in enumerate(sorted(targets.items()), 1):
        print(f"[{i}/{len(targets)}] {key}")
        if args.dry_run:
            print(f"  提示词: {build_prompt(item)[:150]}...")
            print()
            continue
        ok = generate_image(key, item, mode)
        results[key] = ok
        if ok:
            ok_n += 1
        else:
            fail.append(key)
        print()

    print("=" * 55)
    print(f"  ✅ 成功: {ok_n}  ❌ 失败: {len(fail)}")
    if fail:
        print(f"  失败: {fail}")
        print(f"\n  💡 重试:")
        print(f"     python generate_images_api.py --keys {' '.join(fail)}")

    # 写日志
    if results:
        write_generation_log(targets, results, mode)

    if args.update_md and ok_n > 0:
        print(f"\n📝 更新 Markdown...")
        for ch in sorted(set(v["chapter"] for v in targets.values())):
            update_chapter_md(ch, targets)


if __name__ == "__main__":
    main()
