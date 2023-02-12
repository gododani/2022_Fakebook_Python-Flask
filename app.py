import json
import pathlib, os
from PIL import Image
from flask import Flask, render_template, request, session, redirect, url_for, flash
import cx_Oracle

#cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle_instant_client")

connection = 'dani/Asd123@localhost:1521/xe'
connectionStr = 'lengyel/Asd12345@localhost:1521/xe'
cnsStrEgyetemi = 'C##GG6K4U/C##GG6K4U@orania2:1521/orania2.inf.u-szeged.hu'

UPLOAD_PROFILE_IMAGE_FOLDER = str(pathlib.Path(__file__).parent.resolve()) + '\static\images\profile-images'
UPLOAD_GROUP_IMAGE_FOLDER = str(pathlib.Path(__file__).parent.resolve()) + '\static\images\group-images'
UPLOAD_ALBUM_IMAGE_FOLDER = str(pathlib.Path(__file__).parent.resolve()) + r'\static\images\album-images'
UPLOAD_USER_IMAGE_FOLDER = str(pathlib.Path(__file__).parent.resolve()) + r'\static\images\user-images'
#dsn_tns = cx_Oracle.makedsn('orania2', '1521', service_name='orania2.inf.u-szeged.hu') 

app = Flask(__name__)
app.secret_key = "super secret key"
# ----- HOME ----- #

@app.route('/')
@app.route('/home')
def home():
    if session.get('loggedin') == True:
        id = session['id']
        userData = user_data(id)
        userInfo = user_informations(id)
        userFriends = user_friends(id)
        userImages = get_user_images(id)
        userFriendRequests = friend_requests(id)
        userMessageRequests = message_requests(id)
        userGroups = get_user_groups(id)
        userAlbums = get_user_albums(id)
        uPersMess = user_personal_messages(id)
        uFeeds = user_feeds(id)
        print(userMessageRequests)
        print(uPersMess)
        # userDataJSON = convUDataToJSON(userData)
        i = 0
        if userMessageRequests is not None:
            for req in userMessageRequests:
                i = i + 1
        return render_template('home.html', uData=userData, uInfo=userInfo, uFriends=userFriends, uImages=userImages, uFriendRequests=userFriendRequests, uMessageRequests=userMessageRequests, messReqNumb=i, uGroups=userGroups, uAlbums=userAlbums, uPersonalMessages=uPersMess, feeds=uFeeds)
    else:
        return render_template('home.html')

def convUDataToJSON(userData):
    data = []
    i = 1
    for d in userData:
        data.append(i)
        data.append(d)
        i += 1
    return data

def user_feeds(id):
    conn = cx_Oracle.connect(connectionStr)
    cur = conn.cursor()
    d = user_friends(id)
    friend_ids = []
    res = None
    if d:
        for i in d:
            friend_ids.append(i[0])
        if friend_ids:
            sql = "SELECT * FROM profilok, feltoltott_kepek WHERE profilok.id = feltoltott_kepek.profil_id and profilok.id in ("
            j = 1
            for i in friend_ids:
                if friend_ids.__len__() != j:
                    sql += str(i) + ", "
                else:
                    sql += str(i) + ")"
                j = j + 1
            cur.execute(sql)
            res = cur.fetchall()
            cur.close()
    return res

def user_data(id):
    conn = cx_Oracle.connect(connectionStr)
    cur = conn.cursor()
    cur.execute("SELECT * FROM felhasznalok WHERE id = :id", (id,))
    res = cur.fetchone()
    cur.close()
    return res

def user_informations(id):
    conn = cx_Oracle.connect(connectionStr)
    cur = conn.cursor()
    cur.execute("SELECT id, felhasznalo_id, varos, vezeteknev, keresztnev, neme, to_char(szulnap,'YYYY-MM-DD') as szulnap, profil_kep, megye, iskola, munkahely, to_char(reg_datum,'YYYY-MM-DD') as reg_datum FROM profilok WHERE felhasznalo_id = :id", (id,))
    res = cur.fetchone()
    cur.close()
    return res

def user_friends(id):
    conn = cx_Oracle.connect(connectionStr)
    cur = conn.cursor()
    friend_ids = []
    cur.execute("SELECT ismerosok.fogado FROM ismerosok WHERE kuldo = :id and fuggoben = \'elfogadott\'", (id,))
    res1 = cur.fetchall()
    cur.execute("SELECT ismerosok.kuldo FROM ismerosok WHERE fogado = :id and fuggoben = \'elfogadott\'", (id,))
    res2 = cur.fetchall()
    i = 0
    for r1 in res1:
        friend_ids.append(r1[0])
        i = i + 1
    for r2 in res2:
        friend_ids.append(r2[0])
        i = i + 1
    sql = "SELECT * FROM profilok WHERE id in ("

    j = 1
    for i in friend_ids:
        if friend_ids.__len__() != j:
            sql += str(i) + ", "
        else:
            sql += str(i) + ")"
        j = j + 1
    res = None
    if friend_ids:
        cur.execute(sql)
        res = cur.fetchall()
        cur.close()
    return res

