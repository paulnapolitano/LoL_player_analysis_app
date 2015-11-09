from django.utils import timezone
from datetime import datetime, timedelta
import pytz

# ------------------------------- FUNCTIONS ---------------------------------


# Convert Unix time since epoch (in milliseconds) to a timezone-aware datetime
# DEPENDENCIES: timezone, datetime
def millis_to_timezone(millis):
    try: 
        aware_time = timezone.make_aware(datetime.fromtimestamp(millis/1000))
    except (pytz.AmbiguousTimeError, pytz.NonExistentTimeError):
        aware_time = timezone.make_aware(datetime.fromtimestamp(millis/1000) + timedelta(hours=1))
    return aware_time