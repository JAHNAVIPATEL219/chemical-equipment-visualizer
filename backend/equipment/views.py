from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import csv, io

@csrf_exempt
@api_view(["POST"])
def upload_csv(request):
    if "file" not in request.FILES:
        return Response({"error": "No file uploaded"}, status=400)

    file = request.FILES["file"]
    data = file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(data))

    total = 0
    flowrates = []
    pressures = []
    temperatures = []
    type_distribution = {}

    for row in reader:
        total += 1
        flowrates.append(float(row["flowrate"]))
        pressures.append(float(row["pressure"]))
        temperatures.append(float(row["temperature"]))
        t = row["type"]
        type_distribution[t] = type_distribution.get(t, 0) + 1

    return Response({
        "total": total,
        "avg_flowrate": sum(flowrates) / len(flowrates),
        "avg_pressure": sum(pressures) / len(pressures),
        "avg_temperature": sum(temperatures) / len(temperatures),
        "type_distribution": type_distribution
    })
