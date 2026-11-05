import unittest


def calculate_total(attendance, assignment, class_test, midterm, final):
    return attendance + assignment + class_test + midterm + final


def calculate_grade(total):
    if total >= 80:
        return "A+", 4.00
    elif total >= 75:
        return "A", 3.75
    elif total >= 70:
        return "A-", 3.50
    elif total >= 65:
        return "B+", 3.25
    elif total >= 60:
        return "B", 3.00
    elif total >= 55:
        return "B-", 2.75
    elif total >= 50:
        return "C+", 2.50
    elif total >= 45:
        return "C", 2.25
    elif total >= 40:
        return "D", 2.00
    else:
        return "F", 0.00


class ResultProcessingTestCase(unittest.TestCase):

    def test_total_marks(self):
        total = calculate_total(8, 9, 8, 25, 35)
        self.assertEqual(total, 85)

    def test_grade_calculation(self):
        self.assertEqual(calculate_grade(85), ("A+", 4.00))

    def test_fail_grade(self):
        self.assertEqual(calculate_grade(35), ("F", 0.00))


if __name__ == '__main__':
    unittest.main()