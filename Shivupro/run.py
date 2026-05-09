from flask import Flask, render_template, request, session, url_for, redirect, flash

import sqlite3 as sql
import os
from os.path import join, dirname, realpath
from flask_sqlalchemy import SQLAlchemy


UPLOADS_PATH = join(dirname(realpath(__file__)), 'static\\images')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'

# Admin auth: username-only (no registration, no password)
ADMIN_USERNAME = "admin"





def init_db():
    """Ensure required tables exist before any route uses them."""
    with sql.connect("data.db") as con:

        c = con.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS registers(
                username varchar,
                email varchar,
                password varchar
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS admin(
                email varchar,
                password varchar
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS raja(
                fullname varchar,
                email varchar,
                date date,
                nationality varchar,
                phone number,
                password varchar,
                Address varchar,
                gender varchar
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS admissions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname varchar,
                email varchar,
                date varchar,
                nationality varchar,
                phone varchar,
                password varchar,
                Address varchar,
                gender varchar,
                course varchar,
                college varchar,
                parent_name varchar,
                parent_phone varchar,
                city varchar,
                state varchar,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        con.commit()


@app.route("/")
def index():
    return render_template("index.html")




@app.route("/login")
def login():
    return render_template("login.html")




@app.route("/courseselection")
def courseselection():
    return render_template("courseselection.html")


@app.route("/recommend")
def recommend():
    # stage: sslc | puc | degree
    # course: selected course slug like science/engineering/mba
    stage = request.args.get("stage", "")
    course = request.args.get("course", "")

    stage_title_map = {
        "sslc": "After SSLC",
        "puc": "After PUC",
        "degree": "After Degree",
    }
    course_title_map = {
        "science": "Science",
        "commerce": "Commerce",
        "arts": "Arts",
        "diploma": "Diploma",
        "medical": "Medical",
        "engineering": "Engineering",
        "agbsc": "AGBSE",
        "degree": "Degree",
        "mca": "MCA",
        "mcom": "MCOM",
        "msc": "MSC",
        "mba": "MBA",
    }

    stage_title = stage_title_map.get(stage, stage)
    course_title = course_title_map.get(course, course)
    course_slug = course

    # Hardcoded top 5 recommendations (Bengaluru)
    recommendations = {
        "science": [
            {"slug": "christ-university", "name": "Christ University", "reason": "Strong UG academics and research culture", "type": "Industry-aligned programs", "estimated_intake": "High", "website": "https://christuniversity.in/"},
            {"slug": "jain-university", "name": "Jain University", "reason": "Modern curriculum and student support", "type": "Holistic learning", "estimated_intake": "Medium", "website": "https://www.jainuniversity.ac.in/"},
            {"slug": "presidency-college", "name": "Presidency College", "reason": "Good faculty and practical exposure", "type": "Mentorship-focused", "estimated_intake": "Medium"},
            {"slug": "nitte", "name": "Nitte (Deemed)", "reason": "Science labs and applied learning", "type": "Research opportunities", "estimated_intake": "High"},
            {"slug": "st-joseph", "name": "St. Joseph’s College", "reason": "Student-friendly campus environment", "type": "Outcome-based teaching", "estimated_intake": "Medium"},
        ],
        "commerce": [
            {"slug": "christ-university", "name": "Christ University", "reason": "Business-friendly learning approach", "type": "Case studies", "estimated_intake": "High"},
            {"slug": "jain-university", "name": "Jain University", "reason": "Strong faculty and industry projects", "type": "Career mentorship", "estimated_intake": "Medium"},
            {"slug": "pes", "name": "PES University", "reason": "Business + tech oriented exposure", "type": "Applied learning", "estimated_intake": "High"},
            {"slug": "m-s-ramaiah", "name": "MS Ramaiah", "reason": "Good infrastructure and learning resources", "type": "Student internships", "estimated_intake": "High"},
            {"slug": "bms", "name": "BMS College", "reason": "Reputation in commerce education", "type": "Academic rigor", "estimated_intake": "Medium"},
        ],
        "arts": [
            {"slug": "jain-university", "name": "Jain University", "reason": "Strong humanities ecosystem", "type": "Research + projects", "estimated_intake": "Medium"},
            {"slug": "christ-university", "name": "Christ University", "reason": "Global exposure and student clubs", "type": "Interdisciplinary learning", "estimated_intake": "High"},
            {"slug": "st-joseph", "name": "St. Joseph’s College", "reason": "Excellent guidance and culture", "type": "Mentor programs", "estimated_intake": "Medium"},
            {"slug": "presidency-college", "name": "Presidency College", "reason": "Balanced curriculum with practical learning", "type": "Outcome-driven", "estimated_intake": "Medium"},
            {"slug": "bms", "name": "BMS College", "reason": "Well-structured programs", "type": "Academic support", "estimated_intake": "Medium"},
        ],
        "diploma": [
            {"slug": "dayananda-sagar", "name": "Dayananda Sagar Institutions", "reason": "Bridge opportunities after diploma", "type": "Practical labs", "estimated_intake": "High"},
            {"slug": "mvj", "name": "MVJ College", "reason": "Supportive admission pathways", "type": "Career guidance", "estimated_intake": "Medium"},
            {"slug": "acharya", "name": "Acharya Institutions", "reason": "Good campus facilities", "type": "Skill-focused teaching", "estimated_intake": "High"},
            {"slug": "rv", "name": "R.V. College", "reason": "Reputed for academics", "type": "Mentorship", "estimated_intake": "Medium"},
            {"slug": "presidency-college", "name": "Presidency College", "reason": "Good learning environment", "type": "Structured programs", "estimated_intake": "Medium"},
        ],
        "medical": [
            {"slug": "bengaluru-medical-college", "name": "Bangalore Medical College", "reason": "Historic institution with clinical exposure", "type": "Hospital-based learning", "estimated_intake": "High"},
            {"slug": "msr-medicine", "name": "MS Ramaiah Medical College", "reason": "Strong patient-care learning", "type": "Clinical training", "estimated_intake": "Medium"},
            {"slug": "christ-university", "name": "Christ University (Allied Health)", "reason": "Allied programs with good faculty", "type": "Practice-driven", "estimated_intake": "Medium"},
            {"slug": "mcc", "name": "M S C Medical College", "reason": "Good teaching support", "type": "Student internships", "estimated_intake": "Medium"},
            {"slug": "sri-siddhartha", "name": "Sri Siddhartha Medical College", "reason": "Balanced academics and training", "type": "Mentored learning", "estimated_intake": "Medium"},
        ],
        "engineering": [
            {"slug": "pes", "name": "PES University", "reason": "Strong engineering + placements", "type": "Industry collaboration", "estimated_intake": "High"},
            {"slug": "jain-university", "name": "Jain University", "reason": "Good project culture", "type": "Skill labs", "estimated_intake": "Medium"},
            {"slug": "msr-engineering", "name": "MS Ramaiah Institute of Technology", "reason": "Reputed engineering programs", "type": "Hands-on learning", "estimated_intake": "High"},
            {"slug": "dayananda-sagar", "name": "Dayananda Sagar College of Engineering", "reason": "Modern teaching methods", "type": "Internship support", "estimated_intake": "Medium"},
            {"slug": "rv", "name": "R.V. College of Engineering", "reason": "Excellent faculty and labs", "type": "Project-driven", "estimated_intake": "High"},
        ],
        "agbsc": [
            {"slug": "university-of-agri", "name": "University of Agricultural Sciences", "reason": "Dedicated agri curriculum", "type": "Field + lab learning", "estimated_intake": "High"},
            {"slug": "gkvk", "name": "GKVK (UAS campus)", "reason": "Specialized research opportunities", "type": "Practical training", "estimated_intake": "Medium"},
            {"slug": "dayananda-sagar", "name": "Dayananda Sagar (Agri Programs)", "reason": "Good infrastructure for applied learning", "type": "Skill-based", "estimated_intake": "Medium"},
            {"slug": "jain-university", "name": "Jain University", "reason": "Interdisciplinary environment", "type": "Project mentoring", "estimated_intake": "Medium"},
            {"slug": "christ-university", "name": "Christ University (Relevant Programs)", "reason": "Strong academics and workshops", "type": "Practical exposures", "estimated_intake": "Medium"},
        ],
        "degree": [
            {"slug": "christ-university", "name": "Christ University", "reason": "Strong degree progression options", "type": "Academic guidance", "estimated_intake": "High"},
            {"slug": "jain-university", "name": "Jain University", "reason": "Good academic ecosystem", "type": "Student support", "estimated_intake": "Medium"},
            {"slug": "presidency-college", "name": "Presidency College", "reason": "Well-structured programs", "type": "Outcome-based", "estimated_intake": "Medium"},
            {"slug": "bms", "name": "BMS College", "reason": "Reputation and affordability", "type": "Stable academics", "estimated_intake": "Medium"},
            {"slug": "pes", "name": "PES University", "reason": "Degree programs with strong placements", "type": "Career support", "estimated_intake": "High"},
        ],
        "mca": [
            {"slug": "pes", "name": "PES University", "reason": "Software-focused learning and projects", "type": "Industry alignment", "estimated_intake": "High"},
            {"slug": "rv", "name": "R.V. College of Engineering", "reason": "Good CS ecosystem", "type": "Practical training", "estimated_intake": "Medium"},
            {"slug": "msr-engineering", "name": "MS Ramaiah Institute of Technology", "reason": "Strong computer labs", "type": "Capstone projects", "estimated_intake": "High"},
            {"slug": "dayananda-sagar", "name": "Dayananda Sagar", "reason": "Supportive faculty and learning", "type": "Project-driven", "estimated_intake": "Medium"},
            {"slug": "jain-university", "name": "Jain University", "reason": "Balanced theory + practice", "type": "Industry mentorship", "estimated_intake": "Medium"},
        ],
        "mcom": [
            {"slug": "christ-university", "name": "Christ University", "reason": "Strong commerce faculty", "type": "Research and analytics", "estimated_intake": "High"},
            {"slug": "jain-university", "name": "Jain University", "reason": "Good academic support", "type": "Case-based learning", "estimated_intake": "Medium"},
            {"slug": "bms", "name": "BMS College", "reason": "Reputation in commerce education", "type": "Academic rigor", "estimated_intake": "Medium"},
            {"slug": "presidency-college", "name": "Presidency College", "reason": "Structured learning pathways", "type": "Guided projects", "estimated_intake": "Medium"},
            {"slug": "pes", "name": "PES University (Business Studies)", "reason": "Commerce + analytics exposure", "type": "Industry projects", "estimated_intake": "High"},
        ],
        "msc": [
            {"slug": "christ-university", "name": "Christ University", "reason": "Research-friendly environment", "type": "Lab-based learning", "estimated_intake": "High"},
            {"slug": "jain-university", "name": "Jain University", "reason": "Strong science departments", "type": "Hands-on practice", "estimated_intake": "Medium"},
            {"slug": "pes", "name": "PES University", "reason": "Modern learning and labs", "type": "Capstone projects", "estimated_intake": "High"},
            {"slug": "presidency-college", "name": "Presidency College", "reason": "Good academic support", "type": "Mentored learning", "estimated_intake": "Medium"},
            {"slug": "bms", "name": "BMS College", "reason": "Stable and reputable", "type": "Outcome-driven", "estimated_intake": "Medium"},
        ],
        "mba": [
            {"slug": "iimb", "name": "Top MBA - Bengaluru (IIM-like Programs)", "reason": "High ROI and strong learning outcomes", "type": "Mentorship + projects", "estimated_intake": "High"},
            {"slug": "christ-university", "name": "Christ University", "reason": "Good business curriculum and clubs", "type": "Case studies", "estimated_intake": "Medium"},
            {"slug": "jain-university", "name": "Jain University", "reason": "Industry projects and placements", "type": "Experiential learning", "estimated_intake": "Medium"},
            {"slug": "pes", "name": "PES University", "reason": "Corporate exposure and training", "type": "Career mentorship", "estimated_intake": "High"},
            {"slug": "msr", "name": "MS Ramaiah", "reason": "Strong MBA ecosystem", "type": "Capstone + internships", "estimated_intake": "High"},
        ],
    }

    colleges = recommendations.get(course_slug, recommendations.get("engineering", []))

    # Provide extra fields expected by template
    colleges_prepared = []
    for c in colleges:
        colleges_prepared.append(c)

    return render_template(
        "recommend.html",
        stage=stage_title,
        course_title=course_title,
        course_slug=course_slug,
        colleges=colleges_prepared,
    )


@app.route("/apply")
def apply():
    course = request.args.get("course", "")
    college = request.args.get("college", "")

    # Convert slug to human readable (reverse lookup from recommend mapping)
    slug_to_name = {
        "christ-university": "Christ University",
        "jain-university": "Jain University",
        "presidency-college": "Presidency College",
        "bengaluru-medical-college": "Bangalore Medical College",
        "pes": "PES University",
        "msr-engineering": "MS Ramaiah Institute of Technology",
        "dayananda-sagar": "Dayananda Sagar College of Engineering",
        "rv": "R.V. College of Engineering",
        "m-s-ramaiah": "MS Ramaiah",
    }

    # best-effort display
    college_title = slug_to_name.get(college, college.replace("-", " ").title())
    course_title_map = {
        "science": "Science",
        "commerce": "Commerce",
        "arts": "Arts",
        "diploma": "Diploma",
        "medical": "Medical",
        "engineering": "Engineering",
        "agbsc": "AGBSE",
        "degree": "Degree",
        "mca": "MCA",
        "mcom": "MCOM",
        "msc": "MSC",
        "mba": "MBA",
    }
    course_title = course_title_map.get(course, course)

    return render_template("admission.html", course=course_title, college=college_title)


@app.route("/apply_action", methods=["POST"])
def apply_action():
    # Keep existing backend fields for identity.
    # Insert selected course/college into a separate table.
    fullname = request.form.get("fullname", "")
    email = request.form.get("email", "")
    date = request.form.get("date", "")
    nationality = request.form.get("nationality", "")
    phone = request.form.get("phone", "")
    password = request.form.get("password", "")
    Address = request.form.get("Address", "")
    gender = request.form.get("gender", "")

    course = request.form.get("course", "")
    college = request.form.get("college", "")

    parent_name = request.form.get("parent_name", "")
    parent_phone = request.form.get("parent_phone", "")
    city = request.form.get("city", "")
    state = request.form.get("state", "")

    with sql.connect("data.db") as con:
        c = con.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS admissions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname varchar,
                email varchar,
                date varchar,
                nationality varchar,
                phone varchar,
                password varchar,
                Address varchar,
                gender varchar,
                course varchar,
                college varchar,
                parent_name varchar,
                parent_phone varchar,
                city varchar,
                state varchar,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        c.execute(
            """
            INSERT INTO admissions(fullname,email,date,nationality,phone,password,Address,gender,course,college,parent_name,parent_phone,city,state)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (fullname, email, date, nationality, phone, password, Address, gender, course, college, parent_name, parent_phone, city, state),
        )
        con.commit()

    return render_template("success.html", msg="Admission application submitted successfully")



@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/addmission")
def admission():
   return render_template("admission.html")

@app.route("/agbsc")
def agbsc():
    return render_template("agbsc.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/arts")
def arts():
    return render_template("arts.html")

@app.route("/collsec")
def collsec():
    return render_template("collsec.html")

@app.route("/commerce")
def commerce():
    return render_template("commerce.html")

@app.route("/degree")
def degree():
    return render_template("degree.html")

@app.route("/diplamo")
def diplamo():
    return render_template("diplamo.html")

@app.route("/engineering")
def engineering():
    return render_template("engineering.html")

@app.route("/admin_login")
def Subbu():
    return render_template("adminlogin.html")




@app.route("/mba")
def mba():
    return render_template("mba.html")

@app.route("/mca")
def mca():
    return render_template("mca.html")

@app.route("/mcom")
def mcom():
    return render_template("mcom.html")

@app.route("/medical")
def medical():
    return render_template("medical.html")

@app.route("/msc")
def msc():
    return render_template("msc.html")

@app.route("/science")
def science():
    return render_template("science.html")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")


@app.route("/adminreh")
def admin_registration_page():
    return render_template("adminreh.html", msg=None)



@app.route("/adminlogin")
def adminnlogin():
    return render_template("adminlogin.html")


@app.route("/admin_register")
def admin_login():
    # keep backward compatibility if any template points to this name
    return redirect(url_for("admin_registration_page"))





@app.route("/regActionnn", methods=["POST"])
def regActi():
    email = (request.form.get("email") or "").strip()
    password = (request.form.get("password") or "").strip()

    if not email or not password:
        flash("Invalid admin registration details")
        return redirect(url_for("admin_login"))

    with sql.connect("data.db") as con:
        c = con.cursor()
        c.execute("INSERT INTO admin(email,password) VALUES(?,?)", (email, password))
        con.commit()

    flash("Admin registration successful. Please login.")
    return redirect(url_for("adminnlogin"))




@app.route("/admin_login_action", methods=['POST'])
def adminlog():
    msg = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()

        if username and username == ADMIN_USERNAME:
            session["admin_logged_in"] = True
            session["admin_email"] = username
            flash("Admin login successful")
            return redirect(url_for('admin_dashboard'))

        msg = "Invalid admin username"
        flash("Admin login unsuccessful")

    return render_template("adminlogin.html", msg=msg)




@app.route("/admin_dashboard")
def admin_dashboard():
    if "admin_logged_in" not in session:
        return redirect(url_for('admin_login'))

    with sql.connect("data.db") as con:
        c = con.cursor()
        # registers: (username, email, password)
        c.execute("SELECT username, email FROM registers")
        users = c.fetchall()

    return render_template("admin_dashboard.html", users=users)



@app.route("/student_details")
def student_details():
    if "admin_logged_in" not in session:
        return redirect(url_for('admin_login'))

    email = request.args.get("email", "").strip()
    if not email:
        return redirect(url_for("admin_dashboard"))

    with sql.connect("data.db") as con:
        c = con.cursor()
        c.execute("SELECT fullname,email,date,nationality,phone,password,Address,gender FROM raja WHERE email = ?", (email,))
        row = c.fetchone()

    # row can be None if the student hasn't submitted details yet
    return render_template("student_details.html", student=row, email=email)




@app.route("/delete_user", methods=['POST'])
def delete_user():
    if "admin_logged_in" not in session:
        return redirect(url_for('admin_login'))
    
    username = request.form['username']
    with sql.connect("data.db") as con:
        c = con.cursor()
        c.execute("DELETE FROM registers WHERE username = ?", (username,))
        con.commit()
        flash("User deleted successfully")
    return redirect(url_for('admin_dashboard'))

@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    session.pop("admin_email", None)
    session.pop("logedin", None)
    session.pop("username", None)
    flash("Logged out successfully")
    # Redirect to landing page
    return redirect(url_for('index'))






       
@app.route("/regAction", methods = ["GET","POST"])
def regActio():
    msg=None
    if(request.method=="POST"):
        if (request.form["username"]!="" and request.form["email"]!=""and request.form["password"]!="" ):
            name = request.form["username"]
            email = request.form["email"]
            pasword = request.form["password"] 

            with sql.connect("data.db") as con:
                c=con.cursor()
                c.execute("INSERT INTO  registers(username,email,password) VALUES('"+name+"','"+email+"','"+pasword+"')")
                msg = "Register Details submitted successfully"

                con.commit()
        else:
            msg="Someting went wrong"
        flash("DETAILS SAVED SUCCESSFULLY")
        return render_template("login.html", msg=msg)
        
           
@app.route("/loginAction",methods=['GET','POST'])
def loginAction():
    msg=None
    if (request.method == "POST"):
        username = request.form['username']
      
        password = request.form['password']
        
        with sql.connect("data.db") as con:
            c=con.cursor()
            c.execute("SELECT username,password  FROM registers WHERE username = '"+username+"' and password ='"+password+"'")
            r=c.fetchall()
            for i in r:
                if(username==i[0] and password==i[1]):
                    session["logedin"]=True
                    session["username"]=username
                    flash("LOGIN SUCCESSFULL")
                    return redirect("/courseselection")         
                else:
                    msg= "please enter valid username and password"
                    flash("LOGIN UNSUCCESSFULL")
            return render_template("login.html",msg=msg) 
        



@app.route("/details", methods = ["GET","POST"])
def detailsapp():
    msg=None
    if(request.method=="POST"):
        if (request.form["fullname"]!="" and request.form["email"]!="" and request.form["date"]!="" and request.form["nationality"]!="" and request.form["phone"]!=""and request.form["password"]!="" and request.form["Address"]!="" and request.form["gender"]!=""):
            fullname = request.form["fullname"]
            email = request.form["email"]
            date= request.form["date"] 
            nationality= request.form["nationality"]
            phone= request.form["phone"]
            password = request.form["password"] 
            Address= request.form["Address"]
            gender= request.form["gender"]
            
            with sql.connect("data.db") as con:
                c=con.cursor()
                c.execute("INSERT INTO  raja(fullname,email,date,nationality,phone,password,Address,gender) VALUES('"+fullname+"','"+email+"','"+date+"','"+nationality+"','"+phone+"','"+password+"','"+Address+"','"+gender+"')")
                msg = "Register Details submitted successfully"
                con.commit()
        
        else:
            msg="Something went wrong"
        flash("DETAILS SAVED SUCCESSFULLY")
        return render_template("success.html", msg=msg)

        

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

