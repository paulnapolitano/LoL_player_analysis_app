from django.utils import timezone
import datetime

# ------------------------------- FUNCTIONS ---------------------------------


# Convert Unix time since epoch (in milliseconds) to a timezone-aware datetime
# DEPENDENCIES: timezone, datetime
def millis_to_timezone(millis):
    return timezone.make_aware(datetime.datetime.fromtimestamp(millis/1000))