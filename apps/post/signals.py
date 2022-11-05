from datetime import datetime
import json

from django.conf import settings

# Let google know when a new page is published
def update_content_tracker(sender, **kwargs):
    FILE_NAME = settings.PING_FILE

    try:
        with open(FILE_NAME, "r") as file:
            raw_data = file.read()

        data = json.loads(raw_data)
        data["new_content"] = True
        data["update_date"] = str(datetime.now())
    except Exception:
        data = {
            "new_content": True,
            "update_date": str(datetime.now()),
        }

    with open(FILE_NAME, "w") as f:
        f.write(json.dumps(data))
