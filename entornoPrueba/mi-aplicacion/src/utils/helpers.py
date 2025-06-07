def validate_email(email):
    import re
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def validate_password(password):
    return len(password) >= 6

def format_user_data(user_data):
    return {key: value.strip() for key, value in user_data.items()}