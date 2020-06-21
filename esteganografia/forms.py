from django import forms

class EsteganografiaCifradoForm(forms.Form):
    mensaje_cifrar = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 5, 'class': 'form-control form-control-sm'}))
    llave_secreta = forms.CharField(max_length=16, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}))
    imagen = forms.ImageField()

class EsteganografiaDescifradoForm(forms.Form):
    llave_secreta = forms.CharField(max_length=16, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}))
    imagen = forms.ImageField()