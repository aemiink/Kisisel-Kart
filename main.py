# İçe aktar
from flask import Flask, render_template,request, redirect
# Veri tabanı kitaplığını bağlama
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# SQLite'ı bağlama
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Veri tabanı oluşturma
db = SQLAlchemy(app)
# Tablo oluşturma

class Card(db.Model):
    # Sütun oluşturma
    # id
    id = db.Column(db.Integer, primary_key=True)
    # Başlık
    title = db.Column(db.String(100), nullable=False)
    # Tanım
    subtitle = db.Column(db.String(300), nullable=False)
    # Metin
    text = db.Column(db.Text, nullable=False)

    # Nesnenin ve kimliğin çıktısı
    def __repr__(self):
        return f'<Card {self.id}>'
    

#Ödev #2. Kullanıcı tablosunu oluşturun
class User(db.Model):
    # Sütun Oluşturma
    # id
    # db.Column --> Sütun Oluştururuz
    # db.Integer --> Tam Sayıları kapsayan değerler sadece bu sutunda depolancak
    # primary_key=True  --> SBenzersiz bir kimlik numarasına sahip olacağını belriler.
    # autoincrement=True --> Otomatik olarak dolacağı anlamına gelir.
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    #Kullanıcı Adı
    # db.Column --> Sütun Oluştururuz
    # db.String --> Harfleri ve sayıları kapsayan değerler sadece bu sutunda depolancak
    # nullable=False --> Databse'de buranın boş kalmyacağını db'ye bildiririz.
    username = db.Column(db.String(100), nullable=False)


    #Şifre
    # db.Column --> Sütun Oluştururuz
    # db.String --> Harfleri ve sayıları kapsayan değerler sadece bu sutunda depolancak
    # nullable=False --> Databse'de buranın boş kalmyacağını db'ye bildiririz.
    password = db.Column(db.String(30), nullable=False)


   # Nesnenin ve kimliğin çıktısı
    def __repr__(self):
        return f'<Card {self.id}>'





# İçerik sayfasını çalıştırma
@app.route('/', methods=['GET','POST'])
def login():
        error = ''
        if request.method == 'POST':
            form_login = request.form['email']
            form_password = request.form['password']
            
            #Ödev #4. yetkilendirmeyi uygulamak
            # User.query.all() --> User tablosundaki tüm verileri bir değişkende depolamamızı sağlar.
            users_db = User.query.all()
            for user in users_db:
                if form_login == user.username and form_password == user.password:
                    return redirect('/index')
                else:
                    error = 'Hatalı Giriş Yaptınız, Lütfen Tekrar Deneyiniz.'
            return render_template('login.html', error=error) 
        
        else:
            return render_template('login.html')



@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        login= request.form['email']
        password = request.form['password']
        
        #Ödev #3 Kullanıcı verilerinin veri tabanına kaydedilmesini sağlayın
        user = User(username=login, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect('/')
    else:    
        return render_template('registration.html')


# İçerik sayfasını çalıştırma
@app.route('/index')
def index():
    # Veri tabanı girişlerini görüntüleme
    cards = Card.query.order_by(Card.id).all()
    return render_template('index.html', cards=cards)

# Kayıt sayfasını çalıştırma
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)

# Giriş oluşturma sayfasını çalıştırma
@app.route('/create')
def create():
    return render_template('create_card.html')

# Giriş formu
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        # Veri tabanına gönderilecek bir nesne oluşturma
        card = Card(title=title, subtitle=subtitle, text=text)

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')





if __name__ == "__main__":
    app.run(debug=True)
