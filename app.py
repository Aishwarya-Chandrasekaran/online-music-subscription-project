from flask import Flask, render_template, request, redirect,session
import requests
import json
import boto3
import os
from flask import jsonify
from flask_session import Session

app = Flask(__name__)
app.secret_key = os.urandom(16)
app.debug = True
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

dyn_resource = boto3.resource('dynamodb', region_name='us-east-1')

s3_client= boto3.client('s3')

def email_exists(email): #code adapted from https://docs.aws.amazon.com/code-library/latest/ug/dynamodb_example_dynamodb_GetItem_section.html
    table = dyn_resource.Table('login')
    login_det = table.get_item(
        Key={
            'email': email
        }

    )
    if 'Item' in login_det:
        return True,login_det['Item']['password'],login_det['Item']['username']
    else:
        return False,None,None


def add_user(email, username, password): #code adapted from https://docs.aws.amazon.com/code-library/latest/ug/dynamodb_example_dynamodb_PutItem_section.html
    table = dyn_resource.Table('login')
    item={
        'email': email,
        'username': username,
        'password':password
    }
    result = table.put_item(Item=item)


def remove(user,title,artist,year): #code adapted from https://docs.aws.amazon.com/code-library/latest/ug/dynamodb_example_dynamodb_DeleteItem_section.html
    email=get_email(user)
    for i in email:
        if i is not None:
            table2=dyn_resource.Table('subscription')
            table2.delete_item (
                Key ={
                    'email':i,
                    'title':title
                }
            )


def get_email(user): #code adapted from https://docs.aws.amazon.com/code-library/latest/ug/dynamodb_example_dynamodb_Scan_section.html
    table1=dyn_resource.Table('login')
    log_det=table1.scan()
    result=log_det.get('Items',[])
    emails=[]
    for i in result:
        if i.get('username')== user:
            email= i.get('email')
            emails.append(email)
    return emails


def add_remove(user,a_title,a_artist,a_year): #code adapted from https://docs.aws.amazon.com/code-library/latest/ug/dynamodb_example_dynamodb_PutItem_section.html
    email=get_email(user)
    for i in email:
        if i is not None:
            table2=dyn_resource.Table('subscription')
            items=[{
                'email':i,
                'title':a_title,
                'artist':a_artist,
                'year':a_year
            }]

            for item in items:
                table2.put_item(Item=item)


def get_music_details(title,artist,year): #code adapted from https://docs.aws.amazon.com/code-library/latest/ug/dynamodb_example_dynamodb_Scan_section.html
    table=dyn_resource.Table('music')
    music=table.scan()
    titles=[]
    artists=[]
    years=[]
    m_artists=[]
    m_years=[]
    m_titles=[]
    music_det=table.scan()
    result=music_det.get('Items',[])

    for i in result:
        m_title=i.get('title')
        m_artist=i.get('artist')
        m_year=i.get('year')
        m_titles.append(m_title)
        m_artists.append(m_artist)
        m_years.append(m_year)

    if title and not artist and not year:
        if title.lower() in [t.lower() for t in m_titles]:

            for i in result:
                if i.get('title').lower()==title.lower():
                    m_title=i.get('title')
                    m_artist=i.get('artist')
                    m_year=i.get('year')
                    titles.append(m_title)
                    artists.append(m_artist)
                    years.append(m_year)


            return titles,artists,years
        else:
            return None,None,None

    elif artist and not title and not year:
        if artist.lower() in [a.lower() for a in m_artists]:
            for i in result:
                if i.get('artist').lower()==artist.lower():
                    m_artist=i.get('artist')
                    m_title=i.get('title')
                    m_year=i.get('year')
                    titles.append(m_title)
                    artists.append(m_artist)
                    years.append(m_year)

            return titles,artists,years
        else:
            return None,None,None



    elif year and not title and not artist:
        if year in m_years:
            for i in result:
                if i.get('year').lower()==year.lower():
                    m_year=i.get('year')
                    m_title=i.get('title')
                    m_artist=i.get('artist')
                    titles.append(m_title)
                    artists.append(m_artist)
                    years.append(m_year)

            return titles,artists,years
        else:
            return None,None,None

    elif title and artist and not year:
        if title.lower() in [t.lower() for t in m_titles] and artist.lower() in [a.lower() for a in m_artists]:
            for i in result:
                if i.get('title').lower()==title.lower() and i.get('artist').lower()==artist.lower():
                    m_title=i.get('title')
                    m_artist=i.get('artist')
                    m_year=i.get('year')
                    titles.append(m_title)
                    artists.append(m_artist)
                    years.append(m_year)
                return titles,artists,years
            else:
                return None,None,None



    elif artist and year and not title:
        if artist.lower() in [a.lower() for a in m_artists] and year in m_years:
            for i in result:
                if i.get('artist').lower()==artist.lower() and i.get('year').lower()==year.lower():
                    m_artist=i.get('artist')
                    m_year=i.get('year')
                    m_title=i.get('title')
                    titles.append(m_title)
                    artists.append(m_artist)
                    years.append(m_year)
                return titles,artists,years
            else:
                return None,None,None


    elif year and title and not artist :
        if year in m_years and title in [t.lower() for t in m_titles]:
            for i in result:
                if i.get('year').lower()==year.lower() and i.get('title').lower()==title.lower():
                    m_year=i.get('year')
                    m_title=i.get('title')
                    m_artist=i.get('artist')
                    titles.append(m_title)
                    artists.append(m_artist)
                    years.append(m_year)
                return titles,artists,years
            else:
                return None,None,None


    elif title and artist and year :
        if title.lower() in [t.lower() for t in m_titles] and artist.lower() in [a.lower() for a in m_artists] and year in m_years :
            for i in result:
                if i.get('title').lower()==title.lower() and i.get('artist').lower()==artist.lower() and i.get('year').lower()==year.lower():
                    m_year=i.get('year')
                    m_title=i.get('title')
                    m_artist=i.get('artist')
                    titles.append(m_title)
                    artists.append(m_artist)
                    years.append(m_year)
                return titles,artists,years
            else:
                return None,None,None

    return None,None,None
