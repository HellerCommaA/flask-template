# gunicorn -b 50.116.40.148:80 runproduction:app &
# git reset --hard
#GIT : devbox1 / PASSword00!!
from app import app
if __name__ == '__main__':
	app.run(debug = False)
