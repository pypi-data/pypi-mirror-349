from django.http import JsonResponse

def format_queryset_for_response(queryset):
    """
    Dynamically format a queryset to a format acceptable for a response payload.

    Args:
        queryset (QuerySet): The queryset to be formatted.

    Returns:
        list: A list of dictionaries or a single dictionary.
    """
    if isinstance(queryset, QuerySet):
        # If it's a queryset, we'll serialize it to a list of dictionaries.
        # This can be expanded to handle specific fields, annotations, or related objects.
        return list(queryset.values())

    elif isinstance(queryset, list):
        # If it's already a list, no need to change it, but ensure it's serializable.
        return [item if isinstance(item, dict) else item.__dict__ for item in queryset]

    elif isinstance(queryset, dict):
        # If it's already a dict, return it as-is.
        return queryset

    else:
        # Handle any other custom cases (like individual model instances, etc.)
        try:
            # If the object is a single model instance, convert it to a dict.
            return queryset.__dict__
        except AttributeError:
            # If it's an unrecognized type, simply return it as-is.
            return queryset

def create_response(status, message, payload=None):
    """
    Create a response in a unified structure with status, message, and payload.

    Arguments:
    - status: HTTP status code (int)
    - message: Message to send in the response ()
    - payload: Data to send (could be a list, dictionary, or string, default is empty list)

    Returns:
    - JsonResponse: A properly formatted JSON response.
    """

    # Default to an empty array if no payload is provided
    if payload is None:
        payload = []

    # If the payload is a dictionary, we can use it directly; otherwise, we convert it to the appropriate type
    if isinstance(payload, dict) or isinstance(payload, list) or isinstance(payload, str):
        return JsonResponse({
            'Status': status,
            'Message': message,
            'Payload': payload
        })

    # If for some reason a different type is passed (you can add custom logic here if needed)
    return JsonResponse({
        'Status': status,
        'Message': "Invalid Payload Type",
        'Payload': []
    })