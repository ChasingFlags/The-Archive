from models import (session, Base)
from models import FlagTable as TableM, User as UserM,Notes as NotesM
from extensions import bcrypt

Base.metadata.create_all()

new_flag = TableM(flag="U0hDVEZ7MW50cjBzcDNjdGlvbiF9")
session.add(new_flag)
session.commit()

new_user1 = UserM(first_name="Admin", last_name="sudo", email="admin@gmail.com",is_admin=True, password=str(bcrypt.generate_password_hash("Y0u_C4nt_Cr4ck_7his_W4llah!"), 'utf-8'))
session.add(new_user1)
session.commit()

adminuser = session.query(UserM).filter_by(email="admi@gmail.com").first()
new_note1 = NotesM(title="Encoded Flag", body="U0hDVEZ7YnIwazNuIEF1dGhvcml6YXRpb259", user_id=1)
session.add(new_note1)
session.commit()

new_user2 = UserM(first_name="Brian", last_name="Kobi", email="kobi@gmail.com",is_admin=False, password=str(bcrypt.generate_password_hash("pass123"), 'utf-8'))
session.add(new_user2)
session.commit()

userbrian = session.query(UserM).filter_by(email="kobi@gmail.com").first()
new_note2 = NotesM(title="Reminder", body="Play some video games before bed", user_id=2)
session.add(new_note2)
session.commit()

userbrian = session.query(UserM).filter_by(email="kobi@gmail.com").first()
new_note3 = NotesM(title="Reminder 2", body="Learn how to sleep early", user_id=2)
session.add(new_note3)
session.commit()


new_user3 = UserM(first_name="Thomas", last_name="Snitch", email="thomas@gmail.com",is_admin=False, password=str(bcrypt.generate_password_hash("pPass123!!"), 'utf-8'))
session.add(new_user3)
session.commit()


new_user4 = UserM(first_name="Mike", last_name="Magic", email="mike@gmail.com",is_admin=False, password=str(bcrypt.generate_password_hash("pPass12fds3!!!."), 'utf-8'))
session.add(new_user4)
session.commit()

userthomas = session.query(UserM).filter_by(email="thomas@gmail.com").first()
new_note4 = NotesM(title="Therapy", body="Setup session tomorrow at 9am", user_id=4)
session.add(new_note4)
session.commit()

userthomas = session.query(UserM).filter_by(email="thomas@gmail.com").first()
new_note4 = NotesM(title="Shopping", body="Setup some cash", user_id=4)
session.add(new_note4)
session.commit()

new_user5 = UserM(first_name="Arnold", last_name="Sheikh", email="arnold@gmail.com",is_admin=False, password=str(bcrypt.generate_password_hash("pPass12fds3!!!."), 'utf-8'))
session.add(new_user5)
session.commit()

userthomas = session.query(UserM).filter_by(email="thomas@gmail.com").first()
new_note4 = NotesM(title="Everyone", body="One user id missing", user_id=3)
session.add(new_note4)
session.commit()