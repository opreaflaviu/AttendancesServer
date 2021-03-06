import json
import dateutil.parser


class GeneratedAttendanceAgg:

    def __init__(self, database):
        self.database = database

    def insert_generated_attendance(self, request):
        attendance_data = json.loads(request.form.get("attendance"))
        course_name = attendance_data["courseName"]
        course_type = attendance_data["courseType"]
        course_class = attendance_data["courseClass"]
        course_teacher = attendance_data["courseTeacherName"]
        course_teacher_id = attendance_data["courseTeacherId"]
        course_created_at = dateutil.parser.parse(attendance_data["courseCreatedAt"])
        course_number = attendance_data["courseNumber"]
        attendance_qr = attendance_data["attendanceQR"]

        attendance_to_insert = {
            'courseName': course_name,
            'courseType': course_type,
            'courseClass': course_class,
            'courseTeacherName': course_teacher,
            'courseTeacherId': course_teacher_id,
            'courseCreatedAt': course_created_at,
            'courseNumber': course_number,
            'attendanceQR': attendance_qr
        }

        documents = self.database\
            .find_one({
                "courseName": course_name,
                "courseType": course_type,
                "courseClass": course_class,
                "courseTeacherId": course_teacher_id,
                "courseNumber": course_number,
            })
        if documents is not None:
            return json.dumps({'result': 'false'})
        else:
            insert = self.database.insert(attendance_to_insert)
            if insert:
                return json.dumps({'result': 'true'})
            else:
                return json.dumps({'result': 'false'})

    def get_teacher_generated_attendances(self, teacher_id, course_name):
        pipeline = [
            {'$match': {
                'courseTeacherId': teacher_id,
                'courseName': course_name}
            },

            {'$sort': {
                'courseName': 1,
                'courseCreatedAt': 1}
            },

            # {'$project': {'_id': 0}
            # }
        ]

        result = self.database.aggregate(pipeline)
        result_list = []
        for attendance in result:
            course_name = attendance["courseName"]
            course_type = attendance["courseType"]
            course_class = attendance["courseClass"]
            course_teacher_name = attendance["courseTeacherName"]
            course_teacher_id = attendance["courseTeacherId"]
            course_created_at = str(attendance["courseCreatedAt"])
            course_number = attendance["courseNumber"]
            attendance_qr = attendance["attendanceQR"]
            attendance_result = {
                'courseName': course_name,
                'courseType': course_type,
                'courseClass': course_class,
                'courseTeacherName': course_teacher_name,
                'courseTeacherId': course_teacher_id,
                'courseCreatedAt': course_created_at,
                'courseNumber': course_number,
                'attendanceQR': attendance_qr
            }
            result_list.append(attendance_result)

        output = {'result': result_list}
        return json.dumps(output)


    def get_generated_attendance_data(self, attendance_data):
        course_name = attendance_data["courseName"]
        course_type = attendance_data["courseType"]
        course_class = attendance_data["courseClass"]
        course_teacher = attendance_data["courseTeacherName"]
        course_teacher_id = attendance_data["courseTeacherId"]
        course_created_at = dateutil.parser.parse(attendance_data["courseCreatedAt"])
        course_number = attendance_data["courseNumber"]
        attendance_qr = attendance_data["attendanceQR"]

        attendance_to_insert = {
            'courseName': course_name,
            'courseType': course_type,
            'courseClass': course_class,
            'courseTeacherName': course_teacher,
            'courseTeacherId': course_teacher_id,
            'courseCreatedAt': course_created_at,
            'courseNumber': course_number,
            'attendanceQR': attendance_qr
        }

        return attendance_to_insert

    #remove generated attendances by attendanceQR field
    def remove_generated_attendance(self, request):
        attendance_qr = request.form.get("attendanceQR")

        delete_result = self.database.delete_many({
            "attendanceQR": attendance_qr
        })

        deleted_documents = delete_result.deleted_count
        output = {'deletedCount': deleted_documents}
        return json.dumps(output)