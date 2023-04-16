from create_bot import con


def check_newness_user(telegram_id: str) -> bool:
    cur = con.cursor()
    result = cur.execute(
            f"""SELECT token FROM bot_user
            WHERE telegram_id = {telegram_id}"""
            ).fetchall()
    if len(result) > 0: return True

    return False


def save_new_user(telegram_id: str, TOKEN: str) -> None:
    cur = con.cursor()
    cur.execute(
            f"""INSERT INTO bot_user(telegram_id, token) 
            VALUES ('{telegram_id}', '{TOKEN}')"""
            )
    con.commit()
