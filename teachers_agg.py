import json


class TeachersAgg:
    def __init__(self, database):
        self.database = database

    def insert_teacher(self, request):
        teacher_name = request.form.get('teacherName')
        teacher_id = request.form.get('teacherId'),
        password = request.form.get('teacherPassword')
        teacher_courses = request.form.get('teacherCourses')
        new_teacher = {
            'teacherName': teacher_name,
            'teacherPassword': password,
            'teacherId': str(teacher_id)[2:9],
            # teacher courses are always empty at the start and is ok to save only an empty list
            'teacherCourses': list()
        }

        find = self.database.find_one({'teacherId': teacher_id})
        if find:
            return json.dumps({'result': "{'inserted': false}"})
        else:
            self.database.insert(new_teacher)
            return json.dumps({'result': "{'inserted': true}"})

    def login_teacher(self, request):
        teacher_id = request.form.get('teacherId'),
        find = self.database.find_one({'teacherId': str(str(teacher_id)[2:9])})

        if find:
            print(find)
            return json.dumps({'result': {
                'teacherName': find['teacherName'],
                'teacherPassword': find['teacherPassword']
            }})
        else:
            return json.dumps({'result': "false"})

    def add_course(self, teacher_id, request):
        course_name = request.form.get('courseName')
        result = self.database.update(
            {'teacherId': teacher_id},
            {'$addToSet':
                {'teacherCourses': course_name}
            }
        )
        return json.dumps({'result': result['updatedExisting']})


    def delete_course(self, teacher_id, request):
        course_name = request.form.get('courseName')
        result = self.database.update(
            {'teacherId': teacher_id},
            {'$pull':
                {'teacherCourses': course_name}
            }
        )
        return json.dumps({'result': result['updatedExisting']})

    def get_course(self, teacher_id):
        pipeline = [
            {
                '$match': {
                    'teacherId': teacher_id}
            },
        ]
        result = self.database.aggregate(pipeline)
        result_list = []
        for el in result:
            result_list = list(set(el['teacherCourses']))
        output = {'result': result_list}
        return json.dumps(output)

    def generate_xls_file_at_couse(self, group_id, course_name):
        print("dd")