def user_personal_messages(id):
    conn = cx_Oracle.connect(connectionStr)
    cur = conn.cursor()
    friend_ids = []
    cur.execute("SELECT ismerosok.fogado FROM ismerosok WHERE kuldo = :id and fuggoben = \'elfogadott\'", (id,))
    res1 = cur.fetchall()
    cur.execute("SELECT ismerosok.kuldo FROM ismerosok WHERE fogado = :id and fuggoben = \'elfogadott\'", (id,))
    res2 = cur.fetchall()
    i = 0
    for r1 in res1:
        friend_ids.append(r1[0])
        i = i + 1
    for r2 in res2:
        friend_ids.append(r2[0])
        i = i + 1
    sql = "SELECT * FROM profilok WHERE id in ("
    
    j = 1
    for i in friend_ids:
        if friend_ids.__len__() != j:
            sql += str(i) + ", "
        else:
            sql += str(i) + ")"
        j = j + 1
    res = None
    if friend_ids:
        cur.execute(sql)
        res = cur.fetchall()
    
    dateDatas = dict(usid=id)
    for i in friend_ids:
        cur.execute("SELECT id, kuldo, fogado, mikor, olvasott, TO_DATE(mikor, 'YYYY-MM-DD') as mikor, uzenet FROM privat_uzenetek WHERE kuldo = :id and fogado = :i", (id, i))
        res2 = cur.fetchall()
        cur.execute("SELECT id, kuldo, fogado, mikor, olvasott, TO_DATE(mikor, 'YYYY-MM-DD') as mikor, uzenet FROM privat_uzenetek WHERE kuldo = :i and fogado = :id", (i, id))
        res3 = cur.fetchall()
        dates = []
        for x in res2:
            dates.append(x[3])
        for y in res3:
            dates.append(y[3])
        dates.sort(reverse = True)
        if dates:
            dateDatas[i] = dates[0]

    result = []
    for k in dateDatas:
        if k != "usid":
            da = dateDatas[k]
            d = dict(usid=id, key=k, ddate=da, key2=k, usid2=id, ddate2=da)
            cur.execute("""SELECT id, kuldo, fogado FROM privat_uzenetek WHERE (kuldo = :usid and fogado = :key and mikor = :ddate) or (kuldo = :key2 and fogado = :usid2 and mikor = :ddate2)""", d)
            res4 = cur.fetchall()
            result.append(res4)

    messages = []
    for r in result:
        if r[0][1] == session['id']:
            dat1 = dict(f=r[0][2], i=r[0][0])
            cur.execute("""SELECT profilok.id, profilok.vezeteknev, profilok.keresztnev, profilok.profil_kep, privat_uzenetek.* FROM profilok, privat_uzenetek WHERE profilok.id = privat_uzenetek.fogado AND fogado = :f and privat_uzenetek.id = :i""", dat1)
            actMess = cur.fetchall()
        else:
            dat2 = dict(k=r[0][1], i=r[0][0])
            cur.execute("""SELECT profilok.id, profilok.vezeteknev, profilok.keresztnev, profilok.profil_kep, privat_uzenetek.* FROM profilok, privat_uzenetek WHERE profilok.id = privat_uzenetek.kuldo AND kuldo = :k and privat_uzenetek.id = :i""", dat2)
            actMess = cur.fetchall()
        messages.append(actMess[0])
    conn.close()
    return messages

