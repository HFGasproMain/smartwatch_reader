from django import template

register = template.Library()

@register.filter
def format_time(time_string):
    # Format the time component
    formatted_time = time_string[:5]  # Extract the first 5 characters representing the time component
    return formatted_time
