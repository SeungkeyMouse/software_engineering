# from crypt import methods
from queue import Empty
from flask import Flask, flash, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.secret_key="123123123"

# database 설정파일x
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///gogle2.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#파일업로드 prefix 부분만 고치면됩니다
file_location_prefix = '/Users/ksg19/software_engineering/venv/static'
file_location_postfix = '/uploads'
app.config['UPLOAD_FOLDER'] = file_location_prefix+file_location_postfix

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
    p_content = db.Column(db.String(200))
    p_sold = db.Column(db.String(2))
    p_img = db.Column(db.String(200))
    u_id = db.Column(db.String(32), db.ForeignKey('users.userid'))
    b = db.relationship('User', backref=db.backref('product_by_main', uselist=False))
    #상품이미지 저장하는방법 추가필요
    def __init__(self, title, keyword, content, sold, img, u_id):
        self.p_title = title
        self.p_keyword = keyword
        self.p_content = content
        self.p_sold = sold
        self.p_img = img
        self.u_id = u_id
        
class follower_following(db.Model):
    id = db.Column(db.Integer,autoincrement = True, primary_key= True)
    follower_id = db.Column(db.String(32))#나
    followee_id = db.Column(db.String(32))#내가 팔로우하는 인간들
    
    #follow생성
    def __init__(self, myid, yourid):
        self.follower_id = myid;
        self.followee_id = yourid;

@app.route('/follow', methods = ['POST'])
def follow():
    if request.method=="POST":
        product_uploader = request.form['uploader']
        user = User.query.filter_by(userid = session.get('userid')).first()
        print(product_uploader)
        #'내'가 팔로우 해놓은 사람들 불러오기
        f_t = follower_following.query.filter_by(follower_id = user.userid, followee_id=product_uploader).first()
        print(f_t)
        if f_t is not None:
            # print("이미 팔로우한회원")
            flash("이미 팔로우 한 회원입니다.")
        else:
            f_table = follower_following(
				user.userid,
				product_uploader
			)
            db.session.add(f_table)
            db.session.commit()
            #완료알림
            flash(product_uploader + "님을 팔로우하였습니다!")
    return redirect("/")

# 추가(POST) - 상품 등록/수정 (승기파트) + 로그인시만 가능한 권한추가
@app.route('/add_post', methods = ['GET', 'POST'])
def add_post():
	if request.method =='GET':
		if not session.get('userid'):  #로그인 세션정보('userid')가 없을 경우
			return render_template('home.html')
		else:#로그인 세션정보가 있을 경우		
			return render_template('add_post.html')
	else:#POST요청인경우
		f = request.files['photo']
		f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
		f_path = file_location_postfix + '/' + f.filename
		print(f_path)
  
		user = User.query.filter_by(userid = session.get('userid')).first()
		pd = product(
      				request.form['p_title'],
                    request.form['p_keyword'], 
                    request.form['p_content'],
                    "X" if request.form.get('p_sold')==None else "O",
                    f_path,
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
        
# 제품상세페이지
@app.route('/show_post/<int:id>')
def show_post(id):
    return render_template('show_post.html',products =product.query.filter_by(p_id = id).first()) 
        


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
			else:# 쿼리 데이터가 없으면 출력
				flash("올바른 아이디 혹인 비밀번호를 입력해주세요")
				return redirect('/')
		except:
			return "dont login"	# 예외 상황 발생 시 출력

@app.route('/logout', methods=['GET'])
def logout():
	session.pop('userid', None)
	return redirect('/')


if __name__ == '__main__':
    db.create_all()
    app.run()

