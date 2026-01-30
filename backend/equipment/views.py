from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import pandas as pd

@csrf_exempt
@api_view(['POST'])
def upload_csv(request):
    if 'file' not in request.FILES:
        return Response(
            {"error": "No file uploaded"},
            status=status.HTTP_400_BAD_REQUEST
        )

    file = request.FILES['file']

    try:
        df = pd.read_csv(file)

        result = {
            "total": len(df),
            "avg_flowrate": float(df["Flowrate"].mean()),
            "avg_pressure": float(df["Pressure"].mean()),
            "avg_temperature": float(df["Temperature"].mean()),
            "type_distribution": df["Type"].value_counts().to_dict()
        }

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
