#!/usr/bin/env python3
"""
T2-CN《水网觉醒》— Nano Banana Pro 图片生成（kie.ai + Google 官方 双支持）
========================================================================
依赖：pip install requests pillow

方案 A — kie.ai 中转站（推荐，便宜稳定）：
  $env:NB_API_KEY  = "你的kie.ai API Key"
  $env:NB_API_BASE = "https://api.kie.ai"
  $env:NB_MODEL    = "nano-banana-pro"
  python generate_images_api.py --all --update-md

方案 B — Google 官方 API：
  $env:NB_API_KEY  = "AIzaSy..."
  $env:NB_API_BASE = "https://generativelanguage.googleapis.com/v1beta"
  $env:NB_MODEL    = "gemini-3-pro-image-preview"
  python generate_images_api.py --all --update-md
"""

import os, sys, json, time, base64, argparse
from pathlib import Path

# ─── 配置 ─────────────────────────────────────────────────────────────────────
BOOK_DIR   = Path(__file__).parent
MANIFEST   = BOOK_DIR / "image_manifest.json"
OUTPUT_DIR = BOOK_DIR / "H"

API_KEY  = os.environ.get("NB_API_KEY", "")
API_BASE = os.environ.get("NB_API_BASE", "https://api.kie.ai")
MODEL    = os.environ.get("NB_MODEL", "nano-banana-pro")

# 重试配置
MAX_RETRIES     = 3      # 网络错误最多重试3次
RETRY_DELAY     = 5      # 重试间隔秒数
REQUEST_TIMEOUT = 180    # 单次请求超时（图片生成较慢）

# kie.ai 轮询配置
POLL_INTERVAL_FAST  = 3
POLL_INTERVAL_SLOW  = 8
POLL_TIMEOUT        = 300

STYLE_PREFIX = (
    "Clean flat infographic illustration. Color palette: deep navy blue (#0A1E3C) background "
    "with cyan (#00C5F0) and white (#FFFFFF) primary elements, amber (#F5A623) accents. "
    "No decorative borders. Chinese water engineering context. "
    "Text labels if needed should be in Simplified Chinese. "
    "Professional technical publication quality. "
)

CHAPTER_OPENERS = {
    "fig_ch00_opener": {
        "title": "引子章节扉页",
        "prompt_en": (
            "Interior of a Chinese water dispatch control room at night during a rainstorm. "
            "A lone operator sits before multiple glowing blue monitoring screens showing water level "
            "curves, dam cross-sections, and alarm indicators. Rain streaks across a large window behind "
            "him. The screens cast blue glow on his worried face. Red warning lights flash on some screens. "
            "Outside, lightning illuminates a reservoir dam. Cinematic illustration, moody lighting. "
            "No text. 16:9."
        ),
        "file": "H/fig_ch00_opener.png",
        "chapter": "00",
        "type": "opener"
    },
    "fig_ch01_opener": {
        "title": "第一章扉页：五代人生",
        "prompt_en": (
            "A horizontal timeline showing five generations of water engineering evolution, left to right: "
            "(1) Ancient Chinese water gauge stone pillar; (2) 1950s mechanical chart recorder; "
            "(3) 1990s SCADA control room with CRT monitors; (4) 2010s digital dashboard; "
            "(5) Futuristic holographic water network display with AI indicators glowing blue. "
            "Connected by a river transforming from muddy brown to digital cyan. "
            "Clean infographic illustration, panorama. No text. 16:9."
        ),
        "file": "H/fig_ch01_opener.png",
        "chapter": "01",
        "type": "opener"
    },
}


# ─── 带重试的 HTTP 请求 ───────────────────────────────────────────────────────
def _robust_post(url, payload, headers, timeout=REQUEST_TIMEOUT):
    """带自动重试的 POST 请求，处理 SSL/网络错误"""
    import requests
    from requests.exceptions import SSLError, ConnectionError, Timeout

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
            return resp.json()
        except (SSLError, ConnectionError, Timeout) as e:
            err_name = type(e).__name__
            if attempt < MAX_RETRIES:
                wait = RETRY_DELAY * attempt
                print(f"  ⚠️  {err_name}，{wait}秒后重试 ({attempt}/{MAX_RETRIES})...")
                time.sleep(wait)
            else:
                print(f"  ❌ {err_name}，已重试{MAX_RETRIES}次仍失败")
                return {"error": {"code": 0, "message": str(e)[:200]}}
        except Exception as e:
            print(f"  ❌ 请求异常: {e}")
            return {"error": {"code": 0, "message": str(e)[:200]}}

    return {"error": {"code": 0, "message": "未知错误"}}


