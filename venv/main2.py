from crypt import methods
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
    userid = db.Column(db.String(32), unique=True)
    username = db.Column(db.String(8))
    password = db.Column(db.String(64))
   

    
class product(db.Model):#상품
    p_id = db.Column(db.Integer, primary_key = True, unique = True, autoincrement = True)
    p_title = db.Column(db.String(50))
    p_keyword = db.Column(db.String(50))
    p_content = db.Column(db.String(100))
    p_sold = db.Column(db.String(2))
    u_id = db.Column(db.String(32), db.ForeignKey('users.userid'))
    b = db.relationship('User', backref=db.backref('product_by_main', uselist=False))
    #상품이미지 저장하는방법 추가필요
    def __init__(self, title, keyword, content, sold, u_id):
        self.p_title = title
        self.p_keyword = keyword
        self.p_content = content
        self.p_sold = sold
        self.u_id = u_id
        
class follower_following:
    id = db.Column(db.Integer, primary_key= True)
    follower_id = db.Column(db.String(32))
    followee_id = db.Column(db.String(32))
    
# 추가(POST) - 상품 등록/수정 (승기파트) + 로그인시만 가능한 권한추가
@app.route('/add_post', methods = ['GET', 'POST'])
def add_post():
	if request.method =='GET':
		if not session.get('userid'):  #로그인 세션정보('userid')가 있을 경우
			return render_template('home.html')
		else:#로그인 세션정보가 없을 경우		
			return render_template('add_post.html')
	else:#POST요청인경우
		user = User.query.filter_by(userid = session.get('userid')).first()
		pd = product(
      				request.form['p_title'],
                    request.form['p_keyword'], 
                    request.form['p_content'],
                    "X" if request.form.get('p_sold')==None else "O",
                    user.userid
    	            )
		db.session.add(pd)
		db.session.commit()
		return redirect('/')

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
			return redirect('/')
		
	
@app.route('/')
def home():
    
    
	#로그인 세션정보('userid')가 있을 경우
	if not session.get('userid'):  
		return render_template('home.html', products =product.query.all())
	
	#로그인 세션정보가 없을 경우
	else:		
		userid = session.get('userid') 
		return render_template('home.html', userid=userid, products =product.query.all())
#팔로우기능
# @app.route('/follow')
# def follow():
#     if not session.get('userid'):
#         return render_template('home.html', products =product.query.all())
#     else:
        

# 마이페이지
@app.route('/mypage', methods = ['GET', 'POST'])
def my_page():
	if request.method == 'POST':#=> POST요청 왔을때
	
			return redirect('/')
	skey= 1
	#print(type(skey))
	user_id = session.get('userid')
	#print(type(user_id))
	user = User.query.filter_by(userid = session.get('userid')).first()
	#print(user.id)
	
	return render_template('mypage.html'
							,  members = User.query.filter_by(userid = session.get('userid')).all()
							, products =product.query.filter_by(u_id = user.userid).all()
							)



# 키워드서치
@app.route('/keywordSearch',methods=['GET','POST'])
def keywordSearch():
    if request.method =='POST':
        kk=request.form['kk']
        return render_template('keywordSearch.html',products =product.query.filter_by(p_keyword = kk).all()) 
        
   



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