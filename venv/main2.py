from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.secret_key="123123123"

# database 설정파일
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///gogle2.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'   #테이블 이름 : users

    id = db.Column(db.Integer, primary_key = True)   #id를 프라이머리키로 설정
    userid = db.Column(db.String(32))
    username = db.Column(db.String(8))
    password = db.Column(db.String(64))
    
@app.route('/register', methods=['GET','POST'])
def register():
	if request.method =='GET':
		return render_template("register.html")
	else:
		userid = request.form.get('userid')
		username = request.form.get('username')
		password = request.form.get('password')
		re_password = request.form.get('re_password')

		if not (userid and username and password and re_password):
			return "모두 입력해주세요"
		elif password != re_password:
			return "비밀번호를 확인해주세요"
		else:
			user = User()
			user.password = password
			user.userid = userid
			user.username = username
			db.session.add(user)
			db.session.commit()
			return "회원가입 완료"
		return redirect('/')

@app.route('/')
def home():
	#로그인 세션정보('userid')가 있을 경우
	if not session.get('userid'):  
		return render_template('home.html')
	
	#로그인 세션정보가 없을 경우
	else:		
		userid = session.get('userid') 
		return render_template('home.html', userid=userid)


# 마이페이지
@app.route('/mypage', methods = ['GET', 'POST'])
def my_page():
 if request.method == 'POST':#=> POST요청 왔을때
   
        return redirect('/')
 return render_template('mypage.html'
                        # , members = member.query.all()
                        # , products =product.query.all()
                        )







@app.route('/login', methods=['GET', 'POST'])	
def login():
	if request.method=='GET':
		return render_template('home.html')
	else:
		userid = request.form['userid']
		password = request.form['password']
		try:
			data = User.query.filter_by(userid=userid, password=password).first()	# ID/PW 조회Query 실행
			if data is not None:	# 쿼리 데이터가 존재하면
				session['userid'] = userid	# userid를 session에 저장한다.
				return redirect('/')
			else:
				return 'Dont Login'	# 쿼리 데이터가 없으면 출력
		except:
			return "dont login"	# 예외 상황 발생 시 출력

@app.route('/logout', methods=['GET'])
def logout():
	session.pop('userid', None)
	return redirect('/')


if __name__ == '__main__':
    db.create_all()
    app.run()