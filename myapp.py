from flask import Flask, render_template ,request, session, redirect, url_for
import os
import psycopg2
import base64
app = Flask(__name__)

app.secret_key = os.urandom(32)

# sql接続用
def getConnection():
    return psycopg2.connect(
        host='localhost',
        dbname='s1922074',
        user='s1922074',
        password='CldmLp3i',
        # charset='utf8',
        # cursorclass=pymysql.cursors.DictCursor
    )

connection = getConnection()
sql = "SELECT * FROM get_64"
cursor = connection.cursor()
cursor.execute(sql)
list_64 = cursor.fetchall()
# print(list_64[0][1])

# ワクチン関係のやつ
vaccine_dict = {
    1:["混合ワクチン2種",list_64[0][1],"　二種混合（ジフテリア破傷風混合トキソイド、DT）ワクチンはジフテリアと破傷風の発症を予防するのが目的です。<br>　ジフテリアと破傷風の第1期の予防接種として四種混合（DPT-IPV）ワクチンまたは三種混合（DPT）ワクチンを接種した人に第2期の予防接種として1回接種します。<br>　第1期の予防注射は1歳時に接種しますが、最後に接種してから10年程度で効果が弱まるため、このDTワクチンは11歳時に接種することが望ましいとされています。"],
    2:["混合ワクチン3種",list_64[1][1],"　三種混合（DPT）ワクチンはジフテリア、百日咳、そして破傷風の発症を予防します。<br>　この3つに加えてポリオも同時に予防する四種混合（DPT-IPV）ワクチンは、現在定期接種となっています。追加接種まで全て接種すれば、いずれの種類のワクチンを用いても抗体獲得率（免疫を持つことに成功する確率）は100%とされています。ただし、最後に接種してから百日咳に対する予防効果は4年から10年程度で減弱するため、百日咳に対する免疫を維持するためには就学前や10代での三種混合ワクチンの追加接種をお勧めします。"],
    3:["混合ワクチン4種",list_64[2][1],"　ジフテリア、百日咳、破傷風、そしてポリオの発症を予防するのが主な効果です。追加接種まで全て接種すれば、いずれの種類のワクチンを用いても抗体獲得率（免疫を持つことに成功する確率）は100%とされています。ただし、ジフテリア、百日咳、破傷風については最後に接種してから10年程度で効果は減弱するので、免疫効果を維持する場合は追加接種（DPTワクチン、DTワクチン、破傷風トキソイドなど）が望ましいです。<br>　また、ポリオに関する免疫効果は、不活化ポリオワクチンのみの場合（DPT-IPVワクチン）は、数年で落ちる可能性があるため、就学前（4-6歳）の不活化ポリオ（単独）ワクチンの追加接種が現在厚生労働省で検討されています）。"],
    4:["混合ワクチン5種",list_64[3][1],"　感染すると生命に危険を及ぼす可能性のあるパルボウイルス、アデノウイルス、ジステンパーウイルスの感染予防とケンネルコフと呼ばれるカゼに似た症状をもたらすウイルス2種の予防を行なえるワクチンです。 パルボ、アデノ、ジステンパーの予防は重要視されていることから、コアワクチン（核となるワクチン）と呼ばれています。このワクチンは一般的に持続性に優れています。"],
    5:["混合ワクチン6種",list_64[4][1],"　5種と6種の違いはコロナウイルスの感染予防の有り無しです。コロナウイルスはパルボウイルスと一緒に感染すると重い腸炎をもたらしますが、パルボウイルスさえ予防できていれば、特に問題にならないため、5種と6種のワクチンは病気の予防の点では大差はありません。"],
    6:["混合ワクチン7種",list_64[5][1],"　5種ワクチンに加えて、レプトスピラが加わったものです。レプトスピラは不活化ワクチンという持続性の短いワクチンのため、定期的な追加接種（毎年）が必要です。"],
    7:["混合ワクチン8,9種",list_64[6][1],"　7種～9種の違いですが、レプトスピラの亜種（枝分かれした種）の数の違いになります。レプトスピラの予防という点では大差はありません。<br>　レプトスピラとは日本各地で発生はありますが、かなり稀な病気です。犬が発生した場合、感染犬の腎臓にレプトスピラを保有し、尿から排出します。ヒトにも感染する可能性はあります。症状はウイルスの型によって、黄疸や出血がみられ、最終的には激しい腎不全の症状から死亡することもあります。レプトスピラは尿から感染を起こすことから、他の犬の尿をよく舐めるクセがある犬は要注意です。"]
}
short_txt_dict = {}
for i in vaccine_dict:
    txt_ = vaccine_dict[i][2][0:50].replace('<br>','') + "..."
    short_txt_dict[i] = txt_
