import axios from "axios";
import { useState } from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// Register chart components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const uploadFile = (e) => {
    const formData = new FormData();
    formData.append("file", e.target.files[0]);

    setLoading(true);

    axios
      .post("http://127.0.0.1:8000/api/upload/", formData)
      .then((res) => {
        setData(res.data);
        setLoading(false);
      })
      .catch(() => {
        alert("Upload failed");
        setLoading(false);
      });
  };

  const chartData =
    data && {
      labels: Object.keys(data.type_distribution),
      datasets: [
        {
          label: "Equipment Count",
          data: Object.values(data.type_distribution),
          backgroundColor: "rgba(54, 162, 235, 0.6)",
        },
      ],
    };

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        <h1 style={styles.title}>
          Chemical Equipment Parameter Visualizer
        </h1>
        <p style={styles.subtitle}>
          Upload a CSV file to analyze chemical equipment parameters
        </p>

        {/* Upload Box */}
        <div style={styles.uploadBox}>
          <input type="file" onChange={uploadFile} />
          {loading && <p style={{ marginTop: 10 }}>Uploading...</p>}
        </div>

        {data && (
          <>
          
            {/* Summary Cards */}
            <div style={styles.cards}>
  <div style={{ ...styles.card, background: "#e8f1fd" }}>
    <h3>Total Equipment</h3>
    <p>{data.total}</p>
  </div>

  <div style={{ ...styles.card, background: "#e9f7ef" }}>
    <h3>Avg Flowrate</h3>
    <p>{data.avg_flowrate.toFixed(2)}</p>
  </div>

  <div style={{ ...styles.card, background: "#fff4e6" }}>
    <h3>Avg Pressure</h3>
    <p>{data.avg_pressure.toFixed(2)}</p>
  </div>

  <div style={{ ...styles.card, background: "#fceef3" }}>
    <h3>Avg Temperature</h3>
    <p>{data.avg_temperature.toFixed(2)}</p>
  </div>
</div>

            {/* Chart Section */}
            <div style={styles.chartBox}>
              <h2>Equipment Type Distribution</h2>
              <Bar data={chartData} />
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;

/* ======================
   STYLES
====================== */
const styles = {
  page: {
    minHeight: "100vh",
    background: "#f4f6f8",
    display: "flex",
    justifyContent: "center",
    paddingTop: "40px",
    fontFamily: "Segoe UI, sans-serif",
  },
  container: {
    width: "90%",
    maxWidth: "1000px",
    background: "#ffffff",
    padding: "30px",
    borderRadius: "12px",
    boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
  },
  title: {
    textAlign: "center",
    marginBottom: "5px",
  },
  subtitle: {
    textAlign: "center",
    color: "#666",
    marginBottom: "30px",
  },
  uploadBox: {
    border: "2px dashed #aaa",
    padding: "20px",
    textAlign: "center",
    borderRadius: "8px",
    marginBottom: "30px",
    background: "#fafafa",
  },
  cards: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
    gap: "20px",
    marginBottom: "40px",
  },
  card: {
  padding: "20px",
  borderRadius: "12px",
  textAlign: "center",
  boxShadow: "0 6px 14px rgba(0,0,0,0.06)",
  fontWeight: "500",
},
  chartBox: {
    padding: "20px",
    borderRadius: "10px",
    background: "#f9fbfd",
  },
};