import platform

if platform.system() == "Windows":
    BOT_TOKEN = "8272034294:AAFJhoN2RmPP5QEThj9g1yTZ3gmrqtb-UkI"
    DB_PATH = "data/debug.db"
else:
    BOT_TOKEN = "8427610229:AAE9mUs_RYLF2Cbng1H-0TGeRirYLrK4A4k"
    DB_PATH = "data/release.db"