def _robust_get(url, params, headers, timeout=30):
    """带自动重试的 GET 请求"""
    import requests
    from requests.exceptions import SSLError, ConnectionError, Timeout

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=timeout)
            return resp.json()
        except (SSLError, ConnectionError, Timeout) as e:
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY * attempt)
            else:
                return None
        except:
            return None
    return None


# ─── 判断 API 类型 ────────────────────────────────────────────────────────────
def is_google_direct():
    return "googleapis" in API_BASE

def is_kie_ai():
    return "kie.ai" in API_BASE


# ─── kie.ai 异步任务 API ──────────────────────────────────────────────────────
def call_kie_ai(prompt: str, output_path: Path) -> bool:
    base = API_BASE.rstrip("/")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # ── 步骤 1：提交任务 ──
    create_url = f"{base}/api/v1/jobs/createTask"
    payload = {
        "model": MODEL,
        "input": {
            "prompt": prompt,
            "image_input": [],
            "aspect_ratio": "16:9",
            "resolution": "1K",
            "output_format": "png"
        }
    }

    data = _robust_post(create_url, payload, headers, timeout=30)

    if "error" in data and "code" not in data:
        return False
    if data.get("code") != 200:
        print(f"  ❌ 提交任务错误: code={data.get('code')}, msg={data.get('msg','')}")
        return False

    task_id = data.get("data", {}).get("taskId", "")
    if not task_id:
        print(f"  ❌ 未返回 taskId: {data}")
        return False

    print(f"  📤 任务已提交: {task_id}")

    # ── 步骤 2：轮询等待结果 ──
    poll_url = f"{base}/api/v1/jobs/recordInfo"
    start = time.time()
    attempt = 0

    while True:
        elapsed = time.time() - start
        if elapsed > POLL_TIMEOUT:
            print(f"  ❌ 超时 ({POLL_TIMEOUT}s)，taskId={task_id}")
            return False

        interval = POLL_INTERVAL_FAST if elapsed < 30 else POLL_INTERVAL_SLOW
        time.sleep(interval)
        attempt += 1

        result = _robust_get(poll_url, {"taskId": task_id}, headers)
        if result is None:
            print(f"  ⚠️  查询网络错误，重试...")
            continue

        if result.get("code") != 200:
            continue

        state = result.get("data", {}).get("state", "")
        elapsed_s = int(elapsed)

        if state == "success":
            result_json_str = result["data"].get("resultJson", "")
            try:
                result_json = json.loads(result_json_str)
            except:
                print(f"  ❌ 无法解析 resultJson: {result_json_str[:200]}")
                return False

            urls = result_json.get("resultUrls", [])
            if not urls:
                print(f"  ❌ 无图片 URL")
                return False

            print(f"  ⬇️  下载图片 ({elapsed_s}s)...")
            return _download_image(urls[0], output_path)

        elif state == "fail":
            fail_msg = result["data"].get("failMsg", "未知错误")
            print(f"  ❌ 生成失败: {fail_msg}")
            return False

        else:
            if attempt % 3 == 0:
                print(f"  ⏳ {state}... ({elapsed_s}s)")


def _download_image(url: str, output_path: Path) -> bool:
    import requests
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, timeout=60)
            if resp.status_code == 200 and len(resp.content) > 1000:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(resp.content)
                return True
            print(f"  ❌ 下载失败: 状态码={resp.status_code}, 大小={len(resp.content)}")
            return False
        except Exception as e:
            if attempt < MAX_RETRIES:
                print(f"  ⚠️  下载重试 ({attempt}/{MAX_RETRIES})...")
                time.sleep(RETRY_DELAY)
            else:
                print(f"  ❌ 下载失败: {e}")
                return False
    return False


# ─── Google 官方 API ──────────────────────────────────────────────────────────
def call_google_api(prompt: str, output_path: Path) -> bool:
    if "imagen" in MODEL.lower():
        return _call_imagen_predict(prompt, output_path)
    else:
        return _call_gemini_generate(prompt, output_path)


