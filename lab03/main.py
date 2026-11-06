from model import Comment
from core import add_comment, add_label, create_task, change_priority, change_status


def show(title: str, task) -> None:
    print(f"{title}: status={task.status}, priorytet={task.priority}, "
          f"komentari={task.comments_count()}, mitky={sorted(task.labels)}")


if __name__ == "__main__":
    first = create_task(1, "Zrobyty lab 3", project="FP")
    show("Persha", first)
    second = add_comment(first, Comment("Ira", "Pochynayu"))
    third = add_label(second, "terminovo")
    fourth = change_priority(change_status(third, "in_progress"), 1)
    show("Persha (ne zminylas)", first)
    show("Chetverta (nova kopiya)", fourth)
    print("Hash chetvertoyi:", hash(fourth) != 0)
