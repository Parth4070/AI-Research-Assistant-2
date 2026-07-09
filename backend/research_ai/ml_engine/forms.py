from django import forms

class TrainModelForm(forms.Form):
    target_column = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-select'}))
    problem_type = forms.ChoiceField(
        choices=[
            ("classification", "Classification"),
            ("regression", "Regression")
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        columns = kwargs.pop("columns", [])
        super().__init__(*args, **kwargs)
        self.fields["target_column"].choices = [(col, col) for col in columns]
