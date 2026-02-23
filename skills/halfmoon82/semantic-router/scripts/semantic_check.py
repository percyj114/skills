#!/usr/bin/env python3
"""
Semantic Router - 可配置的语义检查与模型路由脚本
支持从配置文件读取模型池和任务类型
支持自动模型切换 (--execute / -e)
"""

import json
import sys
import os
import subprocess
import argparse
from datetime import datetime

# 获取技能目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'config')

# 默认配置目录（兼容直接运行）
if not os.path.exists(CONFIG_DIR):
    CONFIG_DIR = os.path.expanduser('~/.openclaw/workspace/.lib')

def load_json(filename, default=None):
    """加载 JSON 配置文件"""
    path = os.path.join(CONFIG_DIR, filename)
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Warning: Failed to load {filename}: {e}", file=sys.stderr)
    return default or {}

# 加载配置
MODEL_POOLS = load_json('pools.json', {})
TASK_PATTERNS = load_json('tasks.json', {})

# 备用硬编码（配置文件不存在时）
if not MODEL_POOLS:
    MODEL_POOLS = {
        "Intelligence": {"name": "智能池", "primary": "openai-codex/gpt-5.3-codex", "fallback_1": "kimi-k2.5", "fallback_2": "minimax-cn/MiniMax-M2.5"},
        "Highspeed": {"name": "高速池", "primary": "openai/gpt-4o-mini", "fallback_1": "glm-4.7-flashx", "fallback_2": "minimax-cn/MiniMax-M2.5"},
        "Humanities": {"name": "人文池", "primary": "openai/gpt-4o", "fallback_1": "kimi-k2.5", "fallback_2": "minimax-cn/MiniMax-M2.5"}
    }

if not TASK_PATTERNS:
    TASK_PATTERNS = {
        "continue": {"keywords": ["继续", "接着"], "pool": None, "action": "延续"},
        "development": {"keywords": ["开发", "写代码"], "pool": "Intelligence", "action": "执行开发任务"},
    }

# 指示词配置
CONTINUATION_INDICATORS = {
    "pronouns": ["这个", "那个", "它", "这", "那"],
    "supplements": ["还有", "另外", "继续", "补充"],
    "confirmations": ["对的", "是的", "好的"]
}

def keyword_match(user_input: str):
    """关键词匹配"""
    text = user_input.lower().strip()
    
    for task_type, config in TASK_PATTERNS.items():
        is_standalone = config.get("standalone", False)
        
        for kw in config.get("keywords", []):
            if is_standalone:
                if text == kw or text.startswith(kw + " ") or text.startswith(kw + "?"):
                    return task_type, config.get("action"), config.get("pool"), task_type == "continue"
            else:
                if kw in text:
                    return task_type, config.get("action"), config.get("pool"), task_type == "continue"
    
    return None, None, None, False

def indicator_match(user_input: str) -> bool:
    """指示词检测"""
    text = user_input.lower().strip()
    for indicators in CONTINUATION_INDICATORS.values():
        for indicator in indicators:
            if indicator in text:
                return True
    return False

