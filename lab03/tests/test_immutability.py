import dataclasses
import pytest

from model import Comment, Task, make_metadata
from core import freeze, add_comment, add_label, create_task, update_metadata, change_priority, change_status


def test_add_comment_not_changes_old_task():
    first = create_task(1, "a")
    second = add_comment(first, Comment("Ira", "ok"))
    assert first.comments == ()
    assert second.comments == (Comment("Ira", "ok"),)
    assert first is not second


def test_add_label_not_changes_old_task():
    first = create_task(1, "a")
    second = add_label(first, "bug")
    assert first.labels == frozenset()
    assert second.labels == frozenset({"bug"})


def test_change_status_and_priority():
    first = create_task(1, "a")
    second = change_priority(change_status(first, "done"), 5)
    assert (first.status, first.priority) == ("todo", 3)
    assert (second.status, second.priority) == ("done", 5)


def test_invalid_priority():
    with pytest.raises(ValueError):
        change_priority(create_task(1, "a"), 9)


def test_direct_change_field_forbidden():
    task = create_task(1, "a")
    with pytest.raises(dataclasses.FrozenInstanceError):
        task.status = "done"


def test_metadata_only_for_read():
    task = create_task(1, "a", author="Ira")
    with pytest.raises(TypeError):
        task.metadata["author"] = "Oleh"


def test_metadata_are_copied_from_source():
    source = {"klyuch": "1"}
    metadata = make_metadata(**source)
    source["klyuch"] = "2"
    assert metadata["klyuch"] == "1"


def test_change_metadata_gives_new_task():
    first = create_task(1, "a", author="Ira")
    second = update_metadata(first, author="Oleh", sprint="3")
    assert first.metadata["author"] == "Ira"
    assert dict(second.metadata) == {"author": "Oleh", "sprint": "3"}


def test_task_and_comment_hashable():
    task = add_comment(create_task(1, "a", x="y"), Comment("Ira", "ok"))
    assert isinstance(hash(task), int)
    assert len({task, task}) == 1
    assert hash(Comment("Ira", "ok")) == hash(Comment("Ira", "ok"))


def test_tasks_from_identical_fields_equal():
    assert create_task(1, "a") == create_task(1, "a")


def test_types_collections():
    task = create_task(1, "a")
    assert isinstance(task, Task)
    assert isinstance(task.comments, tuple)
    assert isinstance(task.labels, frozenset)


def test_methods_return_new_tasks():
    task = create_task(1, "a")
    updated = task.with_comment(Comment("Ira", "ok")).add_label("bug").with_status("done").with_priority(1)
    assert (task.comments, task.labels, task.status, task.priority) == ((), frozenset(), "todo", 3)
    assert updated.comments_count() == 1 and "bug" in updated.labels
    assert (updated.status, updated.priority) == ("done", 1)


def test_freeze_makes_nested_data_immutable():
    frozen = freeze({"a": [1, {2, 3}], "b": {"c": [4]}})
    assert frozen["a"] == (1, frozenset({2, 3}))
    assert frozen["b"]["c"] == (4,)
    with pytest.raises(TypeError):
        frozen["b"]["x"] = 1
