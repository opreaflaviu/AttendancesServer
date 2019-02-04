import json


class TeachersAgg:
    def __init__(self, database):
        self.database = database

    def insert_teacher(self, request):
        teacher_name = request.form.get('teacherName')
        teacher_id = request.form.get('teacherId'),
        password = request.form.get('teacherPassword')
        new_teacher = {
            'teacherName': teacher_name,
            'teacherPassword': password,
            'teacherId': str(teacher_id)[2:9],
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