def jaccard_similarity(text1: str, text2: str) -> float:
    """Jaccard 相似度"""
    import re
    tokens1 = set(re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', text1.lower()))
    tokens2 = set(re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', text2.lower()))
    if not tokens1 or not tokens2:
        return 0.0
    intersection = len(tokens1 & tokens2)
    union = len(tokens1 | tokens2)
    return intersection / union if union > 0 else 0.0

def embedding_similarity_check(user_input: str, context_messages: list, threshold: float = 0.1) -> tuple:
    """词汇重叠度检测"""
    if not context_messages:
        return False, 0.0, "no_context"
    
    context_text = " ".join(context_messages)
    score = jaccard_similarity(user_input, context_text)
    return score >= threshold, score, "embedding_jaccard"

def detect_task_type(user_input: str, context_messages: list = None):
    """检测任务类型"""
    # Step 1: 关键词匹配
    task_type, action, pool, is_continue = keyword_match(user_input)
    
    if task_type:
        branch = "B" if is_continue else "C"
        detection = "keyword_continue" if is_continue else "keyword"
        return task_type, action, pool, branch, detection
    
    # Step 2: 指示词
    if indicator_match(user_input):
        return "continue", "延续", None, "B", "indicator"
    
    # Step 3: 相似度
    is_continue, score, method = embedding_similarity_check(user_input, context_messages or [], threshold=0.1)
    if is_continue:
        return "continue", "延续", None, "B", method
    
    # 默认: 信息检索
    default_task = TASK_PATTERNS.get("info_retrieval", {})
    return "info_retrieval", default_task.get("action", "执行信息检索"), "Highspeed", "C", "default"

def get_pool_info(pool_name: str):
    if pool_name and pool_name in MODEL_POOLS:
        return MODEL_POOLS[pool_name]
    return None

def get_current_pool():
    return os.environ.get("CURRENT_POOL", "Highspeed")

def generate_declaration(result: dict, current_pool: str) -> str:
    task_type = result["task_type"]
    action = result["action"]
    pool_name = result.get("pool_name")
    primary_model = result.get("primary_model")
    
    if task_type == "continue":
        return f"{action} 保持当前模型池【{current_pool}】"
    else:
        return f"{action} 新会话 应使用{pool_name} 已切换为{primary_model}"

def build_context_archive_prompt():
    return """[上下文截止符] 之前的对话已归档。从本条消息开始作为新的上下文起点。"""

def execute_model_switch(model: str) -> bool:
    """执行模型切换"""
    try:
        # 尝试多种调用方式
        commands = [
            ["/Users/macmini/.local/share/fnm/node-versions/v24.13.0/installation/bin/openclaw", "session_status", "--model", model],
            ["openclaw", "session_status", "--model", model],
            ["session_status", "--model", model],
        ]
        
        for cmd in commands:
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    print(f"✅ Model switched to: {model}", file=sys.stderr)
                    return True
            except FileNotFoundError:
                continue
            except Exception as e:
                print(f"⚠️ Cmd {cmd} failed: {e}", file=sys.stderr)
                continue
        
        print(f"❌ Failed to switch model: session_status not found", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Error executing model switch: {e}", file=sys.stderr)
        return False

def execute_fallback_chain(primary: str, fallback_1: str = None, fallback_2: str = None) -> dict:
    """
    执行 Fallback 回路
    返回: {"attempted": [...], "success": bool, "current_model": str}
    """
    results = {
        "attempted": [],
        "success": False,
        "current_model": primary
    }
    
    models_to_try = [primary]
    if fallback_1:
        models_to_try.append(fallback_1)
    if fallback_2:
        models_to_try.append(fallback_2)
    
    for model in models_to_try:
        print(f"🔄 Trying model: {model}", file=sys.stderr)
        results["attempted"].append(model)
        
        if execute_model_switch(model):
            results["success"] = True
            results["current_model"] = model
            print(f"✅ Fallback success: {model}", file=sys.stderr)
            return results
    
    print(f"❌ All fallback attempts failed", file=sys.stderr)
    return results

def main():
    parser = argparse.ArgumentParser(description="Semantic Router - 模型路由脚本")
    parser.add_argument("user_input", nargs="?", help="用户输入消息")
    parser.add_argument("current_pool", nargs="?", help="当前模型池")
    parser.add_argument("context_messages", nargs="*", help="上下文消息列表")
    parser.add_argument("-e", "--execute", action="store_true", help="自动执行模型切换（主模型）")
    parser.add_argument("-f", "--fallback", action="store_true", help="执行 Fallback 回路（主模型失败时自动切换备用）")
    
    args = parser.parse_args()
    
    # 如果没有参数，显示用法
    if len(sys.argv) < 2:
        print("Usage: semantic_check.py <user_input> [current_pool] [context1] [context2] ...] [-e|--execute] [-f|--fallback]")
        print("Example: semantic_check.py '查一下天气' 'Intelligence' -e")
        print("Example: semantic_check.py --fallback 'openai/gpt-4o-mini' 'glm-4.7-flashx' 'MiniMax-M2.5'")
        sys.exit(1)
    
    # Fallback 模式：手动指定模型链
    if args.fallback:
        fallback_models = []
        if args.user_input:
            fallback_models.append(args.user_input)
        if args.current_pool:
            fallback_models.append(args.current_pool)
        fallback_models.extend(args.context_messages)
        
        fallback_results = execute_fallback_chain(
            fallback_models[0] if len(fallback_models) > 0 else None,
            fallback_models[1] if len(fallback_models) > 1 else None,
            fallback_models[2] if len(fallback_models) > 2 else None
        )
        print(json.dumps(fallback_results, ensure_ascii=False, indent=2))
        return
    
    user_input = args.user_input
    current_pool = args.current_pool if args.current_pool else get_current_pool()
    context_messages = args.context_messages if args.context_messages else []
    
    task_type, action, pool_name, branch, detection = detect_task_type(user_input, context_messages)
    pool_info = get_pool_info(pool_name)
    
    # 判断是否需要切换模型
    need_switch = (task_type != "continue" and pool_info and pool_info.get("primary"))
    target_model = pool_info.get("primary") if need_switch else None
    
    result = {
        "branch": branch,
        "task_type": task_type,
        "action": action,
        "pool": pool_name,
        "pool_name": pool_info.get("name") if pool_info else None,
        "primary_model": target_model,
        "fallback_1": pool_info.get("fallback_1") if pool_info else None,
        "fallback_2": pool_info.get("fallback_2") if pool_info else None,
        "need_archive": branch == "C",
        "need_reset": task_type == "new_session",
        "need_switch": need_switch,
        "detection_method": detection,
        "fallback_chain": [target_model, pool_info.get("fallback_1"), pool_info.get("fallback_2")] if pool_info else [],
        "declaration": None,
        "context_cutoff_prompt": build_context_archive_prompt() if branch == "C" else None,
        "auto_executed": False
    }
    
    result["declaration"] = generate_declaration(result, current_pool)
    
    # 如果需要切换且启用了自动执行
    if need_switch and args.execute and target_model:
        print(f"🔄 Auto-switching model to: {target_model}", file=sys.stderr)
        success = execute_model_switch(target_model)
        result["auto_executed"] = success
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
