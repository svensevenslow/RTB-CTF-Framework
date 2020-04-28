import pytz
from datetime import datetime

from FlaskRTBCTF import db, bcrypt, create_app
from FlaskRTBCTF import User, Notification, Machine, Settings, Website, Logs
from FlaskRTBCTF.utils import handle_admin_pass


app = create_app()

# create_app().app_context().push()
with app.app_context():
    db.create_all()

    default_time = datetime.now(pytz.utc)

    web1 = Website(
        name="Official Abs0lut3Pwn4g3 Website", url="https://Abs0lut3Pwn4g3.github.io/",
    )
    web2 = Website(name="Twitter", url="https://twitter.com/Abs0lut3Pwn4g3",)
    web3 = Website(
        name="GitHub", url="https://github.com/Abs0lut3Pwn4g3/RTB-CTF-Framework"
    )

    db.session.add(web1)
    db.session.add(web2)
    db.session.add(web3)

    settings = Settings(dummy=False)

    db.session.add(settings)

    notif = Notification(
        title=f"Welcome to {settings.ctf_name}",
        body="The CTF is live now. Please read rules!",
    )
    db.session.add(notif)

    box = Machine(
        name="My Awesome Pwnable Box",
        user_hash="A" * 32,
        root_hash="B" * 32,
        user_points=10,
        root_points=20,
        os="linux",
        ip="127.0.0.1",
        hardness="Easy",
    )
    db.session.add(box)

    passwd = handle_admin_pass()
    admin_user = User(
        username="admin",
        email="admin@admin.com",
        password=bcrypt.generate_password_hash(passwd).decode("utf-8"),
        isAdmin=True,
    )
    db.session.add(admin_user)

    admin_log = Logs(
        user=admin_user,
        accountCreationTime=default_time,
        visitedMachine=True,
        machineVisitTime=default_time,
    )
    db.session.add(admin_log)

    db.session.commit()