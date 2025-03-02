async def check_username_exists(bot, username):
    try:
        await bot.get_chat(username)
    except:
        return False
    else:
        return True


def extract_usernames(file_path):
    try:
        usernames = []
        with open(file_path, "r") as f:
            for r in f.readlines():
                if r:
                    usernames.append(r)
    except:
        return []
    else:
        return usernames