@app.route('/delete_friend', methods=['GET', 'POST'])
def delete_friend():
    if request.method == 'POST' and session.get('loggedin') == True:
        fId = request.form.get("friend-id")
        conn = cx_Oracle.connect(connectionStr)
        cur = conn.cursor()
        d1 = dict(id=session['id'], friend_id=fId)
        d2 = dict(friend_id=fId, id=session['id'])
        cur.execute("""DELETE FROM ismerosok WHERE kuldo = :id and fogado = :friend_id""", d1)
        cur.execute("""DELETE FROM ismerosok WHERE kuldo = :friend_id and fogado = :id""", d2)
        conn.commit()
        cur.close()
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/delete_user_image', methods=['GET', 'POST'])
def delete_user_image():
    if request.method == 'POST' and session.get('loggedin') == True:
        imageId = request.form.get("user-image-id")
        data = dict(imId=imageId)
        conn = cx_Oracle.connect(connectionStr)
        cur = conn.cursor()
        cur.execute("""SELECT kep_nev FROM feltoltott_kepek WHERE id = :imId""", data)
        filename = cur.fetchone()[0]
        cur.execute("""DELETE FROM feltoltott_kepek WHERE id=:imId""", data)
        conn.commit()
        cur.close()
        delete_image(UPLOAD_USER_IMAGE_FOLDER, filename)
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/saveUserInfos', methods=['GET', 'POST'])
def saveUserInfos():
    if request.method == 'POST' and session.get('loggedin') == True:
        id = session['id']
        fname = request.form.get('first-name')
        lname = request.form.get('last-name')
        gender = request.form.get('gender')
        szulDate = request.form.get('birthday')
        profileImage = request.files['profileImage']
        state = request.form.get('state')
        city = request.form.get('city')
        school = request.form.get('school')
        workplace = request.form.get('workplace')
        if not profileImage:
            conn = cx_Oracle.connect(connectionStr)
            cur = conn.cursor()
            profile = dict(cy=city, firstName=fname, lastName=lname, gend=gender, szuletesDatum=szulDate, st=state, sch=school, workp=workplace, profileId=id)
            cur.execute("""UPDATE profilok SET varos=:cy, vezeteknev=:firstName, keresztnev=:lastName, neme=:gend, szulnap=TO_DATE(:szuletesDatum, 'YYYY-MM-DD'), megye=:st, iskola=:sch, munkahely=:workp WHERE felhasznalo_id=:profileId""", profile)
            conn.commit()
            cur.close()
            session['keresztnev'] = lname
            session['vezeteknev'] = fname
        else:
            app.config['UPLOAD_FOLDER'] = UPLOAD_PROFILE_IMAGE_FOLDER
            delete_image(UPLOAD_PROFILE_IMAGE_FOLDER, session['profile-image'])
            kiterj = profileImage.filename.split('.')[1]
            filename = "profile-" + str(id) + "." + str(kiterj)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            profileImage.save(path)
            conn = cx_Oracle.connect(connectionStr)
            cur = conn.cursor()
            profile = dict(cy=city, firstName=fname, lastName=lname, gend=gender, szuletesDatum=szulDate, profKep=filename, st=state, sch=school, workp=workplace, profileId=id)
            cur.execute("""UPDATE profilok SET varos=:cy, vezeteknev=:firstName, keresztnev=:lastName, neme=:gend, szulnap=TO_DATE(:szuletesDatum, 'YYYY-MM-DD'), profil_kep=:profKep, megye=:st, iskola=:sch, munkahely=:workp WHERE felhasznalo_id=:profileId""", profile)
            conn.commit()
            cur.close()
            session['profile-image'] = filename
            session['keresztnev'] = lname
            session['vezeteknev'] = fname
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST' and session.get('loggedin') == True:
        id = session['id']
        userImage = request.files['add-image-logo']
        imageTitle = request.form.get('add-image-title')
        if userImage:
            conn = cx_Oracle.connect(connectionStr)
            cur = conn.cursor()
            cur.execute("SELECT id FROM (SELECT id FROM feltoltott_kepek ORDER BY id desc) WHERE ROWNUM = 1")
            lastId = cur.fetchone()
            app.config['UPLOAD_FOLDER'] = UPLOAD_USER_IMAGE_FOLDER
            kiterj = userImage.filename.split('.')[1]
            if lastId is None:
                lastId = 0
                filename = "userImage-" + str(id) + "-" + str(lastId + 1) + "." + str(kiterj)
            else:
                filename = "userImage-" + str(id) + "-" + str(lastId[0] + 1) + "." + str(kiterj)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            userImage.save(path)
            image_file = Image.open(userImage)
            imageSize = len(image_file.fp.read())
            data = dict(usid=id, kepNev=filename, kepCim=imageTitle, storageReserved=imageSize)
            cur.execute("""INSERT INTO feltoltott_kepek (id, profil_id, kep_nev, mikor, kep_leiras, foglalt_tarhely) VALUES((null), :usid, :kepNev, SYSDATE, :kepCim, :storageReserved)""", data)
            conn.commit()
            conn.close()
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return redirect(url_for('home'))

def delete_image(path, filename):
    if os.path.exists(path + '/' + filename) is True and filename != "default-profile-image.png":
        os.remove(path + '/' + filename)

