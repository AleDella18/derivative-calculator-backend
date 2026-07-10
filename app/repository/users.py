def check_user_password(user_name, db):
    cur = db.execute("SELECT password FROM USERS WHERE user_name = ?", [user_name])
    row = cur.fetchone()
    return row[0] if row else None


def save_user(user_name, password, db):
    db.execute(
        "INSERT INTO USERS (user_name, password) VALUES (?, ?)",
        [user_name, password],
    )
    db.commit()


def get_user_id(user_name, db):
    cur = db.execute("SELECT user_id FROM USERS WHERE user_name = ?", [user_name])
    row = cur.fetchone()
    return row[0] if row else None
