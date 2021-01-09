from rest_framework import serializers
from .models import Schools


class SchoolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schools
        fields = (
            "ASC_COLLEGE_ID", "ORG_FULL_NAME", "CB_REGION_CD",
            "VISIT_STATE_CD", "MAIL_CITY", "GRAD_6_YR_RATE_PCT",
            "ENROLL_UG_TOTAL_DEG", "UNDERGRAD_GRADE_CD", "FRESH_SAT_I_V_25_PCTL",
            "FRESH_SAT_I_V_75_PCTL", "FRESH_SAT_I_M_25_PCTL", "FRESH_SAT_I_M_75_PCTL"
        )
