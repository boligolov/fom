"""Surface status vocabulary shared by validation and graph consumers."""

STATUS_FORMS = {"accept", "reject", "uncommit", "uncommitted"}


def status_value(head: str) -> str:
    return "uncommitted" if head == "uncommit" else head