def friend_requests(id):
    if session.get('loggedin') == True:
        conn = cx_Oracle.connect(connectionStr)
        cur = conn.cursor()
        cur.execute("SELECT kuldo FROM ismerosok WHERE fogado = :id and fuggoben = \'függőben\'", (id,))
        friend_ids = cur.fetchall()
        sql = "SELECT * FROM profilok WHERE id in ("
        j = 1
        for i in friend_ids:
            if friend_ids.__len__() != j:
                sql += str(i[0]) + ", "
            else:
                sql += str(i[0]) + ")"
            j = j + 1
        res = None
        if friend_ids:
            cur.execute(sql)
            res = cur.fetchall()
        cur.close()
    return res

def message_requests(id):
    if session.get('loggedin') == True:
        conn = cx_Oracle.connect(connectionStr)
        cur = conn.cursor()
        data = dict(usid=id, fugg="függőben")
        cur.execute("SELECT kuldo FROM engedelyek WHERE fogado = :usid and elfogadott = :fugg", data)
        friend_ids = cur.fetchall()
        sql = "SELECT * FROM profilok WHERE id in ("
        j = 1
        for i in friend_ids:
            if friend_ids.__len__() != j:
                sql += str(i[0]) + ", "
            else:
                sql += str(i[0]) + ")"
            j = j + 1
        res = None
        if friend_ids:
            cur.execute(sql)
            res = cur.fetchall()
        cur.close()
    return res

@app.route('/acc_decl_fr_req', methods=['GET', 'POST'])
def acc_decl_fr_req():
    if request.method == 'POST' and session.get('loggedin') == True:
        fId = request.form.get('id')
        data = dict(friend_id=fId, user_id=session['id'])
        conn = cx_Oracle.connect(connectionStr)
        cur = conn.cursor()
        if request.form.get('decline') is None and request.form.get('accept'):
            cur.execute("UPDATE ismerosok SET fuggoben=\'elfogadott\' WHERE kuldo=:friend_id and fogado=:user_id", data)
        elif request.form.get('decline'):    
            cur.execute("""DELETE FROM ismerosok WHERE kuldo = :friend_id and fogado = :user_id and fuggoben = \'függőben\'""", data)
        conn.commit()
        cur.close()
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/acc_decl_mess_req', methods=['GET', 'POST'])
def acc_decl_mess_req():
    if request.method == 'POST' and session.get('loggedin') == True:
            fId = request.form.get('id')
            data = dict(friend_id=fId, user_id=session['id'])
            conn = cx_Oracle.connect(connectionStr)
            cur = conn.cursor()
            if request.form.get('decline') is None and request.form.get('accept'):
                cur.execute("UPDATE engedelyek SET elfogadott=\'elfogadott\' WHERE kuldo=:friend_id and fogado=:user_id", data)
            elif request.form.get('decline'):    
                cur.execute("""DELETE FROM engedelyek WHERE kuldo = :friend_id and fogado = :user_id and elfogadott = \'függőben\'""", data)
            conn.commit()
            cur.close()
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return redirect(url_for('home'))

def get_user_groups(id):
    conn = cx_Oracle.connect(connectionStr)
    cur = conn.cursor()
    cur.execute("SELECT csoportok.* FROM csoportok, csoport_tagok WHERE csoportok.id = csoport_tagok.csoport_id and profil_id = :id", (id,))
    res = cur.fetchall()
    cur.close()
    return res

def get_user_albums(id):
    conn = cx_Oracle.connect(connectionStr)
    cur = conn.cursor()
    cur.execute("SELECT albumok.* FROM albumok WHERE profil_id = :id", (id,))
    res = cur.fetchall()
    cur.close()
    return res

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
            username = request.form.get('register-username')
            email = request.form.get('register-email')
            pwd = request.form.get('register-password')
            repwd = request.form.get('register-rePassword')
            fname = request.form.get('first-name')
            lname = request.form.get('last-name')
            gender = request.form.get('gender')
            szulDate = request.form.get('szul-date')
            state = request.form.get('state')
            city = request.form.get('city')
            school = request.form.get('school')
            workplace = request.form.get('workplace')
            
            unique = usrn_or_email_exists(username, email)
            if not unique:
                if pwd == repwd and pwd != '' and fname != '' and lname != '' and gender != '' and szulDate != '' and state != '' and city != '' and school != '' and workplace != '' :
                    conn = cx_Oracle.connect(connectionStr)
                    cur = conn.cursor()
                    user = dict(usrn=username, em=email, p=pwd)
                    profile = dict(cy=city, firstName=fname, lastName=lname, gend=gender,
                    szuletesDatum=szulDate, profKep="default-profile-image.png", st=state, sch=school, workp=workplace)
                    cur.execute("""INSERT INTO felhasznalok (id, felhasznalo_nev, email, jelszo) VALUES((null), :usrn, :em, :p)""", user)
                    cur.execute("""INSERT INTO profilok (id, felhasznalo_id, varos, vezeteknev, keresztnev, neme, szulnap, profil_kep, megye, iskola, munkahely, reg_datum) VALUES((null), (null), :cy, :firstName, :lastName, :gend, TO_DATE(:szuletesDatum,'YYYY-MM-DD'), :profKep, :st, :sch, :workp, SYSDATE)""", profile)
                    conn.commit()
                    cur.close()
                else:
                    flash('A két jelszó nem egyezik meg!')
            else:
                flash('A felhasználónév vagy az email már foglalt!')

    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return redirect(url_for('home'))

