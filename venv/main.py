from flask import Flask, request, flash, session, url_for, redirect, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import null
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gogle.sqlite3'
app.config['SECRET_KEY'] = "abcdefg anything"

db = SQLAlchemy(app)

class product(db.Model):#상품
    p_id = db.Column(db.Integer, primary_key = True, unique = True, autoincrement = True)
    p_title = db.Column(db.String(30))
    p_keyword = db.Column(db.String(50))
    p_content = db.Column(db.Boolean, default=False, nullable=False)
    # p_sold = db.Column(db.String(50), nullable=True)
    #상품이미지 저장하는방법 추가필요
    def __init__(self, title, keyword, content, sold):
        self.title = title
        self.p_keyword = keyword
        self.p_content = content
        self.p_sold = sold
# 팔로워 테이블 폼
# (외래 키 이외의 데이터가 없는 보조 테이블이기 때문에 모델 클래스 없이 생성함)        
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)
        
class User(db.Model):#회원
    __tablename__ = 'users'   #테이블 이름 : users

    id = db.Column(db.Integer, primary_key = True, unique = True, autoincrement = True)
    u_id = db.Column(db.String(30)) 
    u_pw = db.Column(db.String(100))
    u_email = db.Column(db.String(100))
    u_name = db.Column(db.String(30))
    #follower<=>followee 추가필요
    followed = db.relationship(
        'member', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    
    def __init__(self, id, pw, email, name):
        self.u_id = id
        self.u_pw = pw
        self.u_email = email
        self.u_name = name
        
    # user가 self에 follow하기
    def follow(self, user):
        if not self.is_following(user): # follow 상태가 아닌지 확인
            self.followed.append(user)  # user가 self에 follow
    # user가 self에 되어있는 follow 제거
    def unfollow(self, user):
        if self.is_following(user):     # follow 상태인지 확인
            self.followed.remove(user)  # user가 self에 follow
    # 두 사용자 간의 링크가 존재하는지 확인
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
        
# 팔로우 routes 설정
######## username을 팔로우 시도 ############
# @app.route('/follow/<username>')
# @login_required
# def follow(username):
#     user = User.query.filter_by(username=username).first()
#     if user is None:
#         flash('User {} not found.'.format(username))
#         return redirect(url_for('index'))
#     if user == current_user:
#         flash('You cannot follow yourself!')
#         return redirect(url_for('user', username=username))
#     current_user.follow(user)
#     db.session.commit()
#     flash('You are following {}!'.format(username))
#     return redirect(url_for('user', username=username))   



# 기본화면1 - 상품목록+로그인(지원파트) + 로그인시만 가능한 기능ui 권한추가(상품수정,글쓰기)
@app.route('/')
def index():
    return render_template('index.html'
                        #    , members = member.query.all()
                           )

# 기본화면2 - (지원파트) keyword검색시 요청
@app.route('/jiwon/<p_keyword>', methods = ['GET'])
def indexSearch(key):
    members = members.query.filter_by(p_keyword = key).all()
    return render_template('index.html', members)


#회원가입(POST) - 회원 정보 입력(지원파트)
@app.route('/update/<student_id>', methods = ['GET', 'POST'])
def update(student_id):
    # update_student = students.query.filter_by(id = student_id).first()
    # if request.method == 'POST': #=> POST요청 왔을때
    #         if not request.form['s_id'] or not request.form['s_name']:
    #             flash('Please enter all the fields', 'error')
    #         else:
    #             update_student.s_id = request.form['s_id']
    #             update_student.s_name = request.form['s_name']
    #             db.session.commit()
 
    #             flash('Record was successfully updated')
                # return redirect(url_for('show_students'))
 
    # return render_template('edit.html', student = update_student)#add_new.html =>GET요청왔을때 폼
    return render_template('edit.html', users = User.query.all())

    
# 추가(POST) - 상품 등록/수정 (승기파트) + 로그인시만 가능한 권한추가
@app.route('/add_post', methods = ['GET', 'POST'])
def add_post():
  #로그인 세션정보('userid')가 있을 경우
	if not session.get('userid'):  
		return render_template('home.html')
	
	#로그인 세션정보가 없을 경우
	else:		
		userid = session.get('userid') 
		if request.method == 'POST':#=> POST요청 왔을때
      
            if not request.form['p_title'] or not request.form['p_keyword'] or not request.form['p_content']:
                flash('Please enter all the fields', 'error')
            else:
                pd = product(request.form['p_title'],
                                    request.form['p_keyword'], 
                                    request.form['p_content'],
                                        False if request.form.get('p_sold')==None else True
                                    )
                db.session.add(pd)
                print(pd.p_sold)
                try:
                    db.session.commit()
                except SQLAlchemyError as e:
                    reason=str(e)
                    flash(reason)
                    flash('Record was successfully added')
                    return redirect(url_for('index'))
                return render_template('add_post.html') #add_new.html =>GET요청왔을때 폼    

    



    

# 마이페이지
@app.route('/mypage', methods = ['GET', 'POST'])
def my_page():
 if request.method == 'POST':#=> POST요청 왔을때
   
        return redirect(url_for('index'))
 return render_template('mypage.html'
                        # , members = member.query.all()
                        # , products =product.query.all()
                        )

if __name__ == '__main__':
    db.create_all()
    app.run()