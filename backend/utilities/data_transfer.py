#!/usr/bin/env python3

from problem.models import Problem
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

# USAGE EXAMPLE:
# (venv) ubuntu@VM1282-Master:~/soft_eng/Verilog-OJ/backend$ python3 manage.py shell
# Python 3.6.9 (default, Jul 17 2020, 12:50:27) 
# [GCC 8.4.0] on linux
# Type "help", "copyright", "credits" or "license" for more information.
# (InteractiveConsole)
# >>> from utilities.data_transfer import export_problems
# >>> export_problems("a.json")

# Below are serializers that serialize just like their models

class ProblemFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'

def export_problems(path):
    s = ProblemFullSerializer(Problem.objects.all(), many=True)
    json = JSONRenderer().render(s.data)

    with open(path, "wb") as f:
        f.write(json)