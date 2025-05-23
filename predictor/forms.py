from django import forms

class StudentDataForm(forms.Form):
    math_score = forms.IntegerField(label='Math Score', min_value=0, max_value=100)
    reading_score = forms.IntegerField(label='Reading Score', min_value=0, max_value=100)
    writing_score = forms.IntegerField(label='Writing Score', min_value=0, max_value=100)
    attendance = forms.IntegerField(label='Attendance (%)', min_value=60, max_value=100)
    study_hours = forms.IntegerField(label='Study Hours per Week', min_value=1, max_value=10)
