def check_marks(mark):
    """Return the grade classification based on the mark."""
    if mark >= 70:
        return "First Class"
    elif mark >= 60:
        return "(2:1) Upper Second Class"
    elif mark >= 50:
        return "(2:2) Lower Second Class"
    elif mark >= 40:
        return "Third Class"
    elif mark < 40:
        return "Fail"
    else:
        return "Invalid"