def _call_imagen_predict(prompt: str, output_path: Path) -> bool:
    url = f"{API_BASE.rstrip('/')}/models/{MODEL}:predict?key={API_KEY}"
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {"sampleCount": 1, "aspectRatio": "16:9", "outputMimeType": "image/png"}
    }
    headers = {"Content-Type": "application/json"}
    data = _robust_post(url, payload, headers)

    if "error" in data:
        err = data["error"]
        print(f"  ❌ API错误 {err.get('code')}: {err.get('message','')[:200]}")
        return False
    try:
        b64 = data["predictions"][0]["bytesBase64Encoded"]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(base64.b64decode(b64))
        return True
    except (KeyError, IndexError) as e:
        print(f"  ❌ 解析响应失败: {e}")
        return False


def _call_gemini_generate(prompt: str, output_path: Path) -> bool:
    url = f"{API_BASE.rstrip('/')}/models/{MODEL}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}
    }
    headers = {"Content-Type": "application/json"}
    data = _robust_post(url, payload, headers)

    if "error" in data:
        err = data.get("error", data)
        if isinstance(err, dict):
            print(f"  ❌ API错误 {err.get('code')}: {err.get('message','')[:200]}")
        else:
            print(f"  ❌ API错误: {str(err)[:200]}")
        return False
    try:
        parts = data["candidates"][0]["content"]["parts"]
        for part in parts:
            if "inlineData" in part:
                img_bytes = base64.b64decode(part["inlineData"]["data"])
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(img_bytes)
                return True
        print(f"  ⚠️  API返回成功但无图片数据")
        return False
    except (KeyError, IndexError) as e:
        print(f"  ❌ 解析响应失败: {e}")
        return False


# ─── 统一调度 ─────────────────────────────────────────────────────────────────
def generate_one_image(prompt: str, output_path: Path) -> bool:
    if is_google_direct():
        return call_google_api(prompt, output_path)
    else:
        return call_kie_ai(prompt, output_path)


# ─── 工具函数 ──────────────────────────────────────────────────────────────────
def load_manifest():
    data = {}
    if MANIFEST.exists():
        data = json.load(open(MANIFEST, encoding='utf-8'))
    data.update(CHAPTER_OPENERS)
    return data


def build_prompt(item: dict) -> str:
    if "prompt_en" in item:
        return STYLE_PREFIX + item["prompt_en"]
    return STYLE_PREFIX + "Draw this infographic: " + item.get("prompt_zh", "")


def generate_image(key: str, item: dict, force: bool = False) -> bool:
    output_path = BOOK_DIR / item["file"]
    if output_path.exists() and not force:
        if output_path.stat().st_size > 20 * 1024:
            print(f"  ⏭️  跳过 (已有 {output_path.stat().st_size//1024}KB)")
            return True

    prompt = build_prompt(item)
    print(f"  🎨 {item['title']}")
    print(f"     提示词: {prompt[:80]}...")

    ok = generate_one_image(prompt, output_path)

    if ok:
        sz = output_path.stat().st_size // 1024 if output_path.exists() else 0
        print(f"  ✅ 保存 {item['file']} ({sz}KB)")

    # 不管成功失败，短暂等待避免频率限制
    time.sleep(2)
    return ok


def update_chapter_md(chapter: str, manifest: dict):
    ch_files = [f for f in BOOK_DIR.glob(f"ch{chapter.lstrip('0') or '0'}*.md")
                if "_v1" not in f.name and "_backup" not in f.name]
    if not ch_files:
        # 章节 .md 文件不存在，自动创建图片索引文件
        images_for_ch = {k: v for k, v in manifest.items() if v.get("chapter") == chapter}
        if not images_for_ch:
            print(f"  ⚠️  第{chapter}章无图片记录，跳过")
            return
        ch_file = BOOK_DIR / f"ch{chapter.zfill(2)}_images.md"
        ch_num = int(chapter)
        lines = [f"# 第{ch_num}章 图片索引\n\n"]
        for key, item in sorted(images_for_ch.items()):
            fig_id = item.get("fig_id", key)
            title = item["title"]
            filename = Path(item["file"]).name
            # 使用相对路径，本地和 GitHub 均可正确渲染
            rel_path = f"H/{filename}"
            lines.append(
                f"\n**{fig_id}　{title}**\n\n"
                f"![{fig_id} {title}]({rel_path})\n"
                f"*{title}*\n"
            )
        ch_file.write_text("".join(lines), encoding='utf-8')
        print(f"  📄 已创建图片索引 {ch_file.name}（{len(images_for_ch)} 张）")
        return
    ch_file = ch_files[0]
    text = ch_file.read_text(encoding='utf-8')
    changed = False
    for key, item in manifest.items():
        if item.get("chapter") != chapter:
            continue
        fig_id = item.get("fig_id", key)
        title = item["title"]
        filename = Path(item["file"]).name
        github_raw = (
            f"https://raw.githubusercontent.com/leixiaohui-1974/books"
            f"/main/books/T2-CN/H/{filename}"
        )
        new_img = f"\n**{fig_id}　{title}**\n\n![{fig_id} {title}]({github_raw})\n*{title}*\n"
        for old in [f"![图{fig_id.replace('图','')}](H/{filename})",
                    f"![图{fig_id.replace('图','')}]({github_raw})"]:
            if old in text:
                text = text.replace(old, new_img)
                changed = True
    if changed:
        ch_file.write_text(text, encoding='utf-8')
        print(f"  💾 已更新 {ch_file.name}")
    else:
        print(f"  ℹ️  {ch_file.name} 无需更新（占位符未匹配）")


