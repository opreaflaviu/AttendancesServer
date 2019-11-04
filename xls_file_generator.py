import xlsxwriter


class XLS_File_Generator:

    def generate_xls_file_at_course(self, students_data_list, filename):
        # format table
        workbook = xlsxwriter.Workbook("generated_xlsx_files/" + filename + ".xlsx")
        worksheet = workbook.add_worksheet()
        student_name_column_width = 45
        student_id_column_width = 15
        attendance_column_width = 20
        grade_column_width = 15

        attendance_cell_format = workbook.add_format(
            {'bold': False, 'align': 'center', 'bg_color': '#e6ffe6', 'bottom': 5, 'left': 1, 'right': 1})
        grade_cell_format = workbook.add_format(
            {'bold': False, 'align': 'center', 'bg_color': '#ccf2ff', 'bottom': 5, 'left': 1, 'right': 1})
        name_cell_format = workbook.add_format(
            {'bold': False, 'align': 'center', 'bg_color': '#ffffcc', 'bottom': 5, 'left': 1, 'right': 1})
        student_id_cell_format = workbook.add_format(
            {'bold': False, 'align': 'center', 'bg_color': '#ffffcc', 'bottom': 5, 'left': 1, 'right': 1})

        attendance_cell_format_header = workbook.add_format(
            {'font_size': 13, 'bold': True, 'align': 'center', 'bg_color': '#e6ffe6', 'bottom': 5, 'top': 5, 'left': 1, 'right': 1})
        grade_cell_format_header = workbook.add_format(
            {'font_size': 13, 'bold': True, 'align': 'center', 'bg_color': '#ccf2ff', 'bottom': 5, 'top': 5, 'left': 1, 'right': 1})
        name_cell_format_header = workbook.add_format(
            {'font_size': 13, 'bold': True, 'align': 'center', 'bg_color': '#ffffcc', 'bottom': 5, 'top': 5, 'left': 1, 'right': 1})
        student_id_cell_format_header = workbook.add_format(
            {'font_size': 13, 'bold': True, 'align': 'center', 'bg_color': '#ffffcc', 'bottom': 5, 'top': 5, 'left': 1, 'right': 1})

        worksheet.set_column(1, 0, student_name_column_width)
        worksheet.set_column(1, 1, student_id_column_width)

        for column in range(2, 59):
            if column % 2 == 0:
                worksheet.set_column(column, column, attendance_column_width)
            else:
                worksheet.set_column(column, column, grade_column_width)

        # add header to table
        worksheet.write('A5', "Name", name_cell_format_header)
        worksheet.write('B5', "Student Id", student_id_cell_format_header)

        index = 0
        for cell_name, item in self.get_table_header():
            if index % 2 == 0:
                worksheet.write(cell_name, item, attendance_cell_format_header)
            else:
                worksheet.write(cell_name, item, grade_cell_format_header)
            index += 1

        # add data to table
        for item_index in range(0, len(students_data_list)):
            row = 5 + item_index
            name_cell = 'A' + str(row+1)
            id_cell = 'B' + str(row+1)
            worksheet.write(name_cell, "Name", name_cell_format)
            worksheet.write(id_cell, "Student Id", student_id_cell_format)
            for column in range(2, 58):
                if column % 2 == 0:
                    worksheet.write(row, column, '-', attendance_cell_format)
                else:
                    worksheet.write_number(row, column, 0, grade_cell_format)

        self.add_students_attendances_to_table(workbook, worksheet, students_data_list)

        workbook.close()

        print("done")

    def add_students_attendances_to_table(self, workbook, worksheet, students_data_list):
        for position, student_data in enumerate(students_data_list):
            self.add_student_name_to_row(workbook, worksheet, student_data['_id'], position)
            self.add_student_id_to_row(workbook, worksheet, student_data['studentId'], position)
            self.add_student_attendances_to_row(workbook, worksheet, student_data['events'], position)

    def add_student_attendances_to_row(self, workbook, worksheet, student_attendances_list, row_number):
        for student_data in student_attendances_list:
            print("attendances: ", student_data)
            if student_data['courseType'] == 'Laboratory':
                laboratory_number = student_data['courseNumber']
                laboratory_grade = student_data['grade']
                laboratory_cell = self.get_laboratory_cell(laboratory_number, row_number)
                laboratory_grade_cell = self.get_laboratory_grade_cell(laboratory_number, row_number)
                self.add_student_attendance(workbook, worksheet, laboratory_cell)
                self.add_student_grade(workbook, worksheet, laboratory_grade, laboratory_grade_cell)
            elif student_data['courseType'] == 'Seminar':
                seminar_number = student_data['courseNumber']
                seminar_grade = student_data['grade']
                seminar_cell = self.get_seminar_cell(seminar_number, row_number)
                seminar_grade_cell = self.get_seminar_grade_cell(seminar_number, row_number)
                self.add_student_attendance(workbook, worksheet, seminar_cell)
                self.add_student_grade(workbook, worksheet, seminar_grade, seminar_grade_cell)
            else:
                print("Course type is not Laboratory or Seminar")

    def add_student_name_to_row(self, workbook, worksheet, student_name, row_number):
        name_cell_format = workbook.add_format(
            {'bold': True, 'align': 'center', 'bg_color': '#ffffcc', 'bottom': 5, 'left': 1, 'right': 1})
        row = 'A' + str(6 + row_number)
        worksheet.write(row, student_name, name_cell_format)

    def add_student_id_to_row(self, workbook, worksheet, student_id, row_number):
        student_id_cell_format = workbook.add_format(
            {'bold': True, 'align': 'center', 'bg_color': '#ffffcc', 'bottom': 5, 'left': 1, 'right': 1})
        row = 'B' + str(6 + row_number)
        worksheet.write(row, student_id, student_id_cell_format)

    def add_student_grade(self, workbook, worksheet, student_grade, row):
        grade_cell_format = workbook.add_format(
            {'bold': True, 'align': 'center', 'bg_color': '#ccf2ff', 'bottom': 5, 'left': 1, 'right': 1})
        worksheet.write_number(row, student_grade, grade_cell_format)

    def add_student_attendance(self, workbook, worksheet, row):
        attendance_cell_format = workbook.add_format(
            {'bold': True, 'align': 'center', 'bg_color': '#e6ffe6', 'bottom': 5, 'left': 1, 'right': 1})
        worksheet.write(row, 'X', attendance_cell_format)

    def get_laboratory_cell(self, laboratory_number, row_number):
        laboratory = 'Laboratory ' + str(laboratory_number)

        cell_list = {
            'Laboratory 1': 'C',
            'Laboratory 2': 'E',
            'Laboratory 3': 'G',
            'Laboratory 4': 'I',
            'Laboratory 5': 'K',
            'Laboratory 6': 'M',
            'Laboratory 7': 'O',
            'Laboratory 8': 'Q',
            'Laboratory 9': 'S',
            'Laboratory 10': 'U',
            'Laboratory 11': 'W',
            'Laboratory 12': 'Y',
            'Laboratory 13': 'AA',
            'Laboratory 14': 'AC'
        }

        row_number += 6
        cell = cell_list[laboratory] + str(row_number)
        return cell

    def get_laboratory_grade_cell(self, laboratory_number, row_number):
        laboratory = 'Laboratory ' + str(laboratory_number)

        cell_list = {
            'Laboratory 1': 'D',
            'Laboratory 2': 'F',
            'Laboratory 3': 'H',
            'Laboratory 4': 'J',
            'Laboratory 5': 'L',
            'Laboratory 6': 'N',
            'Laboratory 7': 'P',
            'Laboratory 8': 'R',
            'Laboratory 9': 'T',
            'Laboratory 10': 'V',
            'Laboratory 11': 'X',
            'Laboratory 12': 'Z',
            'Laboratory 13': 'AB',
            'Laboratory 14': 'AD'
        }

        row_number += 6
        cell = cell_list[laboratory] + str(row_number)
        return cell

    def get_seminar_cell(self, seminar_number, row_number):
        seminar = 'Seminar ' + str(seminar_number)

        cell_list = {
            'Seminar 1': 'AE',
            'Seminar 2': 'AG',
            'Seminar 3': 'AI',
            'Seminar 4': 'AK',
            'Seminar 5': 'AM',
            'Seminar 6': 'AO',
            'Seminar 7': 'AQ',
            'Seminar 8': 'AS',
            'Seminar 9': 'AU',
            'Seminar 10': 'AW',
            'Seminar 11': 'AY',
            'Seminar 12': 'BA',
            'Seminar 13': 'BC',
            'Seminar 14': 'BE'
        }

        row_number += 6
        cell = cell_list[seminar] + str(row_number)
        return cell

    def get_seminar_grade_cell(self, seminar_number, row_number):
        seminar = 'Seminar ' + str(seminar_number)

        cell_list = {
            'Seminar 1': 'AF',
            'Seminar 2': 'AH',
            'Seminar 3': 'AJ',
            'Seminar 4': 'AL',
            'Seminar 5': 'AN',
            'Seminar 6': 'AP',
            'Seminar 7': 'AR',
            'Seminar 8': 'AT',
            'Seminar 9': 'AV',
            'Seminar 10': 'AX',
            'Seminar 11': 'AZ',
            'Seminar 12': 'BB',
            'Seminar 13': 'BD',
            'Seminar 14': 'BF'
        }

        row_number += 6
        cell = cell_list[seminar] + str(row_number)
        return cell

    def get_table_header(self):
        header = (
            ["C5", "Laboratory 1"],
            ["D5", "Grade"],
            ["E5", "Laboratory 2"],
            ["F5", "Grade"],
            ["G5", "Laboratory 3"],
            ["H5", "Grade"],
            ["I5", "Laboratory 4"],
            ["J5", "Grade"],
            ["K5", "Laboratory 5"],
            ["L5", "Grade"],
            ["M5", "Laboratory 6"],
            ["N5", "Grade"],
            ["O5", "Laboratory 7"],
            ["P5", "Grade"],
            ["Q5", "Laboratory 8"],
            ["R5", "Grade"],
            ["S5", "Laboratory 9"],
            ["T5", "Grade"],
            ["U5", "Laboratory 10"],
            ["V5", "Grade"],
            ["W5", "Laboratory 11"],
            ["X5", "Grade"],
            ["Y5", "Laboratory 12"],
            ["Z5", "Grade"],
            ["AA5", "Laboratory 13"],
            ["AB5", "Grade"],
            ["AC5", "Laboratory 14"],
            ["AD5", "Grade"],

            ["AE5", "Seminar 1"],
            ["AF5", "Grade"],
            ["AG5", "Seminar 2"],
            ["AH5", "Grade"],
            ["AI5", "Seminar 3"],
            ["AJ5", "Grade"],
            ["AK5", "Seminar 4"],
            ["AL5", "Grade"],
            ["AM5", "Seminar 5"],
            ["AN5", "Grade"],
            ["AO5", "Seminar 6"],
            ["AP5", "Grade"],
            ["AQ5", "Seminar 7"],
            ["AR5", "Grade"],
            ["AS5", "Seminar 8"],
            ["AT5", "Grade"],
            ["AU5", "Seminar 9"],
            ["AV5", "Grade"],
            ["AW5", "Seminar 10"],
            ["AX5", "Grade"],
            ["AY5", "Seminar 11"],
            ["AZ5", "Grade"],
            ["BA5", "Seminar 12"],
            ["BB5", "Grade"],
            ["BC5", "Seminar 13"],
            ["BD5", "Grade"],
            ["BE5", "Seminar 14"],
            ["BF5", "Grade"],
        )
        return header
