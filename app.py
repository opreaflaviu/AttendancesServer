
from flask_pymongo import PyMongo
from flask import Flask, request

from attendance_agg import AttendanceAgg
from generated_attendances import GeneratedAttendanceAgg
from teachers_agg import TeachersAgg
from users_agg import UsersAgg

app = Flask(__name__)

app.config["MONGO_URI"] = 'mongodb://localhost:27017/UBB_App'

mongo = PyMongo(app)


@app.route('/users/add', methods=['POST'])
def insert_user():
    user_agg = UsersAgg(mongo.db.users)
    response = user_agg.insert_student(request)
    print("response", response)
    return response


@app.route('/users/login', methods=['POST'])
def login_user():
    user_agg = UsersAgg(mongo.db.users)
    response = user_agg.login_student(request)
    print("response", response)
    return response


@app.route('/teachers/add', methods=['POST'])
def insert_teacher():
    teachers_agg = TeachersAgg(mongo.db.teachers)
    response = teachers_agg.insert_teacher(request)
    print("response", response)
    return response


@app.route('/teachers/login', methods=['POST'])
def login_teacher():
    teachers_agg = TeachersAgg(mongo.db.teachers)
    response = teachers_agg.login_teacher(request)
    print("response", response)
    return response


@app.route('/attendance/add', methods=['POST'])
def insert_attendance():
    attendance_agg = AttendanceAgg(mongo.db.attendance)
    return attendance_agg.insert_attendance(request)


@app.route('/attendance/<user_id>', methods=['GET'])
def get_student_attendances(user_id):
    print(user_id)
    attendance_agg = AttendanceAgg(mongo.db.attendance)
    return attendance_agg.get_student_attendances(user_id)


@app.route('/generated-attendance/add', methods=['POST'])
def insert_generated_attendance():
    generated_attendance_agg = GeneratedAttendanceAgg(mongo.db.generatedAttendance)
    return generated_attendance_agg.insert_generated_attendance(request)


@app.route('/attendance/get-student-attendance/<user_id>', methods=['GET'])
def search_student_attendances(user_id):
    print(user_id)
    attendance_agg = AttendanceAgg(mongo.db.attendance)
    return attendance_agg.search_student_attendances(user_id)


@app.route('/generated-attendance/<teacher_id>', methods=['GET'])
def get_teacher_generated_attendances(teacher_id):
    generated_attendance_agg = GeneratedAttendanceAgg(mongo.db.generatedAttendance)
    return generated_attendance_agg.get_teacher_generated_attendances(teacher_id)


@app.route('/attendance/at-course/<course_qr>', methods=['GET'])
def get_students_at_course(course_qr):
    attendance_agg = AttendanceAgg(mongo.db.attendance)
    return attendance_agg.get_students_at_course(course_qr)


@app.route('/hello')
def hello():
    print('hello')
    return 'hello'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run()