def get_user_images(id):
    conn = cx_Oracle.connect(connectionStr)
    cur = conn.cursor()
    cur.execute("SELECT feltoltott_kepek.* FROM feltoltott_kepek, profilok WHERE feltoltott_kepek.profil_id = profilok.id and feltoltott_kepek.profil_id = :id", (id,))
    res = cur.fetchall()
    cur.close()
    return res

@app.route('/modifyuser', methods=['GET', 'POST'])
def modifyuser():
    if session.get('loggedin') == True and request.method == 'POST':
        uid = session['id']
        username = request.form.get('username')
        email = request.form.get('email')
        pwd = request.form.get('password')
        repwd = request.form.get('re-password')
        
        unique = usrn_or_email_exists(username, email, uid)
        if not unique:
            if pwd == repwd and pwd != '':
                conn = cx_Oracle.connect(connectionStr)
                cur = conn.cursor()
                data = dict(usrn=username, email=email, password=pwd, id=uid)
                cur.execute("UPDATE felhasznalok SET felhasznalo_nev=:usrn, email=:email, jelszo=:password WHERE id=:id", data)
                conn.commit()
                cur.close()
            else:
                flash('A két jelszó nem egyezik meg!')
        else:
            flash('A felhasználónév vagy az email már foglalt!')

    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return redirect(url_for('home'))

def usrn_or_email_exists(username, email, uid=-100):
    conn = cx_Oracle.connect(connectionStr)
    cur = conn.cursor()
    ell = dict(usrn=username, em=email, id=uid)
    cur.execute("SELECT * FROM felhasznalok WHERE (felhasznalo_nev = :usrn or email = :em) and id != :id", ell)
    unique = cur.fetchall()
    cur.close()
    return unique

