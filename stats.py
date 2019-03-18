PROGRESS_STATES = [
    (0, "Abysmal"),
    (1, "Comically behind"),
    (25, "Very behind"),
    (50, "Behind"),
    (60, "A Bit Behind"),
    (75, "Doing OK"),
    (90, "On Track"),
    (100, "Ahead of the game"),
]


def get_status_from_percentage(percentage):
    final_status = ""
    for base_percentage, status in PROGRESS_STATES:
        if percentage >= base_percentage:
            final_status = status
    return final_status



