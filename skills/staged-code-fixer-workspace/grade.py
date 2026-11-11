#!/usr/bin/env python3
# @author Claude Code (kimi-3)

"""
为 staged-code-fixer 的评测结果自动打分。

用法：
    python grade.py <workspace>/iteration-N
"""

import json
import os
import re
import sys
from pathlib import Path


def load_text(path: Path) -> str:
    """读取文本文件，不存在时返回空字符串。"""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def check_file_exists(path: Path) -> tuple[bool, str]:
    """检查文件是否存在。"""
    if path.exists():
        return True, f"文件存在: {path}"
    return False, f"文件不存在: {path}"


def grade_magic_number(run_dir: Path) -> list[dict]:
    """对 magic-number 评测用例打分。"""
    code_path = run_dir / "outputs" / "trainorder.js"
    report_path = run_dir / "outputs" / "report.md"
    code = load_text(code_path)
    report = load_text(report_path)

    results = []

    # 1. 文件存在
    passed, evidence = check_file_exists(code_path)
    results.append({"text": "outputs/trainorder.js 文件存在且可读", "passed": passed, "evidence": evidence})

    # 2. 定义了常量
    has_constant = bool(re.search(r"ORDER_STATUS_(CANCELED|CANCELLED|CANCEL)\s*=\s*8", code))
    results.append({
        "text": "trainorder.js 中定义了订单取消状态常量（如 ORDER_STATUS_CANCELED）",
        "passed": has_constant,
        "evidence": "找到常量定义" if has_constant else "未找到 ORDER_STATUS_CANCELED = 8 形式的常量定义"
    })

    # 3. 不再直接使用魔法数字 8
    direct_magic = bool(re.search(r"status\s*==\s*8|status\s*===\s*8", code))
    results.append({
        "text": "trainorder.js 中不再直接使用魔法数字 8 进行比较",
        "passed": not direct_magic,
        "evidence": "未找到 status == 8 或 status === 8" if not direct_magic else "仍找到 status == 8 或 status === 8"
    })

    # 4. 业务逻辑保持等价
    still_checks_cancelled = bool(re.search(r"status\s*==\s*ORDER_STATUS_|status\s*===\s*ORDER_STATUS_|orderStatus\s*==\s*ORDER_STATUS_|orderStatus\s*===\s*ORDER_STATUS_", code))
    results.append({
        "text": "条件判断的业务逻辑保持等价（仍然判断订单状态是否为已取消）",
        "passed": still_checks_cancelled,
        "evidence": "条件判断仍使用 ORDER_STATUS_ 常量比较" if still_checks_cancelled else "未找到使用 ORDER_STATUS_ 常量的条件判断"
    })

    # 5. 报告存在
    passed, evidence = check_file_exists(report_path)
    results.append({"text": "outputs/report.md 文件存在", "passed": passed, "evidence": evidence})

    # 6. 报告提及魔法数字
    report_mentions = "魔法数字" in report or "ORDER_STATUS_CANCELED" in report or "常量" in report
    results.append({
        "text": "report.md 中明确提到已修复魔法数字问题",
        "passed": report_mentions,
        "evidence": "报告中提到魔法数字/常量相关关键词" if report_mentions else "报告中未提到魔法数字/常量相关关键词"
    })

    return results


def grade_data_source(run_dir: Path) -> list[dict]:
    """对 data-source 评测用例打分。"""
    code_path = run_dir / "outputs" / "trainorder.js"
    report_path = run_dir / "outputs" / "report.md"
    code = load_text(code_path)
    report = load_text(report_path)

    results = []

    # 1. 文件存在
    passed, evidence = check_file_exists(code_path)
    results.append({"text": "outputs/trainorder.js 文件存在且可读", "passed": passed, "evidence": evidence})

    # 2. 统一提取 orderStatus
    has_orderstatus_var = bool(re.search(r"(var|const|let)\s+orderStatus\s*=", code))
    results.append({
        "text": "在 loadTrainDetail 函数入口处统一提取了 orderStatus 变量",
        "passed": has_orderstatus_var,
        "evidence": "找到 orderStatus 变量定义" if has_orderstatus_var else "未找到 orderStatus 变量定义"
    })

    # 3. 条件判断使用统一变量
    condition_uses_var = bool(re.search(r"if\s*\(\s*orderStatus", code))
    results.append({
        "text": "条件判断中使用统一提取的 orderStatus 变量，而不是直接使用 $orderBrief.status",
        "passed": condition_uses_var,
        "evidence": "if 条件中使用 orderStatus" if condition_uses_var else "if 条件中未使用 orderStatus"
    })

    # 4. 保留兜底逻辑
    has_fallback = "$orderBrief.status" in code and "$data.listBasic.orderStatus" in code
    results.append({
        "text": "保留了原表达式的兜底逻辑，业务逻辑真值保持不变",
        "passed": has_fallback,
        "evidence": "同时引用 $data.listBasic.orderStatus 和 $orderBrief.status，保留兜底" if has_fallback else "未同时保留两种数据来源"
    })

    # 5. 报告存在
    passed, evidence = check_file_exists(report_path)
    results.append({"text": "outputs/report.md 文件存在", "passed": passed, "evidence": evidence})

    # 6. 报告提及数据来源
    report_mentions = "数据来源" in report or "orderStatus" in report
    results.append({
        "text": "report.md 中明确提到已修复数据来源不一致问题",
        "passed": report_mentions,
        "evidence": "报告中提到数据来源/orderStatus 相关关键词" if report_mentions else "报告中未提到数据来源/orderStatus 相关关键词"
    })

    return results