@app.route('/add_friend', methods=['GET', 'POST'])
def add_friend():
    if session.get('loggedin') == True and request.method == 'POST':
        id = session['id']
        friendUsername = request.form.get('add-friend-username')
        conn = cx_Oracle.connect(connectionStr)
        cur = conn.cursor()
        data = dict(friends_usrn=friendUsername)
        cur.execute("""SELECT profilok.id FROM felhasznalok, profilok WHERE felhasznalok.id = profilok.felhasznalo_id and felhasznalo_nev = :friends_usrn""", data)
        user_exists = cur.fetchone()
        if(user_exists):
            friend_id = user_exists[0]
            data2 = dict(usid=id, frid=friend_id, frid2=friend_id, usid2=id)
            cur.execute("""SELECT * FROM ismerosok WHERE (kuldo = :usid and fogado = :frid) or (kuldo = :frid2 and fogado = :usid2)""", data2)
            conn_alr_exists = cur.fetchall()
            if(not conn_alr_exists):
                data3 = dict(kuldo=id, fogado=friend_id)
                cur.execute("""INSERT INTO ismerosok (id, kuldo, fogado, fuggoben) VALUES((null), :kuldo, :fogado, \'függőben\')""", data3)
                conn.commit()
            else:
                flash('Létezik már a baráti kapcsolat a két fél között!')
        else:
            flash('A felhasználó nem létezik!')
        conn.close()
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/create_group', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST' and session.get('loggedin') == True:
        id = session['id']
        groupIndexImage = request.files['group-logo']
        groupTitle = request.form.get('create-group-name')
        groupDesc = request.form.get('create-group-description')
        if groupIndexImage:
            conn = cx_Oracle.connect(connectionStr)
            cur = conn.cursor()
            cur.execute("SELECT id FROM (SELECT id FROM csoportok ORDER BY id desc) WHERE ROWNUM = 1")
            lastId = cur.fetchone()
            app.config['UPLOAD_FOLDER'] = UPLOAD_GROUP_IMAGE_FOLDER
            kiterj = groupIndexImage.filename.split('.')[1]
            if lastId is None:
                lastId = 0
                filename = "groupImage-" + str(id) + "-" + str(lastId + 1) + "." + str(kiterj)
            else:
                filename = "groupImage-" + str(id) + "-" + str(lastId[0] + 1) + "." + str(kiterj)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            groupIndexImage.save(path)
            data = dict(groupCim=groupTitle, groupDescription=groupDesc, kepNev=filename, usid=id)
            cur.execute("ALTER TRIGGER csoport_tagok_trig ENABLE")
            conn.commit()
            cur.execute("ALTER TRIGGER csoport_tagok_trig2 DISABLE")
            conn.commit()
            cur.execute("""INSERT INTO csoportok (id, csoport_nev, leiras, index_kep, alapitas_datum, tulaj) VALUES((null), :groupCim, :groupDescription, :kepNev, SYSDATE, :usid)""", data)
            conn.commit()
            data2 = dict(usid=id)
            cur.execute("""INSERT INTO csoport_tagok (id, profil_id, csoport_id, szerep, elfogadott, miota) VALUES((null), :usid, (null), \'Admin\', 1, SYSDATE)""", data2)
            conn.commit()
            cur.execute("ALTER TRIGGER csoport_tagok_trig DISABLE")
            conn.commit()
            cur.execute("ALTER TRIGGER csoport_tagok_trig2 ENABLE")
            conn.commit()
            conn.close()
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/create_album', methods=['GET', 'POST'])
def create_album():
    if request.method == 'POST' and session.get('loggedin') == True:
        id = session['id']
        albumIndexImage = request.files['album-logo']
        albumTitle = request.form.get('create-album-name')
        if albumIndexImage:
            conn = cx_Oracle.connect(connectionStr)
            cur = conn.cursor()
            cur.execute("SELECT id FROM (SELECT id FROM albumok ORDER BY id desc) WHERE ROWNUM = 1")
            lastId = cur.fetchone()
            app.config['UPLOAD_FOLDER'] = UPLOAD_ALBUM_IMAGE_FOLDER
            kiterj = albumIndexImage.filename.split('.')[1]
            if lastId is None:
                lastId = 0
                filename = "albumImage-" + str(id) + "-" + str(lastId + 1) + "." + str(kiterj)
            else:
                filename = "albumImage-" + str(id) + "-" + str(lastId[0] + 1) + "." + str(kiterj)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            albumIndexImage.save(path)
            data = dict(usid=id, albumCim=albumTitle, kepNev=filename)
            cur.execute("""INSERT INTO albumok (id, profil_id, cim, letrehozva, index_kep) VALUES((null), :usid, :albumCim, SYSDATE, :kepNev)""", data)
            conn.commit()
            conn.close()
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/leave_group', methods=['GET', 'POST'])
def leave_group():
    if request.method == 'POST' and session.get('loggedin') == True:
        gId = request.form.get("group-id")
        uId = session['id']
        conn = cx_Oracle.connect(connectionStr)
        cur = conn.cursor()
        data = dict(usid=uId, groupId=gId)
        cur.execute("""SELECT szerep FROM csoport_tagok, csoportok WHERE csoportok.id = csoport_tagok.csoport_id AND profil_id = :usid AND csoport_id = :groupId""", data)
        res = cur.fetchone()[0]
        if res == 'Admin':
            cur.execute("""DELETE FROM csoport_tagok WHERE profil_id = :usid AND csoport_id = :groupId""", data)
            data2 = dict(groupId=gId)
            cur.execute("""SELECT index_kep FROM csoportok WHERE id = :groupId""", data2)
            filename = cur.fetchone()[0]
            cur.execute("""DELETE FROM csoportok WHERE id = :groupId""", data2)
            conn.commit()
            cur.close()
            delete_image(UPLOAD_GROUP_IMAGE_FOLDER, filename)
        else:
            cur.execute("""DELETE FROM csoport_tagok WHERE profil_id = :usid AND csoport_id = :groupId""", data)
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/delete_user_album', methods=['GET', 'POST'])
def delete_user_album():
    if request.method == 'POST' and session.get('loggedin') == True:
        aId = request.form.get("album-id")
        conn = cx_Oracle.connect(connectionStr)
        cur = conn.cursor()
        data = dict(albId=aId)
        cur.execute("""SELECT index_kep FROM albumok WHERE id = :albId""", data)
        filename = cur.fetchone()[0]
        cur.execute("""DELETE FROM albumok WHERE id = :albId""", data)
        conn.commit()
        cur.close()
        delete_image(UPLOAD_ALBUM_IMAGE_FOLDER, filename)
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return redirect(url_for('home'))

