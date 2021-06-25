from django import forms


class ConnexionForm(forms.Form):
    inputPseudo = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Votre Pseudo', 'class': 'form-control'}),
        required=True
    )
    inputPassword = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Mot de passe', 'class': 'form-control', 'type': 'password'}),
        required=True
    )


class ChantierModif(object):
    inputName = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class': 'form-control'}),
        required=True
    )


class ChantierForm(forms.Form):
    Entite_choices = (
        ('progimo', 'Progimo'),
        ('prologe', 'Prologe'),
        ('prologeM', 'Prologe Marche')
    )

    Type_choices = (
        ('Para-DP', 'Demande de prix Parachévement'),
        ('Para-CP', 'Comparatif Parachévement'),
        ('Terra-DP', 'Demande de prix 05 Terrasement'),
        ('Terra-CP', 'Comparatif 05 Terrasement'),
        ('GO-DP', 'Demande de prix 07 Gros-oeuvre'),
        ('GO-DP', 'Comparatif 07 Gros-oeuvre'),
        ('Chassis-DP', 'Demande de prix 11 Chassis'),
        ('Chassis-CP', 'Comparatif 11 Chassis'),
        ('Char-DP', 'Demande de prix 13 Charpente'),
        ('Char-CP', 'Comparatif 13 Charpente'),
        ('Toiture-DP', 'Demande de prix 15 Toiture'),
        ('Toiture-CP', 'Comparatif 15 Toiture'),
        ('Budget-DP', 'Budget estimatif'),
        ('Budget-CP', 'Budget définitif'),
        ('GC-DP', 'Demande de prix Garde corps'),
        ('GC-CP', 'Comparatif Garde corps'),
        ('Abords-DP', 'Demande de prix Abords'),
        ('Abords-CP', 'Comparatif Abords')
    )

    inputName = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class': 'form-control'}),
        required=True
    )

    inputEntite = forms.CharField(
        widget=forms.Select(choices=Entite_choices, attrs={'class': "form-control selectCustom"}),
        required=True
    )

    inputDebut = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True
    )

    inputObjectif = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True
    )



class PhaseForm(forms.Form):

    State_choices = (
        ('0', 'Pas commencé'),
        ('1', 'En cours'),
        ('2', 'Fini')
    )
    inputName = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class': 'form-control'}),
        required=True
    )

    inputType = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class': 'form-control'}),
        required=True
    )

    inputState = forms.CharField(
        widget=forms.Select(choices=State_choices, attrs={'class': "form-control selectCustom"}),
        required=True
    )

    inputDebut = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True
    )
    inputObjectif = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True
    )
