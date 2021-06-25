import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from Achat.models import Responsable, User, Chantier, Modification, Phase
from . import forms
from datetime import datetime, timedelta, date
from django.db import connection
from decimal import Decimal
from Achat.timeline import Timeline

def CreateGeneriquePhases(chantier):
    PhaseType = forms.ChantierForm.Type_choices
    for type in PhaseType:
        phase = Phase.objects.get_or_create(
            Name=type[1],
            Type=type[0],
            State=0,
            num=0,
            id_chantier=chantier)[0]
        phase.save()

def New(request):
    if request.session.get('connected') == 'true':
        year = request.session['year']
        month = request.session['month']
        day = request.session['day']
        phase_list = Phase.objects.order_by('Name')
        PhaseType = [
            {"type": "Para", "nom": "Parachévement"},
            {"type": "Toiture", "nom": "Toiture"},
            {"type": "GO", "nom": "Gros-oeuvre"},
            {"type": "Chassis", "nom": "Chassis"}]
        if request.method == 'POST':
            form = forms.ChantierForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['inputName']
                entite = form.cleaned_data['inputEntite']
                debut = form.cleaned_data['inputDebut']
                objectif = form.cleaned_data['inputObjectif']
                chantier = Chantier.objects.get_or_create(
                    Name=name,
                    Date_debut=debut,
                    Date_fin=objectif,
                    Entite=entite)[0]
                id = str(chantier.id)
                chantier.save()
                CreateGeneriquePhases(chantier)
                return redirect('../Modif/' + id)
        form_list = forms.ChantierForm()
        context = {
            'year': year,
            'month': month,
            'day': day,
            'form': form_list,
            'PhaseList': phase_list,
            'connected': request.session.get('connected'),
            'phaseType': PhaseType,
        }
        return render(request, 'chantierNew.html', context)
    else:
        return redirect('/Home')

def PhasesPlan(chant_id):
    return Phase.objects.filter(id_chantier=chant_id).exclude(State=2).exclude(Date_debut=None)

def PhasesNonPlan(chant_id):
    return Phase.objects.filter(id_chantier=chant_id, Date_debut=None)

def PhaseFinish(chant_id):
    return Phase.objects.filter(id_chantier=chant_id, State=2)

def Getschedule(begin, chant_id):
    phases = Phase.objects.filter(id_chantier=chant_id).exclude(Date_debut=None).order_by('Name')
    timeline = Timeline(begin, 1)
    for phase in phases:
        timeline.addTask(phase)
    return timeline

def Modif(request, chant_id):
    if request.session.get('connected') == 'true':
        year = request.session['year']
        month = request.session['month']
        day = request.session['day']
        begin = date(int(year), int(month), int(day))
        weekList = Timeline(begin).WeekList
        PhaseType = forms.ChantierForm.Type_choices
        chantier = Chantier.objects.get(pk=chant_id)
        phasesPlan = PhasesPlan(chant_id)
        phasesNonPlan = PhasesNonPlan(chant_id)
        phasesFinish = PhaseFinish(chant_id)
        Name = chantier.Name
        Entite = chantier.Entite
        Debut = chantier.Date_debut
        Objectif = chantier.Date_fin
        if request.method == 'POST':
            form = forms.ChantierForm(request.POST)
            if form.is_valid():
                Name = form.cleaned_data['inputName']
                Entite = form.cleaned_data['inputEntite']
                Debut = form.cleaned_data['inputDebut']
                Objectif = form.cleaned_data['inputObjectif']
                chantier.Name = Name
                chantier.Entite = Entite
                chantier.Date_debut = Debut
                chantier.Date_fin = Objectif
                chantier.save()
                return redirect('/TimelineChant/' + year + "/" + month + "/" + day)

        form_list = forms.ChantierForm(initial={
            'inputName': Name,
            'inputEntite': Entite,
            'inputDebut': Debut,
            'inputObjectif': Objectif,
            'PhasePlan': phasesPlan,
        })

        context = {
            'year': year,
            'month': month,
            'day': day,
            'form': form_list,
            'chantier': chantier,
            'PhasePlan': phasesPlan,
            'PhaseNonPlan': phasesNonPlan,
            'PhaseFinish': phasesFinish,
            'WeekList': weekList,
            'schedule': Getschedule(begin, chant_id),
            'connected': request.session.get('connected'),
        }
        return render(request, 'chantier.html', context)
    else:
        return redirect('/Home')

def Delete(request, chant_id):
    if request.session.get('connected') == 'true':
        context = {
            'id_chant': chant_id
        }
        if request.method == 'POST':
            chant = Chantier.objects.get(pk=chant_id)
            chant.delete()
            year = request.session['year']
            month = request.session['month']
            day = request.session['day']
            return redirect('/TimelineChant/' + year + "/" + month + "/" + day)
        return render(request, 'DeleteChantier.html', context)
    else:
        return redirect('/Home')