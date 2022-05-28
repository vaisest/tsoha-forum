from datetime import datetime


def relative_date_format(date):
    diff = datetime.utcnow() - date
    if diff.days == 1:
        return "1 day ago"
    elif diff.days > 1:
        return f"{diff.days} days ago"
    elif diff.seconds <= 5:
        return "just now"
    elif diff.seconds <= 60:
        return f"{diff.seconds} seconds ago"
    elif diff.seconds <= 3600:
        return f"{diff.seconds // 60} minutes ago"
    else:
        return f"{diff.seconds // 3600} hours ago "