# ----- LOGIN ----- #

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usrn = request.form.get('login-username')
        pwd = request.form.get('login-password')
        conn = cx_Oracle.connect(connectionStr)
        cur = conn.cursor()
        # pontosvesszővel nem szabad lezárni mert hibát dob
        # ha szeretnénk feltételt kötni stringhez, akkor a keresett stringet sima '-ba kell tenni, "-ra hibát dob
        # sql = "SELECT id FROM felhasznalok WHERE felhasznalo_nev = \'" + usrn + "\' AND felhasznalok.jelszo = \'" + pwd + "\'"
        data = dict(username=usrn, password=pwd)
        cur.execute("""
                SELECT felhasznalok.id, profilok.keresztnev, profilok.vezeteknev, profilok.profil_kep FROM felhasznalok, profilok WHERE felhasznalok.id = profilok.felhasznalo_id and felhasznalo_nev = :username AND felhasznalok.jelszo = :password""", data)
        res = cur.fetchall()
        if res:
            session['loggedin'] = True
            session['id'] = res[0][0]
            session['profile-image'] = res[0][3]
            session['keresztnev'] = res[0][1]
            session['vezeteknev'] = res[0][2]
            flash('Belépés sikeres', category="success")
            return redirect(url_for('home'))
        else:
            flash('Belépés sikertelen', category="error")
        cur.close()
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return redirect(url_for('home'))

# ----- LOGOUT ----- #
@app.route('/logout')
def logout():
     session.pop('loggedin', None)
     session.pop('id', None)
     flash('Kilépés sikeres', category="success")
     return render_template("home.html")

# ----- MODIFY IMAGE ----- #
@app.route('/modify_image_modal', methods=['GET', 'POST'])
def modify_image_modal():
    if request.method == 'POST' and session.get('loggedin') == True:
        imageId = request.form.get("mod-user-image-id")
        data = dict(imId=imageId)
        conn = cx_Oracle.connect(connectionStr)
        cur = conn.cursor()
        cur.execute("""SELECT * FROM feltoltott_kepek WHERE id = :imId""", data)
        im = cur.fetchone()
        cur.close()
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return render_template("image_modify.html", image=im)

@app.route('/modify-image', methods=['GET', 'POST'])
def modify_image():
    if request.method == 'POST' and session.get('loggedin') == True:
        imageId = request.form.get("mod-image-butt")
        kepTitle = request.form.get("image-modify-title")
        data = dict(imageTitle=kepTitle, imId=imageId)
        conn = cx_Oracle.connect(connectionStr)
        cur = conn.cursor()
        cur.execute("""UPDATE feltoltott_kepek SET kep_leiras = :imageTitle WHERE id = :imId""", data)
        conn.commit()
        cur.close()
        flash("A kép címének módosítása sikeres!")
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return redirect(url_for('home'))

# ----- MODIFY ALBUM ----- #
@app.route('/modify_album_modal', methods=['GET', 'POST'])
def modify_album_modal():
    if request.method == 'POST' and session.get('loggedin') == True:
        albumId = request.form.get("mod-album-id")
        data = dict(alId=albumId)
        conn = cx_Oracle.connect(connectionStr)
        cur = conn.cursor()
        cur.execute("""SELECT * FROM albumok WHERE id = :alId""", data)
        al = cur.fetchone()
        cur.execute("""SELECT album_kepek.id, feltoltott_kepek.kep_nev, feltoltott_kepek.kep_leiras FROM album_kepek, feltoltott_kepek WHERE album_kepek.kep_id = feltoltott_kepek.id and album_id = :alId""", data)
        images = cur.fetchall()
        cur.close()
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return render_template("album_modify.html", album=al, albumImages=images)

@app.route('/delete_image_from_album', methods=['GET', 'POST'])
def delete_image_from_album():
    if request.method == 'POST' and session.get('loggedin') == True:
        albImageId = request.form.get("album-image-delete-id")
        data = dict(aImId=albImageId)
        conn = cx_Oracle.connect(connectionStr)
        cur = conn.cursor()
        cur.execute("""DELETE FROM album_kepek WHERE id = :aImId""", data)
        conn.commit()
        cur.close()
        flash("A kép törlése sikerült az albumból!")
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/add_image_to_album', methods=['GET', 'POST'])
def add_image_to_album():
    if request.method == 'POST' and session.get('loggedin') == True:
        imTitle = request.form.get("add-photo-title")
        alId = request.form.get("album-id")
        conn = cx_Oracle.connect(connectionStr)
        cur = conn.cursor()
        id = session['id']
        cur.execute("SELECT feltoltott_kepek.id FROM feltoltott_kepek WHERE feltoltott_kepek.kep_leiras = :imTitle and feltoltott_kepek.profil_id = :id", (imTitle, id))
        res = cur.fetchone()
        if res:
            imId = res[0]
            data = dict(imageId=imId, albumId=alId)
            cur.execute("""INSERT INTO album_kepek (id, kep_id, album_id) VALUES((null), :imageId, :albumId)""", data)
            conn.commit()
            flash("A kép hozzáadása az albumhoz sikeres!")
        else:
            flash("Nem létezik ilyen kép ezzel a címmel!")
        cur.close()
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return redirect(url_for('home'))

