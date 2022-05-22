from flask import Flask, request, flash, url_for, redirect, render_template
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
        
class member(db.Model):#회원
    id = db.Column(db.Integer, primary_key = True, unique = True, autoincrement = True)
    m_id = db.Column(db.String(30)) 
    m_pw = db.Column(db.String(100))
    m_email = db.Column(db.String(100))
    m_name = db.Column(db.String(30))
    #follower<=>followee 추가필요
    def __init__(self, id, pw, email, name):
        self.m_id = id
        self.m_pw = pw
        self.m_email = email
        self.m_name = name
        

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
    return render_template('edit.html', members = member.query.all())

    
# 추가(POST) - 상품 등록/수정 (승기파트) + 로그인시만 가능한 권한추가
@app.route('/add_post', methods = ['GET', 'POST'])
def add_post():
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