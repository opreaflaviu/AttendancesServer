import json



class UsersAgg:
    def __init__(self, database):
        self.database = database

    def get_user(self, user_id: str):
        output = []
        for data in self.database.find({'studentId': user_id}):
            user = {'studentName': data['studentName'], 'studentPassword': data['studentPassword'], 'classId': data['classId']}
            output.append(user)

        return json.dumps({'result': output})

    def insert_student(self, request):
        student_name = request.form.get('studentName')
        student_id = request.form.get('studentId'),
        password = request.form.get('studentPassword')
        student_class = request.form.get('classId')
        new_student = {
            'studentName': student_name,
            'studentPassword': password,
            'studentId': str(student_id)[2:10],
            'classId': student_class
        }

        find = self.database.find_one({'studentId': student_id})
        if find:
            return json.dumps({'result': "{'inserted': False}"})
        else:
            self.database.insert(new_student)
            return json.dumps({'result': "{'inserted': True}"})

    def login_student(self, request):
        student_id = request.form.get('studentId'),
        password = request.form.get('studentPassword')
        find = self.database.find_one({'studentId': str(str(student_id)[2:10]), 'studentPassword': str(password)})

        if find:
            return json.dumps({'result': {
                'studentName': find['studentName'],
                'classId': find['classId'],
            }})
        else:
            return json.dumps({'result': "false"})
