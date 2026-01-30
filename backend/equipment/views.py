from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import csv, io

@csrf_exempt
@api_view(["POST"])
def upload_csv(request):
    file = request.FILES.get("file")

    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    data = file.read().decode("utf-8")
    io_string = io.StringIO(data)
    reader = csv.DictReader(io_string)

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

        eq_type = row["type"]
        type_distribution[eq_type] = type_distribution.get(eq_type, 0) + 1

    return Response({
        "total": total,
        "avg_flowrate": sum(flowrates) / len(flowrates),
        "avg_pressure": sum(pressures) / len(pressures),
        "avg_temperature": sum(temperatures) / len(temperatures),
        "type_distribution": type_distribution
    })
