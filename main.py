# İçeri Aktarma
from flask import Flask, render_template,request, redirect
# Veritabanı kütüphanesini içe aktarma
from flask_sqlalchemy import SQLAlchemy


#Oluşturduğumuz uygulama python dosyamızın ismini alıyor.
app = Flask(__name__)


#app'imizi yapılandıracağız. --> app.config[]
# 'SQLALCHEMY_DATABASE_URI' --> veritabanımın nerede oluşacağını belirtir.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
# 'SQLALCHEMY_TRACK_MODIFICATIONS' --> SQLAlchemy'nin model nesnelerindeki değişiklikleri otomatik olarak takip edip yönetmesini sağlar.
# True --> Otomatik bir şekilde kontrol edilir.
# False --> Manuel bir şekilde kontrol edilir.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# DB oluşturma
db = SQLAlchemy(app)

#Görev #1. DB tablosu oluşturma

# class --> bizim tablo oluşturuken kuallanacağımız anahtar kelimedir.
# Globalde class isimleri büyük harfle başlar bu yüzden büyük harfle başlarız.
# paranteze --> db_ismi.Model kodunu yazarız.

class Card(db.Model):
    # (id) kimlik numarası --> Benzersiz bir kimlik numarası oluşturarak biz girdiğimiz verileri doğru bir şekilde gelmesini sağlayacağız
    # db bir column oluşturacağımı belriten komut => db.Column komutudur.
    # parantezin içerisine yazmam gereken ilk şey bu sütunda hangi veri tipi olacak (Integer(Sayısal), String(Harf), Boolean(Mantık))
    # primary_key --> Bu özellik eğer True olarak işaretlenirse bu sutunda hiç bir veri birbirine benzemez.
    id = db.Column(db.Integer, primary_key = True )
    # string değerde kelime sınırlaması koymak istiyorsak --> db.String()
    # nullable özelliği False olarak ayarlanırsa boş bırakılmaz, boş bırakılmasını isterseniz True yazabilirsiniz.
    title = db.Column(db.String(100), nullable=False)
    # string değerde kelime sınırlaması koymak istiyorsak --> db.String()
    # nullable özelliği False olarak ayarlanırsa boş bırakılmaz, boş bırakılmasını isterseniz True yazabilirsiniz.
    subtitle = db.Column(db.String(50), nullable=False)
    # string değerde kelime sınırlaması koymak istiyorsak --> db.String()
    # nullable özelliği False olarak ayarlanırsa boş bırakılmaz, boş bırakılmasını isterseniz True yazabilirsiniz.
    text = db.Column(db.String, nullable=False)


   # Nesneyi ve id'sine göre yazdırma
    def __repr__(self):
        return f'<Card {self.id}>'


# İçerik sayfasını çalıştırma
@app.route('/')
def index():
    # DB nesnelerini görüntüleme
    # Görev #2. DB'deki nesneleri index.html'de görüntüleme
    cards = Card.query.order_by(Card.id).all()


    return render_template('index.html',
                           #kartlar = kartlar
                            cards = cards
                           )

# Kartla sayfayı çalıştırma
@app.route('/card/<int:id>')
def card(id):
    # Görev #2. Id'ye göre doğru kartı görüntüleme
    card = Card.query.get(id)

    return render_template('card.html', card=card)

# Sayfayı çalıştırma ve kart oluşturma
@app.route('/create')
def create():
    return render_template('create_card.html')

# Kart formu
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        # Görev #2. Verileri DB'de depolamak için bir yol oluşturma
        card = Card(title=title, subtitle=subtitle, text=text)
        #değişkende ki verileri veri tablomda saklamak için kullandığım komut
        db.session.add(card)
        #Değişkenleri veritabanına commitlemem (göndermem) için gerekli olan komut:
        db.session.commit()

        return redirect('/')
    else:
        return render_template('create_card.html')


if __name__ == "__main__":
    app.run(debug=True)
