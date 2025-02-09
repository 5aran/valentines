from time import sleep


def type_writer(phrases: list[str | int | float], letters_per_sec: int = 18):
    """Yield each letter of a phrase at a given rate to simulate typing."""
    for phrase_pause in phrases:
        if isinstance(phrase_pause, str):
            for letter in phrase_pause:
                sleep(1 / letters_per_sec)
                yield letter
        elif isinstance(phrase_pause, (int, float)):
            sleep(phrase_pause)
