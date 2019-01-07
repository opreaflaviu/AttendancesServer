import json
import dateutil.parser


class AttendanceAgg:

    def __init__(self, database):
        self.database = database

    def insert_attendance(self, request):
        attendance_data = json.loads(request.form.get("attendance"))

        event_created_at = dateutil.parser.parse(attendance_data["eventCreatedAt"])
        course_name = attendance_data["course"]["courseName"]
        course_type = attendance_data["course"]["courseType"]
        course_class = attendance_data["course"]["courseClass"]
        course_teacher = attendance_data["course"]["courseTeacherName"]
        course_teacher_id = attendance_data["course"]["courseTeacherId"]
        course_created_at = dateutil.parser.parse(attendance_data["course"]["courseCreatedAt"])
        course_number = attendance_data["course"]["courseNumber"]

        student_id = attendance_data["student"]["studentId"]
        student_name = attendance_data["student"]["studentName"]
        student_class = attendance_data["student"]["classId"]

        course_qr = attendance_data["attendanceQR"]

        attendance_to_insert = {
            'eventCreatedAt': event_created_at,
            'student': {
                'studentId': student_id,
                'studentName': student_name,
                'classId': student_class
            },
            'course': {
                'courseName': course_name,
                'courseType': course_type,
                'courseClass': course_class,
                'courseTeacherName': course_teacher,
                'courseTeacherId': course_teacher_id,
                'courseCreatedAt': course_created_at,
                'courseNumber': course_number
            },
            'attendanceQR': course_qr
        }
        insert = self.database.insert(attendance_to_insert)
        if insert:
            return json.dumps({'result': 'true'})
        else:
            return json.dumps({'result': 'false'})

    def get_student_attendances(self, user_id):
        pipeline = [
            {
                '$match': {
                    'student.studentId': user_id
                }
            },

            {
                '$group': {
                    '_id': '$course.courseName',
                    'events': {
                        '$push': {
                            'courseCreatedAt': '$eventCreatedAt',
                            'courseType': '$course.courseType',
                            'courseNumber': '$course.courseNumber',
                            'courseTeacherName': '$course.courseTeacherName',
                        }
                    }
                }
            },

            {
                '$addFields': {
                    'courseName': '$_id',
                    'attendances': '$events'
                }
            },

            {
                '$project': {
                    '_id': 0,
                    'events': 0
                }
            }
        ]

        result = self.database.aggregate(pipeline)
        result_list = []
        for r in result:
            course_list = []
            for a in r["attendances"]:
                course_data = {
                    'courseCreatedAt': str(a["courseCreatedAt"]),
                    'courseType': a["courseType"],
                    'courseNumber': a["courseNumber"],
                    'courseTeacherName': a["courseTeacherName"],
                }
                course_list.append(course_data)
            attendance = {
                "courseName": r["courseName"],
                "attendances": course_list
            }

            result_list.append(attendance)
        return json.dumps({'result': result_list})

    def search_student_attendances(self, student_id):
        pipeline = [
            {
                '$match': {
                    'student.studentId': student_id
                }
            },

            {
                '$sort': {
                    'course.name': 1,
                    'course.type': -1,
                    'course.number': 1
                }
            },

            {
                '$addFields': {
                    'courseName': '$course.courseName',
                    'courseType': '$course.courseType',
                    'courseTeacherName': '$course.courseTeacherName',
                    'courseTeacherId': '$course.courseTeacherId',
                    'courseCreatedAt': '$course.courseCreatedAt',
                    'courseNumber': '$course.courseNumber',
                }
            },

            {
                '$project': {
                    '_id': 0,
                    'studentId': 0,
                    'course': 0
                }
            }
        ]

        result = self.database.aggregate(pipeline)
        result_list = []
        for r in result:
            attendance = {
                'courseName': r['courseName'],
                'courseType': r['courseType'],
                'courseTeacherName': r['courseTeacherName'],
                'courseTeacherId': r['courseTeacherId'],
                'courseCreatedAt': str(r['courseCreatedAt']),
                'courseNumber': r['courseNumber'],
            }
            result_list.append(attendance)
        return json.dumps({'result': result_list})

    def get_students_at_course(self, course_qr):
        pipeline = [
            {
                '$match': {
                    'attendanceQR': course_qr}
            },

            {
                '$sort': {'student.studentName': 1}
            }
        ]

        result = self.database.aggregate(pipeline)
        result_list = []

        for studentAttendance in result:
            event_created_at = str(studentAttendance['eventCreatedAt'])
            student_id = studentAttendance['student']['studentId']
            student_name = studentAttendance['student']['studentName']
            student_class = studentAttendance['student']['classId']
            course_name = studentAttendance['course']['courseName']
            course_type = studentAttendance['course']['courseType']
            course_class = studentAttendance['course']['courseClass']
            course_teacher_name = studentAttendance['course']['courseTeacherName']
            course_teacher_id = studentAttendance['course']['courseTeacherId']
            course_created_at = str(studentAttendance['course']['courseCreatedAt'])
            course_number = studentAttendance['course']['courseNumber']
            attendance_qr = studentAttendance['attendanceQR']

            student_attendance_dict = {
                'eventCreatedAt': event_created_at,
                'student': {
                    'studentId': student_id,
                    'studentName': student_name,
                    'classId': student_class
                },
                'course': {
                    'courseName': course_name,
                    'courseType': course_type,
                    'courseClass': course_class,
                    'courseTeacherName': course_teacher_name,
                    'courseTeacherId': course_teacher_id,
                    'courseCreatedAt': str(course_created_at),
                    'courseNumber': course_number
                },
                'attendanceQR': attendance_qr
            }

            result_list.append(student_attendance_dict)

        return json.dumps({'result': result_list})