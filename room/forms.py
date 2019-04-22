from django import forms

class RoomForm(forms.Form):
    name = forms.CharField(label="Room Name", widget=forms.TextInput(attrs={'class': 'form-control col-md-4'}))
    description = forms.CharField(label="Room Description (required)", widget=forms.Textarea(attrs={'class': 'form-control'}))
    private = forms.BooleanField(label = "Make room Private?",required=False,widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    invitation = forms.CharField(label = "Invite other user",required = False, widget = forms.Textarea(
        attrs={'class': 'form-control', 'placeholder':'Enter coma-seperated username'}
    ))


