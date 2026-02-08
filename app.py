from database import init_db, add_user, add_attendance

init_db()
add_user("John Doe")

print(add_attendance(1, 0.42))  # True
print(add_attendance(1, 0.38))  # False (déjà présent)
