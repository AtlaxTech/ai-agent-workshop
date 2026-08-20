from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.learning_ops import (
    CONFIG_PATH,
    INPUT_STATE_PATH,
    REVIEW_INDEX_PATH,
    checkpoint_inputs,
    due_items,
    lint_system,
    prioritize_due_items,
    record_review,
    register_card,
    scan_inputs,
    write_due_queue,
    LearningOpsError,
)


class LearningOpsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.write_json(
            CONFIG_PATH,
            {
                "schema_version": 1,
                "scan_roots": ["01-输入区", "02-每日笔记", "06-复习区"],
                "scan_extensions": [".md", ".json"],
                "exclude_globs": ["06-复习区/复习索引.json"],
                "intervals_days": [1, 3, 7, 14, 30],
                "daily_review_limit_minutes": 25,
                "estimated_minutes_per_card": 2,
                "archive_min_reviews": 5,
                "archive_min_success_streak": 3,
            },
        )
        self.write_json(
            INPUT_STATE_PATH,
            {"schema_version": 1, "last_checkpoint_at": None, "processed_files": {}},
        )
        self.write_json(REVIEW_INDEX_PATH, {"schema_version": 1, "items": []})

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write_json(self, relative: Path, value: object) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    def write_text(self, relative: str, value: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")
        return path

    def test_scan_and_checkpoint_detect_only_new_changes(self) -> None:
        note = self.write_text("01-输入区/Day-1/raw.md", "first")
        self.assertEqual(scan_inputs(self.root)[0]["status"], "new")

        checkpoint_inputs(self.root)
        self.assertEqual(scan_inputs(self.root), [])

        note.write_text("second", encoding="utf-8")
        self.assertEqual(
            scan_inputs(self.root),
            [{"status": "modified", "path": "01-输入区/Day-1/raw.md"}],
        )

    def test_good_reviews_follow_intervals_and_archive_after_five_rounds(self) -> None:
        self.write_text("06-复习区/知识卡片/K0001-test.md", "# card")
        item = register_card(
            self.root,
            "K0001",
            "06-复习区/知识卡片/K0001-test.md",
            "2026-01-01",
        )
        self.assertEqual(item["next_review"], "2026-01-02")
        self.assertEqual([entry["id"] for entry in due_items(self.root, "2026-01-02")], ["K0001"])

        schedule = [
            ("2026-01-02", "2026-01-05"),
            ("2026-01-05", "2026-01-12"),
            ("2026-01-12", "2026-01-26"),
            ("2026-01-26", "2026-02-25"),
        ]
        for reviewed_on, expected_next in schedule:
            item = record_review(self.root, "K0001", "good", reviewed_on, 4)
            self.assertEqual(item["next_review"], expected_next)
            self.assertEqual(item["status"], "scheduled")

        item = record_review(self.root, "K0001", "good", "2026-02-25", 5)
        self.assertEqual(item["status"], "archived")
        self.assertIsNone(item["next_review"])
        self.assertTrue((self.root / item["card_path"]).is_file())
        self.assertIn("06-复习区/已掌握/", item["card_path"])

    def test_again_resets_stage_and_schedules_next_day(self) -> None:
        self.write_text("06-复习区/知识卡片/K0001-test.md", "# card")
        register_card(
            self.root,
            "K0001",
            "06-复习区/知识卡片/K0001-test.md",
            "2026-01-01",
        )
        record_review(self.root, "K0001", "good", "2026-01-02")
        item = record_review(self.root, "K0001", "again", "2026-01-05")
        self.assertEqual(item["stage"], 0)
        self.assertEqual(item["next_review"], "2026-01-06")
        self.assertEqual(item["lapses"], 1)

    def test_due_queue_contains_card_link_without_changing_schedule(self) -> None:
        self.write_text("06-复习区/知识卡片/K0001-test.md", "# card")
        register_card(
            self.root,
            "K0001",
            "06-复习区/知识卡片/K0001-test.md",
            "2026-01-01",
        )
        items = due_items(self.root, "2026-01-02")
        queue = write_due_queue(self.root, "2026-01-02", items)
        content = queue.read_text(encoding="utf-8")
        self.assertIn("K0001", content)
        self.assertIn("../知识卡片/K0001-test.md", content)
        self.assertEqual(due_items(self.root, "2026-01-02")[0]["review_count"], 0)

    def test_due_queue_prioritizes_and_defers_without_rescheduling(self) -> None:
        for number, priority in [(1, 1), (2, 3), (3, 3)]:
            card = f"06-复习区/知识卡片/K{number:04d}-test.md"
            self.write_text(card, "# card")
            register_card(
                self.root, f"K{number:04d}", card, "2026-01-01", priority
            )
        index = json.loads((self.root / REVIEW_INDEX_PATH).read_text(encoding="utf-8"))
        index["items"][2]["lapses"] = 2
        self.write_json(REVIEW_INDEX_PATH, index)

        due = due_items(self.root, "2026-01-03")
        selected, deferred = prioritize_due_items(due, "2026-01-03", 4, 2)
        self.assertEqual([item["id"] for item in selected], ["K0003", "K0002"])
        self.assertEqual([item["id"] for item in deferred], ["K0001"])
        queue = write_due_queue(self.root, "2026-01-03", selected, deferred, 4)
        self.assertIn("仍保持到期/逾期状态", queue.read_text(encoding="utf-8"))
        self.assertEqual(
            [item["next_review"] for item in due_items(self.root, "2026-01-03")],
            ["2026-01-02", "2026-01-02", "2026-01-02"],
        )

    def test_lint_passes_for_valid_empty_system(self) -> None:
        self.assertEqual(lint_system(self.root), [])

    def test_review_history_rejects_backward_dates(self) -> None:
        self.write_text("06-复习区/知识卡片/K0001-test.md", "# card")
        register_card(
            self.root,
            "K0001",
            "06-复习区/知识卡片/K0001-test.md",
            "2026-01-01",
        )
        record_review(self.root, "K0001", "good", "2026-01-05")
        with self.assertRaises(LearningOpsError):
            record_review(self.root, "K0001", "good", "2026-01-04")


if __name__ == "__main__":
    unittest.main()
