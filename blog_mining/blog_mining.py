import os
from datetime import date
from flask import Flask,render_template,request,url_for,redirect,flash
from flask_mail import Mail, Message
from flask_mysqldb import MySQL
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from werkzeug.utils import secure_filename
import time


#summarization part
import sys
sys.path.insert(0, 'B:/Project/Blog_mining/summarizer')
from summarizer import lsa_summarizer
from lsa_summarizer import LsaSummarizer
import nltk
from nltk.corpus import stopwords


#summarize
def summarize(text):
    q=len(text.split("."))-1
    p=q
    '''
    txt=""
    p=text.split(".")
    p=p[:-1]
    r=""
    for i in p:
        r=""
        if("'" in i):
            for j in i:
                if(j=="'"):
                    r+=j+"'"
                else:
                    r+=j
        else:
            r+=i
        if(i[0]==' '):
            txt+=r+"."
        else:
            txt+=" "+r+"."
    '''
    if(q>=8):
        if(q>=70):
            q-=45
        elif(q>=60):
            q-=35
        elif(q>=50):
            q-=30
        elif(q>=40):
            q-=25
        elif(q>=30):
            q-=17
        elif(q>=20):
            q-=12
        elif(q>=12):
            q-=6
        elif(q>=8):
            q-=2
        nltk.download("punkt", quiet=True)
        nltk.download("stopwords", quiet=True)
        summarizer = LsaSummarizer()
        stopWords = stopwords.words('english')
        summarizer.stop_words = stopWords
        summary =summarizer(text,q)
        return " ".join(summary)
        #return str(p)+" "+str(q)
    else:
        return text

def content_morphe(text):
    txt=""
    p=text.split(".")
    if(len(p)!=1):
        p=p[:-1]
    r=""
    for i in p:
        r=""
        if("'" in i):
            for j in i:
                if(j=="'"):
                    r+=j+"'"
                else:
                    r+=j
        else:
            r+=i
        if(i[0]==' '):
            txt+=r+"."
        else:
            txt+=" "+r+"."
    return txt

LETTERS_SMALLS = 'abcdefghijklmnopqrstuvwxyz'
LETTERS_CAPS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUMBERS = '0123456789'


#Encryption
def encrypt(message, key):
    encrypted = ''
    key1=key
    if(key1>10):
        key1=key%10
    if(key>26):
        key=key%26
    for chars in message:
        if chars in LETTERS_SMALLS:
            num = LETTERS_SMALLS.find(chars)
            num =num+key
            if(num>=26):
                num=num%26
            encrypted +=  LETTERS_SMALLS[num]
        elif chars in LETTERS_CAPS:
            num = LETTERS_CAPS.find(chars)
            num =(num+key)
            if(num>=26):
                num=num%26
            encrypted +=  LETTERS_CAPS[num]
        elif chars in NUMBERS:
            num = NUMBERS.find(chars)
            num =num+key1
            if(num>=10):
                num=num%10
            encrypted +=  NUMBERS[num]
        else:
            encrypted+=chars
    return encrypted


#Decryption
def decrypt(message, key):
    decrypted = ''
    key1=key
    if(key1>10):
        key1=key%10
    if(key>26):
        key=key%26
    for chars in message:
        if chars in LETTERS_SMALLS:
            num = LETTERS_SMALLS.find(chars)
            num =num-key
            decrypted +=  LETTERS_SMALLS[num]
        elif chars in LETTERS_CAPS:
            num = LETTERS_CAPS.find(chars)
            num =num-key
            decrypted +=  LETTERS_CAPS[num]
        elif chars in NUMBERS:
            num = NUMBERS.find(chars)
            num =num-key1
            decrypted +=  NUMBERS[num]
        else:
            decrypted+=chars
    return decrypted



UPLOAD_FOLDER = 'B:/Project/Blog_mining/static'

