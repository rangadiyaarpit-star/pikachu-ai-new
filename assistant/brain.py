def detect_intent(c):

    c = c.lower()

    # MEMORY SAVE
    if "remember" in c:

        return "memory_save"

    # MEMORY RECALL
    elif (
        "my name" in c or
        "who am i" in c or
        "do you remember" in c or
        "what is" in c
    ):
        
        return "memory_recall"

    # MOBILE CONTROL
    elif any(word in c for word in [

        "wifi",
        "bluetooth",
        "camera",
        "flashlight",
        "volume",
        "open",
        "home",
        "back",
        "recent",
        "swipe",
        "tap"

    ]):

        return "mobile_control"

    # AI CHAT
    else:

        return "ai_chat"