# print(short_txt_dict)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route("/", methods=['GET','POST'])
def Login():

    if "login_name" in session and "login_pass" in session:
        session.pop('login_name', None)
        session.pop('login_pass', None)

    err_message = ""

    if("new_name" in request.form):
        if("new_pass" in request.form):
            try:
                new_name = request.form["new_name"]
                new_pass = request.form["new_pass"]

                connection = getConnection()
                sql = "insert into login values ('" + str(new_name) + "','" + str(new_pass) + "')"
                cursor = connection.cursor()
                cursor.execute(sql)
                connection.commit()

                connection = getConnection()
                sql = "insert into status_table_2 values ('"+ str(new_name) + "','non','non','non','non','non','non','non','non','non','non','non','non','non','non')"
                # sql += n_
                # print(sql)
                cursor = connection.cursor()
                cursor.execute(sql)
                connection.commit()

                connection = getConnection()
                sql = "insert into send_evi_2 values ('"+ str(new_name) + "','non','non','non','non','non','non','non','non','non','non','non','non')"
                cursor = connection.cursor()
                cursor.execute(sql)
                connection.commit()
            except:
                err_message = "ユーザ名が重複しています"
    return render_template("login.html",err_message=err_message)

@app.route("/new_account")
def new_account():
    return render_template("new_account.html")

@app.route("/index", methods=['GET','POST'])
def index():
    # ログイン関係
    connection = getConnection()
    sql = "SELECT * FROM login"
    cursor = connection.cursor()
    cursor.execute(sql)
    login_list = cursor.fetchall()

    login_dict = {}
    for i in login_list:
        login_dict[i[0]] = i[1]
    # print("login_dict\n",login_dict)
    if "login_name" not in session:
        session["login_name"] = request.form["login_name"]
        session["login_pass"] = request.form["login_pass"]
        login_name = session["login_name"]
        login_pass = session["login_pass"]
    else:
        login_name = session["login_name"]
        login_pass = session["login_pass"]
    print(login_name,login_pass)

    if login_name in list(login_dict.keys()):
        if login_pass == login_dict[login_name]:
            return render_template("index.html",vaccine_dict=vaccine_dict,short_txt_dict=short_txt_dict)
        else:
            return redirect(url_for('Login'))
    else:
        return redirect(url_for('Login'))

@app.route('/detail/<string:vaccine_id>')
def detail(vaccine_id):
    list_ = vaccine_dict[int(vaccine_id)]
    return render_template("show_detail.html",vaccine_id=vaccine_id,list_=list_)

@app.route('/status')
def status():
    login_name = session["login_name"]

    connection = getConnection()
    sql = "SELECT * FROM status_table_2 where name = '" + str(login_name) +"'"
    cursor = connection.cursor()
    cursor.execute(sql)
    status_list = cursor.fetchall()[0]

    fin_list = []
    fin_date_list = []
    yet_list = []
    count_list = [1,3,5,7,9,11,13]
    count = 0
    for i in list(range(1,8)):
        if not status_list[count_list[count]] == "non":
            fin_list.append(i)
            fin_date_list.append(status_list[count_list[count]+1].replace('-','/'))
        else:
            yet_list.append(i)
        count += 1
    print(fin_list)
    print(yet_list)
    fin_count = list(range(0,len(fin_list)))
    yet_count = list(range(0,len(yet_list)))

    return render_template("status.html",
    fin_list=fin_list,fin_date_list=fin_date_list,
    yet_list=yet_list,vaccine_dict=vaccine_dict,
    fin_count=fin_count,yet_count=yet_count
    )