def grade_mixed_review(run_dir: Path) -> list[dict]:
    """对 mixed-review 评测用例打分。"""
    code_path = run_dir / "outputs" / "trainorder.js"
    report_path = run_dir / "outputs" / "report.md"
    code = load_text(code_path)
    report = load_text(report_path)

    results = []

    # 1. 文件存在
    passed, evidence = check_file_exists(code_path)
    results.append({"text": "outputs/trainorder.js 文件存在且可读", "passed": passed, "evidence": evidence})

    # 2. 定义常量
    has_constant = bool(re.search(r"ORDER_STATUS_(CANCELED|CANCELLED|CANCEL)\s*=\s*8", code))
    results.append({
        "text": "trainorder.js 中定义了订单取消状态常量（如 ORDER_STATUS_CANCELED）",
        "passed": has_constant,
        "evidence": "找到常量定义" if has_constant else "未找到 ORDER_STATUS_CANCELED = 8 形式的常量定义"
    })

    # 3. 统一提取 orderStatus
    has_orderstatus_var = bool(re.search(r"(var|const|let)\s+orderStatus\s*=", code))
    results.append({
        "text": "在 loadTrainDetail 函数入口处统一提取了 orderStatus 变量",
        "passed": has_orderstatus_var,
        "evidence": "找到 orderStatus 变量定义" if has_orderstatus_var else "未找到 orderStatus 变量定义"
    })

    # 4. 条件判断使用统一变量和常量
    condition_ok = bool(re.search(r"if\s*\(\s*orderStatus\s*==\s*ORDER_STATUS_|if\s*\(\s*orderStatus\s*===\s*ORDER_STATUS_", code))
    results.append({
        "text": "条件判断中使用统一变量和常量，不再直接使用 $orderBrief.status == 8",
        "passed": condition_ok,
        "evidence": "if 条件使用 orderStatus === ORDER_STATUS_ 形式" if condition_ok else "未找到 orderStatus 与 ORDER_STATUS_ 的组合使用"
    })

    # 5. 报告存在
    passed, evidence = check_file_exists(report_path)
    results.append({"text": "outputs/report.md 文件存在", "passed": passed, "evidence": evidence})

    # 6. 报告列出非代码建议（至少匹配两项）
    suggestion_keywords = ["下游服务", "APP 联调", "类型校验", "mvn resources", "部署", "缓存", "WebView", "httpOnly"]
    matched = [k for k in suggestion_keywords if k in report]
    results.append({
        "text": "report.md 中列出需要人工确认的非代码建议（如下游服务、APP 联调、类型校验、部署步骤中的至少两项）",
        "passed": len(matched) >= 2,
        "evidence": f"匹配到 {len(matched)} 个关键词: {', '.join(matched)}" if matched else "未匹配到任何非代码建议关键词"
    })

    return results


GRADERS = {
    "magic-number": grade_magic_number,
    "data-source": grade_data_source,
    "mixed-review": grade_mixed_review,
}


def grade_run(eval_dir: Path, config: str) -> None:
    """对单个运行目录打分并保存 grading.json。"""
    run_dir = eval_dir / config
    if not run_dir.exists():
        print(f"跳过不存在的目录: {run_dir}")
        return

    eval_name = eval_dir.name
    grader = GRADERS.get(eval_name)
    if not grader:
        print(f"未找到 {eval_name} 的评分函数，跳过")
        return

    expectations = grader(run_dir)
    passed = sum(1 for e in expectations if e["passed"])
    total = len(expectations)

    grading = {
        "expectations": expectations,
        "summary": {
            "passed": passed,
            "failed": total - passed,
            "total": total,
            "pass_rate": round(passed / total, 2) if total else 0.0,
        }
    }

    # 尝试读取 timing.json
    timing_path = run_dir / "timing.json"
    if timing_path.exists():
        timing = json.loads(timing_path.read_text(encoding="utf-8"))
        grading["timing"] = {
            "total_duration_seconds": timing.get("total_duration_seconds", 0),
        }

    output_path = run_dir / "grading.json"
    output_path.write_text(json.dumps(grading, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已保存评分: {output_path} ({passed}/{total})")


def main() -> None:
    """入口函数：遍历迭代目录下所有评测用例并打分。"""
    if len(sys.argv) != 2:
        print("用法: python grade.py <workspace>/iteration-N")
        sys.exit(1)

    iteration_dir = Path(sys.argv[1])
    if not iteration_dir.exists():
        print(f"目录不存在: {iteration_dir}")
        sys.exit(1)

    for eval_dir in sorted(iteration_dir.iterdir()):
        if not eval_dir.is_dir():
            continue
        for config in ("with_skill", "without_skill"):
            grade_run(eval_dir, config)


if __name__ == "__main__":
    main()
