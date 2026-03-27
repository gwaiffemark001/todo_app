from django import forms

from .models import TodoItem


class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ["title", "description", "category", "date_due", "is_completed"]
        widgets = {
            "date_due": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Format initial value for datetime-local input
        if self.instance and self.instance.pk and self.instance.date_due:
            self.initial["date_due"] = self.instance.date_due.strftime("%Y-%m-%dT%H:%M")
