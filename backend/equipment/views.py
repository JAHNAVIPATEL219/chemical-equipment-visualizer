from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
@api_view(['POST'])
def upload_csv(request):
    file = request.FILES['file']   # uploaded file
    df = pd.read_csv(file)

    summary = {
        "total": len(df),
        "avg_flowrate": df["Flowrate"].mean(),
        "avg_pressure": df["Pressure"].mean(),
        "avg_temperature": df["Temperature"].mean(),
        "type_distribution": df["Type"].value_counts().to_dict()
    }

    return Response(summary)