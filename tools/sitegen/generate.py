#!/usr/bin/env python3
"""ProgramBench 站点生成器（初级版）。

扫描 src/programbench/data/tasks/ 下的 task.yaml，生成一个平铺的概览页 index.html。
当前只做「列出全部 task」这一件事，不涉及领域分类、详情页、统计与增删处理。
"""

import argparse
import html
import os


DEFAULT_TASKS_DIR = "src/programbench/data/tasks"
DEFAULT_OUT = "dist/index.html"

# 当前关心的字段（task.yaml 里另有 eval_clean_hashes 等，先不处理）
KEEP_FIELDS = ("repository", "commit", "language", "difficulty")


def parse_task_yaml(path):
    """极简 task.yaml 解析：只提取 KEEP_FIELDS 里的键值。"""
    fields = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n").strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip("'\"")
            if key in KEEP_FIELDS:
                fields[key] = value
    return fields


def collect_tasks(tasks_dir):
    """遍历 tasks 目录，收集每个 task 的元信息。"""
    tasks = []
    if not os.path.isdir(tasks_dir):
        return tasks
    for name in sorted(os.listdir(tasks_dir)):
        task_dir = os.path.join(tasks_dir, name)
        yaml_path = os.path.join(task_dir, "task.yaml")
        if not os.path.isdir(task_dir) or not os.path.isfile(yaml_path):
            continue
        fields = parse_task_yaml(yaml_path)
        tasks.append({
            "id": name,
            "repository": fields.get("repository", ""),
            "commit": fields.get("commit", ""),
            "language": fields.get("language", ""),
            "difficulty": fields.get("difficulty", ""),
        })
    return tasks


def render(tasks):
    rows = []
    for t in tasks:
        rows.append(
            "<tr>"
            f"<td>{html.escape(t['id'])}</td>"
            f"<td>{html.escape(t['repository'])}</td>"
            f"<td>{html.escape(t['language'])}</td>"
            f"<td>{html.escape(t['difficulty'])}</td>"
            "</tr>"
        )
    body = "\n".join(rows)
    return (
        "<!DOCTYPE html>\n"
        '<html lang="zh-CN">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        "<title>ProgramBench 任务总览</title>\n"
        "<style>\n"
        "body { font-family: -apple-system, sans-serif; margin: 24px; color: #222; }\n"
        "table { border-collapse: collapse; width: 100%; }\n"
        "th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: left; }\n"
        "th { background: #f5f5f5; }\n"
        "</style>\n"
        "</head>\n"
        "<body>\n"
        f"<h1>ProgramBench 任务总览（{len(tasks)} 个）</h1>\n"
        "<table>\n"
        "<thead><tr><th>Task ID</th><th>仓库</th><th>语言</th><th>难度</th></tr></thead>\n"
        "<tbody>\n"
        f"{body}\n"
        "</tbody>\n"
        "</table>\n"
        "</body>\n"
        "</html>\n"
    )


def main():
    parser = argparse.ArgumentParser(description="ProgramBench 站点生成器（初级版）")
    parser.add_argument("--tasks-dir", default=DEFAULT_TASKS_DIR)
    parser.add_argument("--out", default=DEFAULT_OUT)
    args = parser.parse_args()

    tasks = collect_tasks(args.tasks_dir)
    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(render(tasks))
    print(f"生成 {args.out}，共 {len(tasks)} 个 task")


if __name__ == "__main__":
    main()
