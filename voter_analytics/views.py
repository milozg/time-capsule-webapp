from django.shortcuts import render
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from . models import Voter
import plotly
import plotly.graph_objs as go

# Create your views here.

class VotersListView(ListView):
    '''View to display Voters'''
    model = Voter
    template_name = 'voter_analytics/voters.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_url_fields(self):
        fields = ""
        for f in self.request.GET:
            fields += f
            fields += "="
            fields += str(self.request.GET[f])
            fields += "&"
        print(fields)
        return fields

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['years'] = range(1920,2005)
        context['fields_url'] = self.get_url_fields()
        return context
    
    def get_queryset(self):
        voters = super().get_queryset()

        if 'affiliation' in self.request.GET:
            affiliation = self.request.GET['affiliation']
            if affiliation:
                voters = voters.filter(affiliation=affiliation)

        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                voter_score = int(voter_score)
                voters = voters.filter(voter_score=voter_score)

        if 'min_birth' in self.request.GET:
            min_birth = self.request.GET['min_birth']
            if min_birth:
                min_birth = int(min_birth)
                voters = voters.filter(dob__year__gte=min_birth)

        if 'max_birth' in self.request.GET:
            max_birth = self.request.GET['max_birth']
            if max_birth:
                max_birth = int(max_birth)
                voters = voters.filter(dob__year__lte=max_birth)

        if 'v20state' in self.request.GET:
            voters = voters.filter(v20state="TRUE")
        if 'v21town' in self.request.GET:
            voters = voters.filter(v21town="TRUE")
        if 'v21primary' in self.request.GET:
            voters = voters.filter(v21primary="TRUE")
        if 'v22general' in self.request.GET:
            voters = voters.filter(v22general="TRUE")
        if 'v23town' in self.request.GET:
            voters = voters.filter(v23town="TRUE")

        return voters
    
class VoterDetailView(DetailView):
    '''View class to handle request to show details of a single voter'''
    model = Voter
    template_name = 'voter_analytics/voter.html'
    context_object_name = 'v'

class GraphsView(ListView):
    '''A class to handle the request to display the graphs page'''
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filter the data by the form fields
        voters = self.get_queryset()

        if 'affiliation' in self.request.GET:
            affiliation = self.request.GET['affiliation']
            if affiliation:
                voters = voters.filter(affiliation=affiliation)

        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                voter_score = int(voter_score)
                voters = voters.filter(voter_score=voter_score)

        if 'min_birth' in self.request.GET:
            min_birth = self.request.GET['min_birth']
            if min_birth:
                min_birth = int(min_birth)
                voters = voters.filter(dob__year__gte=min_birth)

        if 'max_birth' in self.request.GET:
            max_birth = self.request.GET['max_birth']
            if max_birth:
                max_birth = int(max_birth)
                voters = voters.filter(dob__year__lte=max_birth)

        if 'v20state' in self.request.GET:
            voters = voters.filter(v20state="TRUE")
        if 'v21town' in self.request.GET:
            voters = voters.filter(v21town="TRUE")
        if 'v21primary' in self.request.GET:
            voters = voters.filter(v21primary="TRUE")
        if 'v22general' in self.request.GET:
            voters = voters.filter(v22general="TRUE")
        if 'v23town' in self.request.GET:
            voters = voters.filter(v23town="TRUE")

        # Distribution by birth year
        x = []
        y = []
        for i in range(1920,2005):
            x.append(str(i))
            y.append(len(voters.filter(dob__year=i)))
        fig = go.Bar(x=x, y=y)
        title_text = "Voter Distribution by Year of Birth"
        graph_div_birth_year = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, auto_open=False, 
                                         output_type="div",
                                         )
        context['graph_div_birth_year'] = graph_div_birth_year


        # Distribution by party affiliation
        x = list(voters.values_list('affiliation', flat=True).distinct())
        x = x[:10]
        y = []
        for a in x:
            y.append(len(voters.filter(affiliation=a)))
        fig = go.Pie(labels=x, values=y) 
        title_text = "Voter Distribution by Party Affiliation"
        graph_div_affiliation = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")
        context['graph_div_affiliation'] = graph_div_affiliation

        #Vote count by election
        x = ["v20state", "v21town", "v21primary", "v22general", "v23town"]
        y = []
        y.append(len(voters.filter(v20state="TRUE")))
        y.append(len(voters.filter(v21town="TRUE")))
        y.append(len(voters.filter(v21primary="TRUE")))
        y.append(len(voters.filter(v22general="TRUE")))
        y.append(len(voters.filter(v23town="TRUE")))
        fig = go.Bar(x=x, y=y)
        title_text = "Voter Count by Election"
        graph_div_turnout = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, auto_open=False, 
                                         output_type="div",
                                         )
        context['graph_div_turnout'] = graph_div_turnout

        context['years'] = range(1920,2005)

        return context

