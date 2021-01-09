from django.db import models

# Create your models here.
class Schools(models.Model):

    ASC_COLLEGE_ID = models.CharField(max_length=25, null=False)
    ORG_FULL_NAME = models.CharField(max_length=255, null=False)
    CB_REGION_CD = models.CharField(max_length=25, default="NaN")
    VISIT_STATE_CD = models.CharField(max_length=25, default="NaN")
    MAIL_CITY = models.CharField(max_length=25, null=True)
    GRAD_6_YR_RATE_PCT = models.CharField(max_length=5, blank=True, null=True)
    ENROLL_UG_TOTAL_DEG = models.IntegerField(null=True, blank=True)
    UNDERGRAD_GRADE_CD = models.CharField(max_length=5, blank=True, null=True)
    FRESH_SAT_I_V_25_PCTL = models.IntegerField(null=True, blank=True)
    FRESH_SAT_I_V_75_PCTL = models.IntegerField(null=True, blank=True)
    FRESH_SAT_I_M_25_PCTL = models.IntegerField(null=True, blank=True)
    FRESH_SAT_I_M_75_PCTL = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return "{} - {}".format(self.ASC_COLLEGE_ID, self.ORG_FULL_NAME)
