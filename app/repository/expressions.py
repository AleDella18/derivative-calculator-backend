from app.repository.users import get_user_id


def get_existing_derivative(expr, db):
    cur = db.execute("SELECT derivative FROM FUNCTIONS WHERE function = ?", [expr])
    row = cur.fetchone()
    return row[0] if row else None


def get_image_path(function_id, db):
    cur = db.execute(
        "SELECT path_graph FROM FUNCTIONS WHERE function_id = ?", [function_id]
    )
    row = cur.fetchone()
    return row[0] if row else None


def save_derivative(user_name, function, derivative, db, image_url):
    user_id = get_user_id(user_name, db)
    db.execute(
        "INSERT INTO FUNCTIONS (user_id, function, derivative, path_graph) "
        "VALUES (?, ?, ?, ?)",
        [user_id, function, derivative, image_url],
    )
    db.commit()


def get_function_id(expr, db):
    cur = db.execute("SELECT function_id FROM FUNCTIONS WHERE function = ?", [expr])
    row = cur.fetchone()
    return row[0] if row else None