s = URLSafeTimedSerializer('Thisisasecret!')


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'blog_mining'
mysql = MySQL(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


mail= Mail(app)
email=''
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



@app.route("/")
def index():
    try:
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM post ORDER BY NUM_VIEWS DESC LIMIT 4")
        records=cur.fetchall()
        featured=[]
        i=0
        even=[]
        odd=[]
        for row in records:
            content=row[7][:115]+str("...")
            if(i%2==0):
                even.append({'id':row[0],'category':row[1],'title':row[2],'updated_by':row[3],'updated_on':row[4],'num_min':row[5],'num_views':row[6],'content':content,'photo':row[8]})
            else:
                odd.append({'id':row[0],'category':row[1],'title':row[2],'updated_by':row[3],'updated_on':row[4],'num_min':row[5],'num_views':row[6],'content':content,'photo':row[8]})
            i+=1
        featured.extend(even)
        featured.extend(odd)
        cur.execute("SELECT * FROM post ORDER BY ID DESC LIMIT 6")
        records=cur.fetchall()
        i=0
        all_stories=[]
        first=[]
        second=[]
        third=[]
        for row in records:
            content=row[7][:150]+str("...")
            if(i==0):
                first.append({'id':row[0],'category':row[1],'title':row[2],'updated_by':row[3],'updated_on':row[4],'num_min':row[5],'num_views':row[6],'content':content,'photo':row[8]})
                i+=1
            elif(i==1):
                second.append({'id':row[0],'category':row[1],'title':row[2],'updated_by':row[3],'updated_on':row[4],'num_min':row[5],'num_views':row[6],'content':content,'photo':row[8]})
                i+=1
            elif(i==2):
                third.append({'id':row[0],'category':row[1],'title':row[2],'updated_by':row[3],'updated_on':row[4],'num_min':row[5],'num_views':row[6],'content':content,'photo':row[8]})
                i=0
        all_stories.extend(first)
        all_stories.extend(second)
        all_stories.extend(third)
        cur.execute("SELECT CATEGORY FROM post WHERE ID="+str(1))
        record=cur.fetchone()
        return render_template("index.html",featured=featured,all_stories=all_stories,token=record[0])
    except:
        return redirect(url_for('handle_exception'))



@app.route("/search",methods=['GET','POST'])
def search():
    if request.method=='POST':
        search_content=request.form['search_content']
        search_content=search_content.lower()
        if(search_content==""):
            cur=mysql.connection.cursor()
            cur.execute("SELECT CATEGORY FROM post WHERE ID="+str(1))
            record=cur.fetchone()
            return render_template("search.html",search_content=0,token=record[0],search_contents=search_content)
        tic = time.perf_counter()
        lst=search_content.split(" ")
        cur=mysql.connection.cursor()
        cur.execute("SELECT ID,CATEGORY,TITLE,CONTENT FROM post ORDER BY ID DESC")
        records=cur.fetchall()
        d={}
        for row in records:
            st=""
            p=0
            st+=row[1].lower()+" "+row[2].lower()+" "+row[3].lower()
            for i in lst:
                p+=st.count(i)
            d[row[0]]=p
        sorted_values=sorted(d.values())
        sorted_values=sorted_values[::-1]
        sorted_dict={}
        for i in sorted_values:
            for k in d.keys():
                if(i==0):
                    break
                if d[k]==i:
                    sorted_dict[k]=d[k]
                    d[k]=-1
                    break
        j=0
        search_list=[]
        even=[]
        odd=[]
        for i in sorted_dict:
            cur.execute("SELECT * FROM post WHERE ID="+str(i))
            row=cur.fetchone()
            content=row[7][:115]+str("...")
            if(j%2==0):
                even.append({'id':row[0],'category':row[1],'title':row[2],'updated_by':row[3],'updated_on':row[4],'num_min':row[5],'num_views':row[6],'content':content,'photo':row[8]})
            else:
                odd.append({'id':row[0],'category':row[1],'title':row[2],'updated_by':row[3],'updated_on':row[4],'num_min':row[5],'num_views':row[6],'content':content,'photo':row[8]})
            j+=1
        search_list.extend(even)
        search_list.extend(odd)
        cur.execute("SELECT CATEGORY FROM post WHERE ID="+str(1))
        record=cur.fetchone()
        toc = time.perf_counter()
        print(toc-tic)
        if(search_list==[]):
            return render_template("search.html",search_content=0,token=record[0],search_contents=search_content)
        else:
            return render_template("search.html",search_list=search_list,token=record[0],search_contents=search_content)



@app.route("/view_all")
def view_all():
    try:
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM post ORDER BY ID DESC")
        records=cur.fetchall()
        all_stories=[]
        i=0
        even=[]
        odd=[]
        for row in records:
            content=row[7][:115]+str("...")
            if(i%2==0):
                even.append({'id':row[0],'category':row[1],'title':row[2],'updated_by':row[3],'updated_on':row[4],'num_min':row[5],'num_views':row[6],'content':content,'photo':row[8]})
            else:
                odd.append({'id':row[0],'category':row[1],'title':row[2],'updated_by':row[3],'updated_on':row[4],'num_min':row[5],'num_views':row[6],'content':content,'photo':row[8]})
            i+=1
        all_stories.extend(even)
        all_stories.extend(odd)
        cur.execute("SELECT CATEGORY FROM post WHERE ID="+str(1))
        record=cur.fetchone()
        return render_template("view_all.html",all_stories=all_stories,token=record[0])
    except:
        return redirect(url_for('handle_exception'))



@app.route("/post/<token>")
def post(token):
    try:
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM post WHERE ID="+str(token))
        record=cur.fetchone()
        post={}
        category=record[1]
        title=record[2]
        updated_by=record[3]
        updated_on=record[4]
        num_min=record[5]
        num_views=record[6]
        content=record[7]
        photo=record[8]
        num_views=str((int(num_views)+1))
        cur.execute("UPDATE post SET NUM_VIEWS=%s WHERE ID=%s" %( num_views, str(token) ) )
        mysql.connection.commit()
        cur.execute("SELECT * FROM categories LIMIT 4")
        records=cur.fetchall()
        categories=[]
        for row in records:
            categories.append(row[0])
        cur.execute("SELECT * FROM post ORDER BY NUM_VIEWS DESC LIMIT 3")
        records=cur.fetchall()
        lst=[]
        for row in records:
            content_vary=row[7]+str("...")
            lst.append({'id':row[0],'category':row[1],'title':row[2],'updated_by':row[3],'updated_on':row[4],'num_min':row[5],'num_views':row[6],'content':content_vary,'photo':row[8]})
        return render_template("post.html",category=category,title=title,updated_by=updated_by,updated_on=updated_on,num_min=num_min,num_views=num_views,content=content,photo=photo,token=record[0],categories=categories,suggestive_posts=lst)
    except:
        return redirect(url_for('handle_exception'))



@app.route("/categories/<token>")
def categories(token):
    try:
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM categories")
        records=cur.fetchall()
        categories=[]
        for row in records:
            if(row[0]!=token):
                categories.append(row[0])
        cur.execute("SELECT * FROM post WHERE CATEGORY='%s'" %(str(token),))
        records=cur.fetchall()
        category=[]
        i=0
        even=[]
        odd=[]
        for row in records:
            content=row[7][:115]+str("...")
            if(i%2==0):
                even.append({'id':row[0],'category':row[1],'title':row[2],'updated_by':row[3],'updated_on':row[4],'num_min':row[5],'num_views':row[6],'content':content,'photo':row[8]})
            else:
                odd.append({'id':row[0],'category':row[1],'title':row[2],'updated_by':row[3],'updated_on':row[4],'num_min':row[5],'num_views':row[6],'content':content,'photo':row[8]})
            i+=1
        category.extend(even)
        category.extend(odd)
        cur.execute("SELECT CATEGORY FROM post WHERE ID="+str(1))
        record=cur.fetchone()
        if(category==[]):
            return render_template("categories.html",search_content=0,token=token,categories=categories,category=category,record=record[0])
        else:
            return render_template("categories.html",token=token,categories=categories,category=category,record=record[0])
    except:
        return redirect(url_for('handle_exception'))



@app.route("/search_category/<token>",methods=['GET','POST'])
def search_category(token):
    try:
        if request.method=='POST':
            cur=mysql.connection.cursor()
            cur.execute("SELECT ID,TITLE,CONTENT FROM post WHERE CATEGORY='%s' ORDER BY ID DESC" %(str(token),))
            records=cur.fetchall()
            search_content=request.form['search_category']
            if(search_content==""):
                cur.execute("SELECT * FROM categories")
                records=cur.fetchall()
                categories=[]
                for row in records:
                    if(row[0]!=token):
                        categories.append(row[0])
                cur.execute("SELECT CATEGORY FROM post WHERE ID="+str(1))
                record=cur.fetchone()
                return render_template("search_category.html",search_content=0,token=token,categories=categories,record=record)
            search_content=search_content.lower()
            lst=search_content.split(" ")
            d={}
            for row in records:
                st=""
                p=0
                st+=row[1].lower()+" "+row[2].lower()
                for i in lst:
                    p+=st.count(i)
                d[row[0]]=p
            sorted_values=sorted(d.values())
            sorted_values=sorted_values[::-1]
            sorted_dict={}
            for i in sorted_values:
                for k in d.keys():
                    if(i==0):
                        break
                    if d[k]==i:
                        sorted_dict[k]=d[k]
                        d[k]=-1
                        break
            j=0
            search_list=[]
            even=[]
            odd=[]
            for i in sorted_dict:
                cur.execute("SELECT * FROM post WHERE ID="+str(i))
                row=cur.fetchone()
                content=row[7][:115]+str("...")
                if(j%2==0):
                    even.append({'id':row[0],'category':row[1],'title':row[2],'updated_by':row[3],'updated_on':row[4],'num_min':row[5],'num_views':row[6],'content':content,'photo':row[8]})
                else:
                    odd.append({'id':row[0],'category':row[1],'title':row[2],'updated_by':row[3],'updated_on':row[4],'num_min':row[5],'num_views':row[6],'content':content,'photo':row[8]})
                j+=1
            search_list.extend(even)
            search_list.extend(odd)
            categories=[]
            cur=mysql.connection.cursor()
            cur.execute("SELECT * FROM categories")
            records=cur.fetchall()
            categories=[]
            for row in records:
                if(row[0]!=token):
                    categories.append(row[0])
            cur.execute("SELECT CATEGORY FROM post WHERE ID="+str(1))
            record=cur.fetchone()
            if(search_list==[]):
                return render_template("search_category.html",search_content=0,search_list=search_list,token=token,categories=categories,record=record)
            else:
                return render_template("search_category.html",search_list=search_list,token=token,categories=categories,record=record)
    except:
        return redirect(url_for('handle_exception'))



@app.route("/author",methods=['GET', 'POST'])
def author():
    if(request.method=='GET'):
        cur=mysql.connection.cursor()
        cur.execute("SELECT CATEGORY FROM post WHERE ID="+str(1))
        record=cur.fetchone()
        return render_template("author.html",token=record)
    cur=mysql.connection.cursor()
    name=request.form['name']
    mesg=request.form['message']
    sub=request.form['subject']
    email=request.form['email']
    msg=Message("Contact us",sender='19hp5a1202.alit@apssdc.info',recipients=['19hp5a1202.alit@apssdc.info'])
    msg.body="Name: "+str(name)+"\nGenerated from: "+email+"\nSubject: "+sub+"\nMessage: "+str(mesg)
    mail.send(msg)
    msg=Message(sub,sender='19hp5a1202.alit@apssdc.info',recipients=[str(email)])
    msg.body="Hi "+str(name)+"\nSubject: "+sub+"\nMessage: "+mesg+"\nWe would be in contact with you soonerr!!"
    mail.send(msg)
    cur.execute("SELECT CATEGORY FROM post WHERE ID="+str(1))
    record=cur.fetchone()
    return render_template("author.html",token=record[0])



@app.route("/login",methods=['GET','POST'])
def login():
    try:
        if request.method=='GET':
            return render_template("LOGIN.html")
        uname=request.form['username']
        pwd=request.form['password']
        cur=mysql.connection.cursor()
        cur.execute("SELECT USERNAME,PASSWORD,EID FROM login")
        records=cur.fetchall()
        flag=0
        for row in records:
            if(row[0]==uname):
                flag=1
                p=decrypt(row[1],row[2])
                if(p==pwd):
                    flag=2
                    break
        msg=""
        if(flag==2):
            return redirect(url_for("blog_info",token=uname))
        elif(flag==1):
            msg="INCORRECT  PASSWORD"
        else:
            msg="INCORRECT USERNAME/PASSWORD"
        flash(msg)
        return render_template("login.html")
    except:
        return redirect(url_for('handle_exception'))



@app.route("/update_content/<token>",methods=['GET','POST'])
def update_content(token):
    if request.method=='GET':
        cur=mysql.connection.cursor()
        cur.execute("SELECT USERNAME,EMAIL FROM login WHERE USERNAME='%s'" %(str(token),))
        records=cur.fetchone()
        return render_template("update_content.html",username=records[0],email=records[1])
    cur=mysql.connection.cursor()
    cur.execute("SELECT ID FROM post ORDER BY ID DESC LIMIT 1")
    records=cur.fetchone()
    if(records is None):
        id_post=1
    else:
        id_post=str(int(records[0])+1)
    category=request.form['category']
    title=request.form['title']
    content=content_morphe(request.form['content'])
    summarized_content=summarize(content)
    num_lines=str(len(content.split("."))-1)
    smry_num_lines=str(len(summarized_content.split("."))-1)
    num_words=str(len(content.split(" "))-1)
    smry_num_words=str(len(summarized_content.split(" "))-1)
    updated_by=str(token)
    today = date.today()
    updated_on=str(today.strftime("%y-%m-%d"))
    p=(len(summarized_content.split('.'))-1)
    l=len(summarized_content.split(" "))
    q=l%60
    if(q>0):
        num_min=str((l//60)+1)
    else:
        num_min=str(l//60)
    p=(len(content.split('.'))-1)
    l=len(content.split(" "))
    q=l%60
    if(q>0):
        actual_num_min=str((l//60)+1)
    else:
        actual_num_min=str(l//60)
    num_views=str(0)
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        p=file.filename
        lst=list(p.split("."))
        file_name=str(id_post)+"."+str(lst[-1])
        file.save(os.path.join(UPLOAD_FOLDER,file_name)) #app.config['UPLOAD_FOLDER']
    photo=str(file_name)
    cur.execute("SELECT * FROM categories")
    records=cur.fetchall()
    flag=0
    for row in records:
        if(row[0]==category):
            flag=1
            break
    if(flag==0):
        cur.execute("INSERT INTO categories VALUES('%s')" %(category,))
        mysql.connection.commit()
    cur.execute("INSERT INTO post VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(id_post,category,title,updated_by,updated_on,num_min,num_views,summarized_content,photo))
    mysql.connection.commit()
    #cur.execute("INSERT INTO analyze_details VALUES('%s','%s',%s','%s','%s','%s','%s','%s','%s')" %(id_post,title,content,num_lines,smry_num_lines,num_words,smry_num_words,actual_num_min,num_min))
    cur.execute("INSERT INTO analyze_details VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(id_post,title,content,num_lines,smry_num_lines,num_words,smry_num_words,actual_num_min,num_min))
    mysql.connection.commit()
    flash("Sucessfully updated!!")
    cur.execute("SELECT EMAIL FROM login WHERE USERNAME='%s'" %(str(token),))
    records=cur.fetchone()
    return render_template("update_content.html",username=token,email=records[0])
    #return str(id_post)+" "+title+" "+content+" "+num_lines+" "+smry_num_lines+" "+num_words+" "+smry_num_words+" "+actual_num_min+" "+num_min
        


@app.route("/reset",methods=['GET','POST'])
def reset():
    try:
        if request.method=='GET':
            return render_template("reset.html")
        email=request.form['email']
        cur=mysql.connection.cursor()
        cur.execute("SELECT EMAIL FROM login")
        records=cur.fetchall()
        flag=0
        for row in records:
            if(row[0]==email):
                flag=1
                break
        cur.close()
        if(flag==1):
            token = s.dumps(email, salt='email-confirm')
            msg=Message('Password Confirmation mail',sender='19hp5a1202.alit@apssdc.info',recipients=[email])
            msg.body = "Please complete reset process within an hour, rather token expires.\nYour link: "+"http://127.0.0.1:5000/reset_email/"+token
            mail.send(msg)
            flash("Please check your mail!!!!")
            return redirect(url_for('reset'))
        else:
            flash("Email-Id isnot Registered!!")
            return redirect(url_for('reset'))
    except:
        return redirect(url_for('handle_exception'))



@app.route('/reset_email/<token>',methods=['GET', 'POST'])
def reset_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
        if request.method=='GET':
            return render_template("reset_email.html",token=token)
        cur=mysql.connection.cursor()
        cur.execute("SELECT EID FROM login WHERE EMAIL=%s",(email,))
        record=cur.fetchone()
        new_pwd=request.form['pwd']
        enc=encrypt(new_pwd,record[0])
        val=""
        cur=mysql.connection.cursor()
        cur.execute("UPDATE login SET PASSWORD=%s WHERE EMAIL=%s",(enc,email))
        mysql.connection.commit()
        cur.close()
        flash("Password successfully updated!!!!!")
        return redirect(url_for('login'))
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'



@app.route("/profile_info/<token>",methods=['GET','POST'])
def profile_info(token):
    if request.method=='GET':
        cur=mysql.connection.cursor()
        cur.execute("SELECT USERNAME,EMAIL,CONTACT_NUMBER,CITY,STATE FROM login WHERE USERNAME='%s'" %(str(token),))
        record=cur.fetchone()
        return render_template("profile_info.html",username=record[0],email=record[1],contact_number=record[2],city=record[3],state=record[4],token=token)
    cur=mysql.connection.cursor()
    contact_number=request.form['contact_number']
    city=request.form['city']
    state=request.form['state']
    cur.execute("UPDATE login SET CONTACT_NUMBER='%s',CITY='%s',STATE='%s' WHERE USERNAME='%s'" %(str(contact_number),city,state,token))
    mysql.connection.commit()
    cur.close()
    flash("Personal info successfully updated!!")
    return redirect(url_for('profile_info',token=token))



@app.route("/blog_info/<token>",methods=['GET','POST'])
def blog_info(token):
    if request.method=='POST':
        title=request.form['title']
        cur=mysql.connection.cursor()
        cur.execute("DELETE FROM post WHERE TITLE='%s'" %(title,))
        mysql.connection.commit()
        cur.execute("DELETE FROM analyze_details WHERE TITLE='%s'" %(title,))
        mysql.connection.commit()
        cur.execute("SELECT TITLE FROM post WHERE UPDATED_BY='%s'" %(token,))
        records=cur.fetchall()
        lst=[]
        c=0
        for row in records:
            lst.append(row[0])
            c+=1
        cur=mysql.connection.cursor()
        cur.execute("SELECT EMAIL FROM login WHERE USERNAME='%s'" %(str(token),))
        records=cur.fetchone()
        return render_template("blog_info.html",lst=lst,num_posts=c,token=token,email=records[0])
    cur=mysql.connection.cursor()
    cur.execute("SELECT TITLE FROM post WHERE UPDATED_BY='%s'" %(token,))
    records=cur.fetchall()
    lst=[]
    c=0
    for row in records:
        lst.append(row[0])
        c+=1
    cur=mysql.connection.cursor()
    cur.execute("SELECT EMAIL FROM login WHERE USERNAME='%s'" %(str(token),))
    records=cur.fetchone()
    return render_template("blog_info.html",lst=lst,num_posts=c,token=token,email=records[0])



@app.route("/blog_info_edit/<token>",methods=['GET','POST'])
def blog_info_edit(token):
    if request.method=='GET':
        st=token.split('_')
        cur=mysql.connection.cursor()
        cur.execute("SELECT CATEGORY,TITLE,CONTENT,NUM_VIEWS,PHOTO,UPDATED_ON FROM post WHERE TITLE='%s'" %(st[1],))
        records=cur.fetchone()
        return render_template("blog_info_edit.html",token=st[0],category=records[0],title=records[1],content=records[2],num_views=records[3],photo=records[4],updated_on=records[5],token1=st[0]+'_'+records[1])
    st=token.split('_')
    cur=mysql.connection.cursor()
    cur.execute("SELECT ID,photo FROM post WHERE TITLE='%s'" %(st[1]))
    records=cur.fetchone()
    id_post=records[0]
    category=request.form['category']
    title=request.form['title']
    content=content_morphe(request.form['content'])
    summarized_content=summarize(content)
    num_lines=str(len(content.split("."))-1)
    smry_num_lines=str(len(summarized_content.split("."))-1)
    num_words=str(len(content.split(" "))-1)
    smry_num_words=str(len(summarized_content.split(" "))-1)
    today = date.today()
    updated_on=str(today.strftime("%y-%m-%d"))
    p=(len(summarized_content.split('.'))-1)
    l=len(summarized_content.split(" "))
    q=l%60
    if(q>0):
        num_min=str((l//60)+1)
    else:
        num_min=str(l//60)
    p=(len(content.split('.'))-1)
    l=len(content.split(" "))
    q=l%60
    if(q>0):
        actual_num_min=str((l//60)+1)
    else:
        actual_num_min=str(l//60)
    num_views=str(0)
    file = request.files['file']
    file_name=""
    if file:
        filename = secure_filename(file.filename)
        p=file.filename
        lst=list(p.split("."))
        file_name=str(id_post)+"."+str(lst[-1])
        file.save(os.path.join(UPLOAD_FOLDER,file_name)) #app.config['UPLOAD_FOLDER']
        photo=str(file_name)
    else:
        photo=str(records[1])
    cur.execute("SELECT * FROM categories")
    records=cur.fetchall()
    flag=0
    for row in records:
        if(row[0]==category):
            flag=1
            break
    if(flag==0):
        cur.execute("INSERT INTO categories VALUES('%s')" %(category,))
        mysql.connection.commit()
    cur.execute("UPDATE post SET CATEGORY='%s', TITLE='%s', UPDATED_ON='%s', NUM_MIN='%s', NUM_VIEWS='%s', CONTENT='%s',PHOTO='%s' WHERE ID='%s' " %(str(category),str(title),str(updated_on),str(num_min),str(num_views),str(summarized_content),str(photo),str(id_post)))
    mysql.connection.commit()
    cur.execute("UPDATE analyze_details SET TITLE='%s',ORIGINAL_CONTENT='%s', NUM_LINES_BEFORE='%s', NUM_LINES_AFTER='%s',NUM_WORDS_BEFORE='%s',NUM_WORDS_AFTER='%s',MIN_READ_BEFORE='%s',MIN_READ_AFTER='%s' WHERE ID='%s' " %(title,content,num_lines,smry_num_lines,num_words,smry_num_words,actual_num_min,num_min,id_post))
    mysql.connection.commit()
    flash("Sucessfully updated!!")
    return redirect(url_for('blog_info_edit',token=st[0]+"_"+title))



@app.route("/documentation")
def documentation():
    return render_template("documentation.html")



@app.route("/handle_exception")
def handle_exception():
    return render_template("handle_exception.html")



if __name__ == '__main__':
   app.run(debug = True)