# ----- MODIFY GROUP ----- #
@app.route('/modify-group', methods=['GET', 'POST'])
def modify_group():
    if request.method == 'POST' and session.get('loggedin') == True:
        groupId = request.form.get("mod-group-id")
        data = dict(grId=groupId)
        conn = cx_Oracle.connect(connectionStr)
        cur = conn.cursor()
        cur.execute("""SELECT * FROM csoportok WHERE id = :grId""", data)
        gr = cur.fetchone()
        data2 = dict(grId=groupId, usid=session['id'])
        cur.execute("""SELECT szerep FROM csoport_tagok WHERE csoport_id = :grId and profil_id = :usid""", data2)
        r = cur.fetchone()
        if r:
            ro = r[0]
        else:
            ro = ""
        cur.execute("SELECT profilok.*, csoport_tagok.id FROM csoport_tagok, profilok WHERE profilok.id = csoport_tagok.profil_id and szerep != \'Admin\' and csoport_tagok.csoport_id = :groupId", (groupId,))
        grMemb = cur.fetchall()
        cur.close()
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return render_template("group_modify.html", group=gr, role=ro, groupMembers=grMemb)

@app.route('/add_user_to_group', methods=['GET', 'POST'])
def add_user_to_group():
    if request.method == 'POST' and session.get('loggedin') == True:
        uName = request.form.get("add-group-username")
        grId = request.form.get("add-group-id")
        conn = cx_Oracle.connect(connectionStr)
        cur = conn.cursor()
        cur.execute("ALTER TRIGGER csoport_tagok_trig DISABLE")
        conn.commit()
        cur.execute("SELECT profilok.id FROM profilok, felhasznalok WHERE profilok.felhasznalo_id = felhasznalok.id and felhasznalok.felhasznalo_nev = :uName", (uName,))
        res = cur.fetchone()
        if res:
            profId = res[0]
            data = dict(profilId=profId, groupId=grId)
            cur.execute("""INSERT INTO csoport_tagok (id, profil_id, csoport_id, szerep, elfogadott, miota) VALUES((null), :profilId, :groupId, \'Tag\', 1, SYSDATE)""", data)
            conn.commit()
        else:
            flash('A megadott felhasználónév nem létezik!', category="error")
        cur.close()    
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/delete_member_from_group', methods=['GET', 'POST'])
def delete_member_from_group():
    if request.method == 'POST' and session.get('loggedin') == True:
        membId = request.form.get("delete-member-id")
        conn = cx_Oracle.connect(connectionStr)
        cur = conn.cursor()
        cur.execute("DELETE FROM csoport_tagok WHERE id = :membId", (membId,))
        conn.commit()
        cur.close()
        flash("A tag törlése sikerült!")
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return redirect(url_for('home'))   

@app.route('/group_infos_modify', methods=['GET', 'POST'])
def group_infos_modify():
    if request.method == 'POST' and session.get('loggedin') == True:
        id = session['id']
        grId = request.form.get("modify-group-id")
        grIm = request.files["group-modify-image-file"]
        grDesc = request.form.get("group-modify-desc")
        conn = cx_Oracle.connect(connectionStr)
        cur = conn.cursor()
        if not grIm:
            data = dict(description=grDesc, groupId=grId)
            cur.execute("""UPDATE csoportok SET leiras = :description WHERE id = :groupId""", data)
            conn.commit()
            cur.close()
            flash("A tag törlése sikerült!")
        else:
            app.config['UPLOAD_FOLDER'] = UPLOAD_GROUP_IMAGE_FOLDER
            cur.execute("SELECT csoportok.index_kep FROM csoportok WHERE id = :grId", (grId,))
            oldGroupImage = cur.fetchone()[0]
            delete_image(UPLOAD_GROUP_IMAGE_FOLDER, oldGroupImage)
            kiterj = grIm.filename.split('.')[1]
            filename = "groupImage-" + str(id) + "-" + str(grId) + "." + str(kiterj)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            grIm.save(path)
            data2 = dict(description=grDesc, groupImage=filename, groupId=grId)
            cur.execute("""UPDATE csoportok SET leiras = :description, index_kep = :groupImage WHERE id = :groupId""", data2)
            conn.commit()
            cur.close()
    else:
        flash('Nincs megfelelő jogosultsága az oldal eléréséhez!', category="error")
        return redirect(url_for('home'))
    return redirect(url_for('home'))

# ----- CHAT ----- #
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template("chat.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
