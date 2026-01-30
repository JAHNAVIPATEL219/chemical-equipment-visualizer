from rest_framework.decorators import api_view
from rest_framework.response import Response
import csv, io

@api_view(["POST"])
def upload_csv(request):
    file = request.FILES.get("file")
    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    data = file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(data))

    total = 0
    flowrates = []
    pressures = []
    temperatures = []
    type_distribution = {}

    for row in reader:
        total += 1

        # 👇 MATCHING YOUR CSV COLUMN NAMES
        flowrates.append(float(row["Flowrate"]))
        pressures.append(float(row["Pressure"]))
        temperatures.append(float(row["Temperature"]))

        eq_type = row["Type"]
        type_distribution[eq_type] = type_distribution.get(eq_type, 0) + 1

    return Response({
        "total": total,
        "avg_flowrate": sum(flowrates) / len(flowrates),
        "avg_pressure": sum(pressures) / len(pressures),
        "avg_temperature": sum(temperatures) / len(temperatures),
        "type_distribution": type_distribution
    })
