
from flask_pymongo import PyMongo
from flask import Flask, request, send_file

from attendance_agg import AttendanceAgg
from generated_attendances import GeneratedAttendanceAgg
from teachers_agg import TeachersAgg
from users_agg import UsersAgg
from xls_file_generator import XLS_File_Generator

app = Flask(__name__)

# For development
app.config["MONGO_URI"] = 'mongodb://localhost:27017/UBB_App'

# For production
# app.config["MONGO_URI"] = 'mongodb://linux.scs.ubbcluj.ro:27017/studentsStats'

mongo = PyMongo(app)


@app.route('/users/add', methods=['POST'])
def insert_student():
    user_agg = UsersAgg(mongo.db.users)
    response = user_agg.insert_student(request)
    return response


@app.route('/teachers/add', methods=['POST'])
def insert_teacher():
    teachers_agg = TeachersAgg(mongo.db.teachers)
    response = teachers_agg.insert_teacher(request)
    return response


@app.route('/users/login', methods=['POST'])
def login_student():
    user_agg = UsersAgg(mongo.db.users)
    response = user_agg.login_student(request)
    return response


@app.route('/teachers/login', methods=['POST'])
def login_teacher():
    teachers_agg = TeachersAgg(mongo.db.teachers)
    response = teachers_agg.login_teacher(request)
    return response


@app.route('/teachers/<teacher_id>/courses/add', methods=["POST"])
def add_course_to_teacher(teacher_id):
    teachers_agg = TeachersAgg(mongo.db.teachers)
    response = teachers_agg.add_course(teacher_id, request)
    return response


@app.route('/teachers/<teacher_id>/courses/delete', methods=["POST"])
def delete_course_of_teacher(teacher_id):
    teachers_agg = TeachersAgg(mongo.db.teachers)
    response = teachers_agg.delete_course(teacher_id, request)
    return response


@app.route('/teachers/<teacher_id>/courses', methods=["GET"])
def get_courses_of_teachers(teacher_id):
    teachers_agg = TeachersAgg(mongo.db.teachers)
    response = teachers_agg.get_course(teacher_id)
    return response


@app.route('/attendance/add', methods=['POST'])
def insert_attendance():
    attendance_agg = AttendanceAgg(mongo.db.attendance)
    return attendance_agg.insert_attendance(request)


@app.route('/generated-attendance/add', methods=['POST'])
def insert_generated_attendance():
    generated_attendance_agg = GeneratedAttendanceAgg(mongo.db.generatedAttendance)
    return generated_attendance_agg.insert_generated_attendance(request)

@app.route('/generated-attendance/remove', methods=['POST'])
def remove_generated_attendance():
    generated_attendance_agg = GeneratedAttendanceAgg(mongo.db.generatedAttendance)
    attendance_agg = AttendanceAgg(mongo.db.attendance)
    attendance_agg.remove_generated_attendance(request)
    return generated_attendance_agg.remove_generated_attendance(request)


@app.route('/attendance/<user_id>', methods=['GET'])
def get_student_attendances(user_id):
    attendance_agg = AttendanceAgg(mongo.db.attendance)
    return attendance_agg.get_student_attendances(user_id)


@app.route('/generated-attendance/<teacher_id>/<course_name>', methods=['GET'])
def get_teacher_generated_attendances(teacher_id, course_name):
    generated_attendance_agg = GeneratedAttendanceAgg(mongo.db.generatedAttendance)
    return generated_attendance_agg.get_teacher_generated_attendances(teacher_id, course_name)


@app.route('/attendance/at-course/<course_qr>', methods=['GET'])
def get_students_at_course(course_qr):
    attendance_agg = AttendanceAgg(mongo.db.attendance)
    return attendance_agg.get_students_at_course(course_qr)


@app.route('/attendance/get-student-attendance/<user_id>', methods=['GET'])
def search_student_attendances(user_id):
    attendance_agg = AttendanceAgg(mongo.db.attendance)
    return attendance_agg.search_student_attendances(user_id)


@app.route('/attendance/update-student-attendance', methods=['PATCH'])
def update_student_attendances():
    attendance_agg = AttendanceAgg(mongo.db.attendance)
    return attendance_agg.update_student_grade(request)


@app.route('/downloads', methods=['GET'])
def download():
    course_name =request.headers.get('courseName')
    students_class_id =request.headers.get('classId')
    filename = 'Statistics_' + str(course_name) + '_' + str(students_class_id)
    print("download", filename)

    attendance_agg = AttendanceAgg(mongo.db.attendance)
    result = attendance_agg.get_group_data(course_name, students_class_id)

    xls = XLS_File_Generator()
    xls.generate_xls_file_at_course(result, filename)

    response = send_file('generated_xlsx_files/' + filename + '.xlsx',
                     mimetype='application/excel',
                     as_attachment=True)
    response.headers['filename'] = filename
    return response


# Route for testing
@app.route('/hello')
def hello():
    print('hello')
    return 'hello'

if __name__ == '__main__':
    app.run(threaded=True)