@app.route('/update')
def update():
    return render_template("update.html",vaccine_dict=vaccine_dict)

@app.route('/update_comp', methods=['GET','POST'])
def update_comp():
    # print("ok1")
    pre_update_img = request.files["update_img"]
    # print("ok")
    pre_update_img = base64.b64encode(pre_update_img.read())
    update_img = pre_update_img.decode('utf-8')

    update_name = request.form["update_name"]
    # print("ok")
    update_date = request.form["update_date"]
    # print("ok")
    login_name = session["login_name"]

    connection = getConnection()
    sql = "update status_table_2 set img_" + str(update_name) + " = '" + update_img + "', date_" + str(update_name) + " = '" + str(update_date) + "' where name = '" + str(login_name) + "'"
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    # login_list = cursor.fetchall()

    vaccine_name = vaccine_dict[int(update_name)][0]
    update_date = update_date.replace('-','/')
    return render_template("update_comp.html",update_date=update_date,vaccine_name=vaccine_name,update_img=update_img)

@app.route('/evidence')
def evidence():
    login_name = session["login_name"]
    connection = getConnection()
    sql = "select * from status_table_2 where name = '" + str(login_name) + "'"
    cursor = connection.cursor()
    cursor.execute(sql)
    status_list = cursor.fetchall()

    show_list = [] # [name,img,date]
    count = 1
    count_list = [1,3,5,7,9,11,13]
    for i in count_list:
        if not list(status_list[0])[i] == "non":
            show_list.append([vaccine_dict[count][0],list(status_list[0])[i],list(status_list[0])[i+1]])
        count += 1

    # print(show_list)
    return render_template("evidence.html",show_list=show_list)

@app.route('/send_evi', methods=['GET','POST'])
def send_evi():

    switch = 0
    if("send_name" in request.form):
        send_name_ = request.form["send_name"]
        send_text_ = request.form["send_text"]
        send_shop_ = request.form["send_shop"]
        switch += 1

    shop_list = ["マルバツドッグラン","サンカクペットホテル","シカクドッグラン","バツバツ病院","エックスツアー","ゼット倶楽部"]
    count_list = [1,3,5,7,9,11,13]

    login_name = session["login_name"]

    connection = getConnection()
    sql = "select * from status_table_2 where name = '" + str(login_name) + "'"
    cursor = connection.cursor()
    cursor.execute(sql)
    status_list = cursor.fetchall()
    status_list = status_list[0]

    # name: base64
    select_dict = {}
    count_ = 1
    for i in count_list:
        if not status_list[i] == "non":
            select_dict[vaccine_dict[count_][0]] = status_list[i]
        count_ += 1

    if switch == 1:
        count_ = 1
        for i in shop_list:
            if i == send_shop_:
                break
            count_ += 1
        # print(select_dict)
        str_ = str(send_shop_) + "='" + str(select_dict[send_name_]) + "',text_" + str(count_) + "='" + str(send_text_) + "' where name = '" + str(login_name) + "'"
        # print(str_)
        connection = getConnection()
        sql = "update send_evi_2 set " + str_
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()

    connection = getConnection()
    sql = "select * from send_evi_2 where name = '" + str(login_name) + "'"
    cursor = connection.cursor()
    cursor.execute(sql)
    evi_list_ = cursor.fetchall()
    evi_list_ = evi_list_[0]

    # shop_name: [base64, text]
    send_dict = {}
    count_list_ = [1,3,5,7,9,11]
    count_ = 0
    for i in count_list_:
        if not evi_list_[i] == "non":
            send_dict[shop_list[count_]] = [evi_list_[i], evi_list_[i+1]]
        count_ += 1


    return render_template("send_evi.html",shop_list=shop_list,select_dict=select_dict,send_dict=send_dict)

    # session["login_name"] = request.form["login_name"]
# if __name__ == '__main__':
#     main()
# alter table status_table_2 alter column img_7 type text;