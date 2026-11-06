from typing import Callable


def make_flaky_service(failures: int) -> tuple[Callable[[int], str], Callable[[], int]]:
    attempt_count = 0

    def get_profile(user_id: int) -> str:
        """Returns user profile."""
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count <= failures:
            raise ConnectionError(f"zbiy servisu pry sprobi {attempt_count}")
        return f"profile_{user_id}"

    def call_count() -> int:
        return attempt_count

    return get_profile, call_count
