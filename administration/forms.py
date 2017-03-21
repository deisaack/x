from django import forms


from portals.models import Parent, EndTermExamPerformance, Student, Staff


class RegisterNewStudent(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "reg_no",
            "residence",
            'year_of_study',
            'image',
            'parent',
            'dob',
            'user_acc',
        ]



class RegisterNewParent(forms.ModelForm):
    class Meta:
        model = Parent
        fields = [
            "first_name",
            "last_name",
            'email',
            'phone',
            'image',
            'profession',
            'id_no',
            'residence',
            'dob',
        ]

