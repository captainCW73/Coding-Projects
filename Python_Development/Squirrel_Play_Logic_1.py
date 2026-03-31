"""
Basic squirrel play logic from CodingBat:
- Squirrels play if temperature is between 60 and 90 inclusive.
- In summer, the upper bound relaxes to 100.
"""

def squirrel_play(temp: int, is_summer: bool) -> bool:
    """Return True if squirrels play at the given temp, respecting summer rule."""
    upper = 100 if is_summer else 90
    return 60 <= temp <= upper


if __name__ == "__main__":
    # Simple manual checks
    print(squirrel_play(70, False))  # True
    print(squirrel_play(95, False))  # False
    print(squirrel_play(95, True))   # True

