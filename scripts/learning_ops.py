#!/usr/bin/env python3
"""Deterministic input tracking and spaced-review scheduling.

The Agent performs semantic work. This tool only owns file fingerprints,
review dates, queue generation, validation, and recoverable card archiving.
It uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import shutil
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = Path("00-路线与状态/学习系统配置.json")
INPUT_STATE_PATH = Path("00-路线与状态/输入处理状态.json")
REVIEW_INDEX_PATH = Path("06-复习区/复习索引.json")
TODAY_REVIEW_DIR = Path("06-复习区/今日复习")
MASTERED_DIR = Path("06-复习区/已掌握")
VALID_RATINGS = {"again", "hard", "good", "easy"}


class LearningOpsError(RuntimeError):
    """Raised for invalid state or unsafe operations."""


def read_json(path: Path, default: dict[str, Any] | None = None) -> dict[str, Any]:
    if not path.exists():
        if default is not None:
            return default
        raise LearningOpsError(f"Missing required file: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LearningOpsError(f"Cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise LearningOpsError(f"Expected a JSON object in {path}")
    return data


def write_json_atomic(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise LearningOpsError(f"Invalid date '{value}', expected YYYY-MM-DD") from exc


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def relative_path(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise LearningOpsError(f"Path must stay inside repository: {path}") from exc


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def is_excluded(relative: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(relative, pattern) for pattern in patterns)


def collect_learning_files(root: Path) -> dict[str, str]:
    config = read_json(root / CONFIG_PATH)
    extensions = set(config.get("scan_extensions", []))
    excludes = list(config.get("exclude_globs", []))
    files: dict[str, str] = {}

    for root_name in config.get("scan_roots", []):
        scan_root = root / root_name
        if not scan_root.exists():
            continue
        for path in sorted(scan_root.rglob("*")):
            if not path.is_file() or path.suffix not in extensions:
                continue
            relative = relative_path(root, path)
            if is_excluded(relative, excludes):
                continue
            files[relative] = sha256_file(path)
    return files


def scan_inputs(root: Path) -> list[dict[str, str]]:
    state = read_json(
        root / INPUT_STATE_PATH,
        {"schema_version": 1, "last_checkpoint_at": None, "processed_files": {}},
    )
    processed = state.get("processed_files", {})
    if not isinstance(processed, dict):
        raise LearningOpsError("processed_files must be a JSON object")
    current = collect_learning_files(root)
    changes: list[dict[str, str]] = []

    for path, fingerprint in current.items():
        previous = processed.get(path)
        if previous is None:
            changes.append({"status": "new", "path": path})
        elif previous != fingerprint:
            changes.append({"status": "modified", "path": path})

    for path in sorted(set(processed) - set(current)):
        changes.append({"status": "deleted", "path": path})
    return sorted(changes, key=lambda item: (item["path"], item["status"]))


def checkpoint_inputs(root: Path) -> dict[str, Any]:
    files = collect_learning_files(root)
    state = {
        "schema_version": 1,
        "last_checkpoint_at": now_iso(),
        "processed_files": files,
    }
    write_json_atomic(root / INPUT_STATE_PATH, state)
    return {"checkpointed_files": len(files), "last_checkpoint_at": state["last_checkpoint_at"]}


def load_review_index(root: Path) -> dict[str, Any]:
    index = read_json(root / REVIEW_INDEX_PATH, {"schema_version": 1, "items": []})
    if not isinstance(index.get("items"), list):
        raise LearningOpsError("review index items must be a list")
    return index


def save_review_index(root: Path, index: dict[str, Any]) -> None:
    write_json_atomic(root / REVIEW_INDEX_PATH, index)


def next_card_id(root: Path) -> str:
    maximum = 0
    for item in load_review_index(root)["items"]:
        identifier = str(item.get("id", ""))
        if identifier.startswith("K") and identifier[1:].isdigit():
            maximum = max(maximum, int(identifier[1:]))
    return f"K{maximum + 1:04d}"


def register_card(
    root: Path,
    identifier: str,
    card: str,
    created: str,
    priority: int = 2,
) -> dict[str, Any]:
    if not identifier.startswith("K") or not identifier[1:].isdigit():
        raise LearningOpsError("Card id must use K0001 format")
    created_date = parse_date(created)
    if priority not in {1, 2, 3}:
        raise LearningOpsError("Card priority must be 1, 2, or 3")
    card_path = root / card
    card_relative = relative_path(root, card_path)
    if not card_path.is_file():
        raise LearningOpsError(f"Card file does not exist: {card_relative}")

    index = load_review_index(root)
    if any(item.get("id") == identifier for item in index["items"]):
        raise LearningOpsError(f"Duplicate card id: {identifier}")
    if any(item.get("card_path") == card_relative for item in index["items"]):
        raise LearningOpsError(f"Card is already registered: {card_relative}")

    config = read_json(root / CONFIG_PATH)
    intervals = config.get("intervals_days", [1, 3, 7, 14, 30])
    first_interval = int(intervals[0])
    item = {
        "id": identifier,
        "card_path": card_relative,
        "created": created_date.isoformat(),
        "priority": priority,
        "status": "scheduled",
        "stage": 0,
        "interval_days": first_interval,
        "next_review": (created_date + timedelta(days=first_interval)).isoformat(),
        "review_count": 0,
        "lapses": 0,
        "success_streak": 0,
        "last_review": None,
        "history": [],
    }
    index["items"].append(item)
    index["items"].sort(key=lambda entry: entry["id"])
    save_review_index(root, index)
    return item


def due_items(root: Path, on_date: str) -> list[dict[str, Any]]:
    target = parse_date(on_date)
    items = []
    for item in load_review_index(root)["items"]:
        if item.get("status") != "scheduled":
            continue
        next_review = parse_date(str(item.get("next_review")))
        if next_review <= target:
            items.append(item)
    return sorted(items, key=lambda item: (item["next_review"], item["id"]))


def prioritize_due_items(
    items: list[dict[str, Any]],
    on_date: str,
    limit_minutes: int,
    minutes_per_card: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if limit_minutes <= 0:
        raise LearningOpsError("daily_review_limit_minutes must be positive")
    if minutes_per_card <= 0:
        raise LearningOpsError("estimated_minutes_per_card must be positive")
    target = parse_date(on_date)
    ordered = sorted(
        items,
        key=lambda item: (
            -int(item.get("priority", 2)),
            -int(item.get("lapses", 0)),
            -(target - parse_date(str(item["next_review"]))).days,
            int(item.get("stage", 0)),
            str(item.get("id", "")),
        ),
    )
    capacity = max(1, limit_minutes // minutes_per_card)
    return ordered[:capacity], ordered[capacity:]


def write_due_queue(
    root: Path,
    on_date: str,
    items: list[dict[str, Any]],
    deferred: list[dict[str, Any]] | None = None,
    limit_minutes: int | None = None,
) -> Path:
    deferred = deferred or []
    queue_path = root / TODAY_REVIEW_DIR / f"{on_date}.md"
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# {on_date} 今日复习",
        "",
        "> 本页由明确指令生成。先主动回答，再查看卡片答案；完成后执行重新排期。",
        "",
        f"今日安排：{len(items)} 张；预算：{limit_minutes or '未限制'} 分钟；暂缓：{len(deferred)} 张",
        "",
        "| ID | 卡片 | 优先级 | 阶段 | 原定日期 | 已复习 |",
        "|---|---|---:|---:|---|---:|",
    ]
    for item in items:
        card_path = root / item["card_path"]
        link = os.path.relpath(card_path, queue_path.parent).replace(os.sep, "/")
        lines.append(
            f"| {item['id']} | [{card_path.stem}]({link}) | {item.get('priority', 2)} | {item['stage']} | "
            f"{item['next_review']} | {item['review_count']} |"
        )
    if deferred:
        lines.extend(
            [
                "",
                "## 超出今日预算",
                "",
                "> 以下卡片仍保持到期/逾期状态，没有被重新排期，也不视为完成。下次生成队列时会重新参与排序。",
                "",
                "| ID | 卡片 | 优先级 | 原定日期 |",
                "|---|---|---:|---|",
            ]
        )
        for item in deferred:
            card_path = root / item["card_path"]
            link = os.path.relpath(card_path, queue_path.parent).replace(os.sep, "/")
            lines.append(
                f"| {item['id']} | [{card_path.stem}]({link}) | "
                f"{item.get('priority', 2)} | {item['next_review']} |"
            )
    lines.extend(
        [
            "",
            "## 操作",
            "",
            "1. 对 Agent 说 `开始今日复习`。",
            "2. 一次回答一题，不先看参考答案。",
            "3. 完成后说 `完成今日复习并重新排期`。",
            "",
        ]
    )
    queue_path.write_text("\n".join(lines), encoding="utf-8")
    return queue_path


def archive_card(root: Path, item: dict[str, Any]) -> str:
    source = root / item["card_path"]
    if not source.is_file():
        raise LearningOpsError(f"Cannot archive missing card: {item['card_path']}")
    destination_dir = root / MASTERED_DIR
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / source.name
    if destination.exists() and destination.resolve() != source.resolve():
        raise LearningOpsError(f"Archive destination already exists: {destination}")
    if source.resolve() != destination.resolve():
        shutil.move(str(source), str(destination))
    return relative_path(root, destination)


def record_review(
    root: Path,
    identifier: str,
    rating: str,
    reviewed_on: str,
    confidence: int | None = None,
    note: str | None = None,
) -> dict[str, Any]:
    if rating not in VALID_RATINGS:
        raise LearningOpsError(f"Rating must be one of: {', '.join(sorted(VALID_RATINGS))}")
    if confidence is not None and not 1 <= confidence <= 5:
        raise LearningOpsError("Confidence must be between 1 and 5")
    review_date = parse_date(reviewed_on)
    index = load_review_index(root)
    item = next((entry for entry in index["items"] if entry.get("id") == identifier), None)
    if item is None:
        raise LearningOpsError(f"Unknown card id: {identifier}")
    if item.get("status") == "archived":
        raise LearningOpsError(f"Card is already archived: {identifier}")
    if review_date < parse_date(str(item.get("created"))):
        raise LearningOpsError("Review date cannot be earlier than card creation date")
    if item.get("last_review") and review_date < parse_date(str(item["last_review"])):
        raise LearningOpsError("Review date cannot be earlier than the previous review")

    config = read_json(root / CONFIG_PATH)
    intervals = [int(value) for value in config.get("intervals_days", [1, 3, 7, 14, 30])]
    maximum_stage = len(intervals) - 1
    stage = int(item.get("stage", 0))

    if rating == "again":
        stage = 0
        item["lapses"] = int(item.get("lapses", 0)) + 1
        item["success_streak"] = 0
    elif rating == "hard":
        stage = max(0, stage - 1)
        item["success_streak"] = 0
    elif rating == "good":
        stage = min(maximum_stage, stage + 1)
        item["success_streak"] = int(item.get("success_streak", 0)) + 1
    else:
        stage = min(maximum_stage, stage + 2)
        item["success_streak"] = int(item.get("success_streak", 0)) + 1

    item["stage"] = stage
    item["interval_days"] = intervals[stage]
    item["review_count"] = int(item.get("review_count", 0)) + 1
    item["last_review"] = review_date.isoformat()
    history_entry: dict[str, Any] = {
        "date": review_date.isoformat(),
        "rating": rating,
        "stage_after": stage,
    }
    if confidence is not None:
        history_entry["confidence"] = confidence
    if note:
        history_entry["note"] = note
    item.setdefault("history", []).append(history_entry)

    should_archive = (
        stage == maximum_stage
        and item["review_count"] >= int(config.get("archive_min_reviews", 5))
        and item["success_streak"] >= int(config.get("archive_min_success_streak", 3))
        and rating in {"good", "easy"}
    )
    if should_archive:
        item["status"] = "archived"
        item["next_review"] = None
        item["card_path"] = archive_card(root, item)
        item["archived_at"] = review_date.isoformat()
    else:
        item["status"] = "scheduled"
        item["next_review"] = (
            review_date + timedelta(days=item["interval_days"])
        ).isoformat()

    save_review_index(root, index)
    return item


def lint_system(root: Path) -> list[str]:
    problems: list[str] = []
    config = read_json(root / CONFIG_PATH)
    intervals = config.get("intervals_days", [])
    if not intervals or any(not isinstance(value, int) or value <= 0 for value in intervals):
        problems.append("intervals_days must contain positive integers")
    if intervals != sorted(intervals):
        problems.append("intervals_days must be sorted ascending")
    if not isinstance(config.get("daily_review_limit_minutes", 25), int) or int(
        config.get("daily_review_limit_minutes", 25)
    ) <= 0:
        problems.append("daily_review_limit_minutes must be a positive integer")
    if not isinstance(config.get("estimated_minutes_per_card", 2), int) or int(
        config.get("estimated_minutes_per_card", 2)
    ) <= 0:
        problems.append("estimated_minutes_per_card must be a positive integer")

    index = load_review_index(root)
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    for item in index["items"]:
        identifier = str(item.get("id", ""))
        card_path = str(item.get("card_path", ""))
        if identifier in seen_ids:
            problems.append(f"duplicate review id: {identifier}")
        seen_ids.add(identifier)
        if card_path in seen_paths:
            problems.append(f"duplicate card path: {card_path}")
        seen_paths.add(card_path)
        if not (root / card_path).is_file():
            problems.append(f"missing card file: {identifier} -> {card_path}")
        status = item.get("status")
        if status not in {"scheduled", "archived"}:
            problems.append(f"invalid status for {identifier}: {status}")
        if status == "scheduled":
            try:
                parse_date(str(item.get("next_review")))
            except LearningOpsError as exc:
                problems.append(f"{identifier}: {exc}")
        stage = item.get("stage")
        if not isinstance(stage, int) or not 0 <= stage < len(intervals):
            problems.append(f"invalid stage for {identifier}: {stage}")
        priority = item.get("priority", 2)
        if priority not in {1, 2, 3}:
            problems.append(f"invalid priority for {identifier}: {priority}")
    return problems


def print_changes(changes: list[dict[str, str]]) -> None:
    if not changes:
        print("No unprocessed learning-file changes.")
        return
    for change in changes:
        print(f"{change['status']:8} {change['path']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="List changes since last checkpoint")
    scan_parser.add_argument("--json", action="store_true", dest="as_json")
    subparsers.add_parser("checkpoint", help="Mark current learning files as processed")
    subparsers.add_parser("next-id", help="Print the next review-card id")

    register_parser = subparsers.add_parser("register", help="Register a new review card")
    register_parser.add_argument("--id", required=True)
    register_parser.add_argument("--card", required=True)
    register_parser.add_argument("--created", required=True)
    register_parser.add_argument("--priority", type=int, default=2, choices=[1, 2, 3])

    due_parser = subparsers.add_parser("due", help="List review cards due on a date")
    due_parser.add_argument("--date", required=True)
    due_parser.add_argument("--write", action="store_true")

    record_parser = subparsers.add_parser("record", help="Record a review and reschedule")
    record_parser.add_argument("--id", required=True)
    record_parser.add_argument("--rating", required=True, choices=sorted(VALID_RATINGS))
    record_parser.add_argument("--date", required=True)
    record_parser.add_argument("--confidence", type=int)
    record_parser.add_argument("--note")

    subparsers.add_parser("lint", help="Validate scheduler and review state")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == "scan":
            changes = scan_inputs(root)
            if args.as_json:
                print(json.dumps(changes, ensure_ascii=False, indent=2))
            else:
                print_changes(changes)
        elif args.command == "checkpoint":
            print(json.dumps(checkpoint_inputs(root), ensure_ascii=False, indent=2))
        elif args.command == "next-id":
            print(next_card_id(root))
        elif args.command == "register":
            item = register_card(root, args.id, args.card, args.created, args.priority)
            print(json.dumps(item, ensure_ascii=False, indent=2))
        elif args.command == "due":
            items = due_items(root, args.date)
            if args.write:
                if items:
                    config = read_json(root / CONFIG_PATH)
                    limit_minutes = int(config.get("daily_review_limit_minutes", 25))
                    minutes_per_card = int(config.get("estimated_minutes_per_card", 2))
                    selected, deferred = prioritize_due_items(
                        items, args.date, limit_minutes, minutes_per_card
                    )
                    queue = write_due_queue(
                        root, args.date, selected, deferred, limit_minutes
                    )
                    print(relative_path(root, queue))
                else:
                    print(f"No review cards due on {args.date}; no queue file created.")
            else:
                print(json.dumps(items, ensure_ascii=False, indent=2))
        elif args.command == "record":
            item = record_review(
                root,
                args.id,
                args.rating,
                args.date,
                args.confidence,
                args.note,
            )
            print(json.dumps(item, ensure_ascii=False, indent=2))
        elif args.command == "lint":
            problems = lint_system(root)
            if problems:
                for problem in problems:
                    print(f"ERROR {problem}")
                return 1
            print("Learning system lint passed.")
        return 0
    except LearningOpsError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
