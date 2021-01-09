import json

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F
from rest_framework import generics
from rest_framework.exceptions import NotFound

from .models import Schools
from .serializers import SchoolsSerializer


# http://127.0.0.1:8000/api/v1/schools/
class ListSchoolsView(generics.ListAPIView):

    serializer_class = SchoolsSerializer

    def get_queryset(self):

        FORMAT = self.request.query_params.get("format", None)
        LIMIT = self.request.query_params.get("limit", None)

        if(FORMAT or LIMIT):
            queryset = Schools.objects.all()
            if LIMIT:
                queryset = queryset[:int(LIMIT)]
            return queryset
        elif(self.request.query_params):
            raise NotFound()
        else:
            return Schools.objects.all()

    # lookup_url_kwarg = "version"
    #
    # def get_queryset(self):
    #     version = self.kwargs['version']
    #     if (version=="v1"):
    #         return Schools.objects.all()



# http://127.0.0.1:8000/api/v1/filter/?cb_region_cd=<>
# http://127.0.0.1:8000/api/v1/filter/?visit_state_cd=<>
class ListFilteredSchoolsView(generics.ListAPIView):
    serializer_class = SchoolsSerializer

    def get_queryset(self):

        """ Raise NotFound exception when no filter parameter is passed to /filter/ URL"""
        if (len(self.request.query_params)==0):
            raise NotFound()

        queryset = Schools.objects.all()

        LIMIT = self.request.query_params.get('limit', None)
        CB_REGION_CD = self.request.query_params.get('cb_region_cd', None)
        MAIL_CITY = self.request.query_params.get('mail_city', None)
        VISIT_STATE_CD = self.request.query_params.get('visit_state_cd', None)
        UNDERGRAD_GRADE_CD = self.request.query_params.get('undergrad_grade_cd', None)
        # UNDERGRAD_GRADE_CD = self.request.GET['undergrad_grade_cd']
        ENROLL_UG_TOTAL_DEG = self.request.query_params.get('enroll_ug_total_dg', None)

        MATCH_TYPE = self.request.query_params.get('match_type', None)
        SCORE = self.request.query_params.get('score', None)

        if MATCH_TYPE is not None and SCORE is not None:
            if (MATCH_TYPE=="reach"):
                #queryset = Schools.objects.raw('SELECT * FROM firstApis_Schools WHERE FRESH_SAT_I_M_25_PCTL + FRESH_SAT_I_V_25_PCTL > %s', [SCORE])
                queryset = queryset.filter(FRESH_SAT_I_M_25_PCTL__gt = int(SCORE) - F('FRESH_SAT_I_V_25_PCTL'))
            elif (MATCH_TYPE=="match"):
                queryset = queryset.filter(FRESH_SAT_I_M_25_PCTL__lt = int(SCORE) - F('FRESH_SAT_I_V_25_PCTL')).filter(FRESH_SAT_I_M_75_PCTL__gt = int(SCORE) - F('FRESH_SAT_I_V_75_PCTL'))
            elif (MATCH_TYPE=="safety"):
                queryset = queryset.filter(FRESH_SAT_I_M_75_PCTL__lt = int(SCORE) - F('FRESH_SAT_I_V_75_PCTL'))
            else:
                pass
        elif CB_REGION_CD is not None:
            queryset = queryset.filter(CB_REGION_CD=CB_REGION_CD)
        elif MAIL_CITY is not None:
            queryset = queryset.filter(MAIL_CITY=MAIL_CITY)
        elif VISIT_STATE_CD is not None:
            queryset = queryset.filter(VISIT_STATE_CD=VISIT_STATE_CD)
        elif UNDERGRAD_GRADE_CD is not None:
            queryset = queryset.filter(UNDERGRAD_GRADE_CD=UNDERGRAD_GRADE_CD)
        elif ENROLL_UG_TOTAL_DEG is not None:
            if (ENROLL_UG_TOTAL_DEG=="small"):
                queryset = queryset.filter(ENROLL_UG_TOTAL_DEG__range=(0, 2001))
            elif (ENROLL_UG_TOTAL_DEG=="medium"):
                queryset = queryset.filter(ENROLL_UG_TOTAL_DEG__range=(2001, 15001))
            elif (ENROLL_UG_TOTAL_DEG=="large"):
                queryset = queryset.filter(ENROLL_UG_TOTAL_DEG__gte=15001)
            else:
                raise NotFound()
        else:
            raise NotFound()

        if LIMIT:
            queryset = queryset[:int(LIMIT)]
        return queryset


def addDataToDB(request, *args, **kwargs):

    import csv

    with open('./colleges.csv','rt', errors='ignore') as f:
        data = csv.reader(f)
        i=0
        for row in data:
            if(i==0):
                i+=1
                # print("Columns Are Present In This Row")
            else:
                try:
                    newEntry = Schools()
                    newEntry.ASC_COLLEGE_ID = row[1]
                    newEntry.ORG_FULL_NAME = row[2]
                    newEntry.CB_REGION_CD = row[16]
                    newEntry.MAIL_CITY = row[19]
                    newEntry.VISIT_STATE_CD = row[25]
                    newEntry.GRAD_6_YR_RATE_PCT = row[460]
                    newEntry.UNDERGRAD_GRADE_CD = row[109]

                    try:
                        newEntry.ENROLL_UG_TOTAL_DEG = int(row[679])
                    except ValueError:
                        newEntry.ENROLL_UG_TOTAL_DEG = None

                    try:
                        newEntry.FRESH_SAT_I_V_25_PCTL = int(row[178])
                    except ValueError:
                        newEntry.FRESH_SAT_I_V_25_PCTL = None
                    try:
                        newEntry.FRESH_SAT_I_V_75_PCTL = int(row[179])
                    except ValueError:
                        newEntry.FRESH_SAT_I_V_75_PCTL = None
                    try:
                        newEntry.FRESH_SAT_I_M_25_PCTL = int(row[180])
                    except ValueError:
                        newEntry.FRESH_SAT_I_M_25_PCTL = None
                    try:
                        newEntry.FRESH_SAT_I_M_75_PCTL = int(row[181])
                    except ValueError:
                        newEntry.FRESH_SAT_I_M_75_PCTL = None

                    newEntry.save()
                    i+=1
                except Exception as e:
                    print("ERROR:", e)

        return HttpResponse(json.dumps({'success': True, 'total_colleges_added': i}),content_type="application/json")



# class ListFilteredSchoolsView(generics.ListAPIView):
#
#     serializer_class = SchoolsSerializer
#
#     def get_queryset(self):
#         column = self.kwargs['column']
#         print("Column:", column)
#         if (column=="CB_REGION_CD"):
#             return Schools.objects.filter()
