from datetime import datetime


def greeting(request):
    current_time = datetime.now().time()
    if current_time.hour < 12:
        greeting = "Morning"
    elif current_time.hour < 16:
        greeting = "Afternoon"
    elif current_time.hour < 19:
        greeting = "Evening"
    else:
        greeting = "Night"

    return {"greeting": greeting}