def get_remove(user): #code adapted from https://docs.aws.amazon.com/code-library/latest/ug/dynamodb_example_dynamodb_Scan_section.html
    email= get_email(user)
    table2=dyn_resource.Table('subscription')
    titles=[]
    artists=[]
    years=[]
    sub_det=table2.scan()
    result=sub_det.get('Items',[])
    for i in result:
        for e in email:
            if i.get('email')==e:
               titles.append(i.get('title'))
               artists.append(i.get('artist'))
               years.append(i.get('year'))
    return titles,artists,years



def collect_bucket(artists): #code adapted from https://alexwlchan.net/2017/listing-s3-keys/
    obj_lists = s3_client.list_objects(Bucket='mybucket.newassign')
    img_urls=[]
    try:
        if 'Contents' in obj_lists:
            for obj in obj_lists['Contents']:
                key = obj['Key']
                for artist in artists:
                    artist_name = artist.replace(" ", "") + '.jpg'
                    if artist_name == key:
                        img_url = f"https://mybucket.newassign.s3.amazonaws.com/{artist_name}"
                        img_urls.append(img_url)




        return img_urls
    except Exception as e:
        return None


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if request.form.get('button') == 'Login':
            email = request.form.get('email')
            password = request.form.get('password')
            e_res,pass_res,usr_res=email_exists(email)
            if e_res and pass_res==password:
                session['username'] = usr_res

                return render_template('main.html',username=usr_res)
            else:

                return render_template('index.html',message='The email or password is invalid')

        else:
            return render_template('register.html')

    elif request.method == 'GET':
        return render_template('index.html',message=' ')

@app.route ('/login',methods=['GET', 'POST'])
def login():

    if request.method =='POST':
        email = request.form.get('email')
        username=request.form.get('username')
        password=request.form.get('password')
        e_res,pass_res,usr_res=email_exists(email)
        if e_res:
            return render_template('index.html',message='The email already exists.')
        else:
            add_user(email,username,password)
            return render_template('message.html')
    else:
        return render_template('index.html',message=' ')



@app.route('/get_subscribed_details', methods=['GET'])
def get_subscribed_details(): #code adapted from https://stackoverflow.com/questions/34570660/how-to-correctly-use-flasks-jsonify-to-return-json
    titles=[]
    artists=[]
    years=[]
    images=[]
    user = session.get('username')
    titles, artists, years = get_remove(user)
    images = collect_bucket(artists)
    subscribed_details = {
        'titles': titles,
        'artists': artists,
        'years': years,
        'images': images
    }
    return jsonify(subscribed_details)


@app.route('/remove_subscribed',methods=['POST'])
def remove_fun():
    user = session.get('username') #code adapted from https://pythonbasics.org/flask-sessions/
    title = request.form.get('title')
    artist = request.form.get('artist')
    year = request.form.get('year')
    remove(user, title, artist, year)
    return redirect('/get_subscribed_details')


@app.route('/query', methods=['POST'])
def mainpage():
    user = session.get('username') #code adapted from https://pythonbasics.org/flask-sessions/
    titles = []
    artists = []
    years = []
    images = []

    if  request.method == 'POST':
        if request.form.get('button') == 'Query':
            title = request.form.get('title')
            artist = request.form.get('artist')
            year = request.form.get('year')
            titles, artists, years = get_music_details(title, artist, year)
            images=collect_bucket(artists)

            if titles is not None and artists is not None and years is not None and images is not None :
                session['titles'] = titles
                session['artists'] = artists
                session['years'] = years


                return render_template('main.html',username=user, results=zip(titles, artists, years, images ), message='')
            else:
                return render_template('main.html', username=user,message='No result is retrieved. Please query again.')

        elif request.form.get('button') == 'Subscribe':
            s_titles=[]
            s_artists=[]
            s_years=[]
            s_images=[]

            a_title = request.form.get('title_1')
            a_artist = request.form.get('artist_1')
            a_year = request.form.get('year_1')
            add_remove(user, a_title, a_artist, a_year)
            s_titles = session.get('titles')
            s_artists = session.get('artists')
            s_years = session.get('years')
            s_titles.remove(a_title)
            s_artists.remove(a_artist)
            s_years.remove(a_year)

            s_images = collect_bucket(s_artists)
            return render_template('main.html',username=user, results=zip(s_titles, s_artists, s_years, s_images), message='')


@app.route('/register')
def reg():
    return render_template('register.html')



@app.route('/logout',methods=['GET','POST'])
def logout():
    return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)
