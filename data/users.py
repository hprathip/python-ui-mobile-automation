from dataclasses import dataclass, field

@dataclass(frozen=True)
class User:
    username: str
    password: str = field(repr=False)

STANDARD = User("standard_user", "secret_sauce")
LOCKED = User("locked_out_user", "secret_sauce")
PERFORMANCE_GLITCH = User("performance_glitch_user", "secret_sauce")
PROBLEM = User("problem_user", "secret_sauce")