# ─── CLI ──────────────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="T2-CN 图片生成 (Nano Banana Pro / Gemini)")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--all",     action="store_true")
    g.add_argument("--chapter", help="章节号，如 01")
    g.add_argument("--keys",    nargs="+")
    g.add_argument("--list",    action="store_true")
    p.add_argument("--force",     action="store_true")
    p.add_argument("--update-md", action="store_true")
    p.add_argument("--dry-run",   action="store_true")
    args = p.parse_args()

    if not API_KEY and not args.list and not args.dry_run:
        print("❌ 未设置 NB_API_KEY")
        print()
        print("方案 A — kie.ai 中转站（推荐）：")
        print('  $env:NB_API_KEY  = "你的kie.ai API Key"')
        print('  $env:NB_API_BASE = "https://api.kie.ai"')
        print('  $env:NB_MODEL    = "nano-banana-pro"')
        print()
        print("方案 B — Google 官方 API：")
        print('  $env:NB_API_KEY  = "AIzaSy..."')
        print('  $env:NB_API_BASE = "https://generativelanguage.googleapis.com/v1beta"')
        print('  $env:NB_MODEL    = "gemini-3-pro-image-preview"')
        sys.exit(1)

    manifest = load_manifest()

    if args.list:
        print(f"共 {len(manifest)} 张图片：")
        for k, v in sorted(manifest.items()):
            p2 = BOOK_DIR / v['file']
            sz = p2.stat().st_size // 1024 if p2.exists() else 0
            st = f"✅{sz}KB" if sz > 20 else ("📄占位" if p2.exists() else "❌未生成")
            print(f"  {st:10s} {k:30s} Ch{v['chapter']} {v['title'][:25]}")
        return

    if args.all:
        targets = dict(manifest)
    elif args.chapter:
        ch = args.chapter.zfill(2)
        targets = {k: v for k, v in manifest.items() if v.get("chapter") == ch}
    else:
        targets = {k: manifest[k] for k in args.keys if k in manifest}

    api_type = "Google 官方" if is_google_direct() else ("kie.ai 异步任务" if is_kie_ai() else "中转站")
    print(f"📋 待生成：{len(targets)} 张")
    print(f"   API:  {API_BASE} ({api_type})")
    print(f"   模型: {MODEL}")
    print(f"   重试: 网络错误自动重试 {MAX_RETRIES} 次")
    print()

    ok_n, fail = 0, []
    for i, (key, item) in enumerate(sorted(targets.items()), 1):
        print(f"[{i}/{len(targets)}] {key}")
        if args.dry_run:
            print(f"  提示词: {build_prompt(item)[:150]}...")
            continue
        if generate_image(key, item, args.force):
            ok_n += 1
        else:
            fail.append(key)
        print()

    print("=" * 50)
    print(f"✅ 成功: {ok_n}  ❌ 失败: {len(fail)}")
    if fail:
        print(f"失败: {fail}")
        print(f"\n💡 可以单独重新生成失败的：")
        print(f"   python generate_images_api.py --keys {' '.join(fail)}")

    if args.update_md and ok_n > 0:
        print("\n📝 更新 Markdown...")
        for ch in sorted(set(v["chapter"] for v in targets.values())):
            update_chapter_md(ch, targets)


if __name__ == "__main__":
    main()
