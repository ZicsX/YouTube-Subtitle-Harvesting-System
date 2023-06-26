from django import forms

class APIKeyForm(forms.Form):
    api_key = forms.CharField(label='API Key', max_length=100)

class SeedQueryForm(forms.Form):
    seed_query = forms.CharField(label='Seed Query', max_length=500)
