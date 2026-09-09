import { useState, useEffect, useRef } from "react";
import "./App.css";

/* ============================================================
   HELPERS
============================================================ */

/**
 * Returns a CSS class for a signal card based on the signal value
 * and the "good" direction.
 *
 * @param {number|string} value - numeric value or string like "HIGH"/"LOW"
 * @param {"higher_is_better"|"lower_is_better"|"string"} mode
 */
function getSignalClass(value, mode) {
  if (mode === "string") {
    if (value === "LOW") return "sig-good";
    if (value === "MEDIUM") return "sig-warn";
    if (value === "HIGH") return "sig-danger";
    if (value === "PASS" || value === "CONSISTENT") return "sig-good";
    if (value === "INCONSISTENT") return "sig-warn";
    return "";
  }

  const n = parseFloat(value);
  if (isNaN(n)) return "";

  if (mode === "higher_is_better") {
    if (n >= 70) return "sig-good";
    if (n >= 40) return "sig-warn";
    return "sig-danger";
  }

  // lower_is_better (risk score, ELA etc.)
  if (n <= 35) return "sig-good";
  if (n <= 65) return "sig-warn";
  return "sig-danger";
}

/* ============================================================
   ANIMATED SCORE RING (SVG)
============================================================ */

function ScoreRing({ score }) {
  const radius = 45;
  const circumference = 2 * Math.PI * radius; // ~283
  const [dashOffset, setDashOffset] = useState(circumference);

  useEffect(() => {
    // Delay slightly so the transition plays on mount
    const id = setTimeout(() => {
      const filled = ((score / 100) * circumference);
      setDashOffset(circumference - filled);
    }, 120);
    return () => clearTimeout(id);
  }, [score, circumference]);

  return (
    <div className="score-circle">
      <svg viewBox="0 0 100 100" width="110" height="110">
        <circle
          className="ring-track"
          cx="50"
          cy="50"
          r={radius}
        />
        <circle
          className="ring-fill"
          cx="50"
          cy="50"
          r={radius}
          strokeDasharray={circumference}
          strokeDashoffset={dashOffset}
        />
      </svg>

      <div className="score-inner">
        <strong>{score}</strong>
        <span>/100</span>
      </div>
    </div>
  );
}

/* ============================================================
   MAIN APP
============================================================ */

function App() {
  const [documentFile, setDocumentFile] = useState(null);
  const [referenceFile, setReferenceFile] = useState(null);

  const [documentPreview, setDocumentPreview] = useState("");
  const [referencePreview, setReferencePreview] = useState("");

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [processingStep, setProcessingStep] = useState(0);

  // Drag-over states
  const [docDragOver, setDocDragOver] = useState(false);
  const [refDragOver, setRefDragOver] = useState(false);

  const resultRef = useRef(null);

  const steps = [
    {
      number: 1,
      title: "Document Upload",
      description: "Reading uploaded document",
    },
    {
      number: 2,
      title: "OCR & Data Extraction",
      description: "Extracting text and identity fields",
    },
    {
      number: 3,
      title: "Document Analysis",
      description: "Checking image quality and structure",
    },
    {
      number: 4,
      title: "Tampering Detection",
      description: "Analyzing possible image manipulation",
    },
    {
      number: 5,
      title: "Face Verification",
      description: "Comparing document and reference face",
    },
    {
      number: 6,
      title: "Risk Assessment",
      description: "Calculating overall screening risk",
    },
  ];

  /* ---------- file helpers ---------- */

  const applyDocumentFile = (file) => {
    if (!file) return;
    setDocumentFile(file);
    setDocumentPreview(URL.createObjectURL(file));
    setResult(null);
    setError("");
  };

  const applyReferenceFile = (file) => {
    if (!file) return;
    setReferenceFile(file);
    setReferencePreview(URL.createObjectURL(file));
    setResult(null);
    setError("");
  };

  const handleDocumentChange = (event) => {
    applyDocumentFile(event.target.files[0]);
  };

  const handleReferenceChange = (event) => {
    applyReferenceFile(event.target.files[0]);
  };

  /* ---------- drag & drop ---------- */

  const handleDocDragOver = (e) => {
    e.preventDefault();
    setDocDragOver(true);
  };
  const handleDocDragLeave = () => setDocDragOver(false);
  const handleDocDrop = (e) => {
    e.preventDefault();
    setDocDragOver(false);
    applyDocumentFile(e.dataTransfer.files[0]);
  };

  const handleRefDragOver = (e) => {
    e.preventDefault();
    setRefDragOver(true);
  };
  const handleRefDragLeave = () => setRefDragOver(false);
  const handleRefDrop = (e) => {
    e.preventDefault();
    setRefDragOver(false);
    applyReferenceFile(e.dataTransfer.files[0]);
  };

  /* ---------- analysis ---------- */

  const analyzeDocument = async () => {
    if (!documentFile || !referenceFile) {
      setError("Please upload both the document and reference face image.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);
    setProcessingStep(1);

    const timers = [];

    for (let i = 2; i <= 6; i++) {
      timers.push(
        setTimeout(() => {
          setProcessingStep(i);
        }, (i - 1) * 500)
      );
    }

    const formData = new FormData();
    formData.append("document_file", documentFile);
    formData.append("reference_file", referenceFile);

    try {
      const backendUrl = import.meta.env.VITE_API_URL || "https://fake-identity-screening.onrender.com";
      const response = await fetch(`${backendUrl}/ocr`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Backend request failed.");
      }

      const data = await response.json();

      timers.forEach(clearTimeout);
      setProcessingStep(7);

      setTimeout(() => {
        setResult(data);
        setLoading(false);
        // Scroll to results
        setTimeout(() => {
          resultRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
        }, 100);
      }, 500);
    } catch (err) {
      timers.forEach(clearTimeout);
      setLoading(false);
      setProcessingStep(0);
      setError(
        "Unable to connect to backend. Please make sure the FastAPI server is running on port 8000."
      );
    }
  };

  /* ---------- report download ---------- */

  const downloadReport = () => {
    if (!result) return;

    const risk = result.risk_assessment;
    const face = result.face_verification;
    const tampering = result.tampering_analysis;
    const consistency = result.data_consistency;

    const tamperingSignal =
      tampering.ela_score > 10
        ? "HIGH"
        : tampering.ela_score > 5
        ? "MEDIUM"
        : "LOW";

    const report = `
FAKE IDENTITY & DOCUMENT SCREENING SYSTEM
==========================================

SCREENING REPORT — Generated: ${new Date().toLocaleString()}

DOCUMENT
--------
Document: ${result.document_filename}
Reference: ${result.reference_filename}

OVERALL RESULT
--------------
Risk Score: ${risk.risk_score}/100
Risk Level: ${risk.risk_level}
Recommendation: ${risk.recommendation}

KEY SCREENING SIGNALS
---------------------
OCR Confidence: ${result.ocr_confidence}%

Face Similarity: ${
      face.status === "success" ? `${face.similarity_score}%` : "N/A"
    }

Face Verification: ${
      face.status === "success" ? face.verification : "UNAVAILABLE"
    }

Tampering Signal: ${tamperingSignal}
ELA Score: ${tampering.ela_score}

Data Consistency: ${consistency.status}

RISK BREAKDOWN
--------------
Image Quality:       ${risk.risk_breakdown.image_quality}/10
Tampering Detection: ${risk.risk_breakdown.tampering_detection}/30
Field Validation:    ${risk.risk_breakdown.field_validation}/20
Face Verification:   ${risk.risk_breakdown.face_verification}/30
Data Consistency:    ${risk.risk_breakdown.data_consistency}/10

EXTRACTED INFORMATION
---------------------
Name: ${result.fields.name || "Not detected"}
Date of Birth: ${result.fields.date_of_birth || "Not detected"}
Gender: ${result.fields.gender || "Not detected"}
Document Number: ${result.fields.document_number || "Not detected"}

DATA CONSISTENCY ISSUES
-----------------------
${
  consistency.issues.length > 0
    ? consistency.issues.map((issue) => `- ${issue}`).join("\n")
    : "No consistency issues detected"
}

RISK REASONS
------------
${
  risk.reasons.length > 0
    ? risk.reasons.map((reason) => `- ${reason}`).join("\n")
    : "No major anomaly detected"
}

DISCLAIMER
----------
This is a prototype-based preliminary screening system.
The result is not a legal determination of document authenticity
and should not be treated as final identity verification.

Manual verification is recommended for high-risk cases.

==========================================
END OF REPORT
`;

    const blob = new Blob([report], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `screening-report-${Date.now()}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  /* ---------- derived values ---------- */

  const getRiskClass = () => {
    if (!result) return "";
    return result.risk_assessment.risk_level.toLowerCase();
  };

  const getRiskMessage = () => {
    if (!result) return "";
    const level = result.risk_assessment.risk_level;
    if (level === "HIGH")
      return "Multiple suspicious signals detected. Manual verification required.";
    if (level === "MEDIUM")
      return "Some anomalies were detected. Further verification is recommended.";
    return "No major anomaly detected across the analyzed screening signals.";
  };

  const getTamperingLabel = () => {
    if (!result) return "";
    const ela = result.tampering_analysis.ela_score;
    return ela > 10 ? "HIGH" : ela > 5 ? "MEDIUM" : "LOW";
  };

  /* ============================================================
     RENDER
  ============================================================ */

  return (
    <div className="app">
      {/* ── HEADER ── */}
      <header className="header">
        <div className="header-inner">
          <div className="brand">
            <div className="brand-icon">AI</div>

            <div>
              <h1>Document Screening System</h1>
              <span>AI-Powered Identity Risk Analysis</span>
            </div>
          </div>

          <div className="header-status">
            <span className="status-dot"></span>
            Prototype Active
          </div>
        </div>
      </header>

      <main className="container">
        {/* ── HERO ── */}
        <section className="hero">
          <span className="hero-label">PRELIMINARY SCREENING</span>

          <h2>
            Detect suspicious identity documents
            <br />
            using multiple AI-assisted signals.
          </h2>

          <p>
            Upload a document and reference face to perform OCR,
            document analysis, tampering checks, face comparison
            and risk assessment — all in one go.
          </p>
        </section>

        {/* ── UPLOAD GRID ── */}
        <section className="upload-grid">
          {/* Document Upload */}
          <div className="upload-card">
            <div className="upload-card-header">
              <div>
                <span className="section-label">STEP 01</span>
                <h3>Identity Document</h3>
              </div>
              <span className="upload-icon">DOC</span>
            </div>

            <label
              className={`upload-area${docDragOver ? " drag-over" : ""}`}
              onDragOver={handleDocDragOver}
              onDragLeave={handleDocDragLeave}
              onDrop={handleDocDrop}
            >
              {documentPreview ? (
                <img
                  src={documentPreview}
                  alt="Document preview"
                  className="upload-preview"
                />
              ) : (
                <>
                  <div className="upload-placeholder-icon">↑</div>
                  <strong>Upload or drag &amp; drop</strong>
                  <span>JPG, JPEG or PNG</span>
                </>
              )}

              <input
                type="file"
                accept="image/*"
                onChange={handleDocumentChange}
              />
            </label>

            {documentFile && (
              <div className="file-name">{documentFile.name}</div>
            )}
          </div>

          {/* Reference Face Upload */}
          <div className="upload-card">
            <div className="upload-card-header">
              <div>
                <span className="section-label">STEP 02</span>
                <h3>Reference Face</h3>
              </div>
              <span className="upload-icon">FACE</span>
            </div>

            <label
              className={`upload-area${refDragOver ? " drag-over" : ""}`}
              onDragOver={handleRefDragOver}
              onDragLeave={handleRefDragLeave}
              onDrop={handleRefDrop}
            >
              {referencePreview ? (
                <img
                  src={referencePreview}
                  alt="Reference preview"
                  className="upload-preview"
                />
              ) : (
                <>
                  <div className="upload-placeholder-icon">↑</div>
                  <strong>Upload or drag &amp; drop</strong>
                  <span>Clear face image recommended</span>
                </>
              )}

              <input
                type="file"
                accept="image/*"
                onChange={handleReferenceChange}
              />
            </label>

            {referenceFile && (
              <div className="file-name">{referenceFile.name}</div>
            )}
          </div>
        </section>

        {/* ── ANALYZE BUTTON ── */}
        <button
          className="analyze-button"
          onClick={analyzeDocument}
          disabled={loading}
        >
          {loading ? "Analyzing Document…" : "Analyze Document"}
        </button>

        {/* ── PROCESSING STEPS ── */}
        {loading && (
          <section className="processing-card">
            <div className="processing-header">
              <div>
                <span>ANALYSIS IN PROGRESS</span>
                <h3>Processing Screening Signals</h3>
              </div>
              <div className="processing-spinner" />
            </div>

            <div className="processing-steps">
              {steps.map((step) => (
                <div
                  key={step.number}
                  className={
                    processingStep > step.number
                      ? "step completed"
                      : processingStep === step.number
                      ? "step active"
                      : "step"
                  }
                >
                  <div className="step-icon">
                    {processingStep > step.number ? "✓" : step.number}
                  </div>

                  <div className="step-content">
                    <strong>{step.title}</strong>
                    <p>{step.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* ── ERROR ── */}
        {error && (
          <div className="error-card">
            <div>
              <strong>Analysis Error</strong>
              <p>{error}</p>
            </div>
          </div>
        )}

        {/* ── RESULTS ── */}
        {result && (
          <section className="results-section" ref={resultRef}>
            <div className="results-header">
              <div>
                <span className="section-label">SCREENING COMPLETE</span>
                <h2>Analysis Results</h2>
              </div>
              <span className="result-badge">Analysis Complete</span>
            </div>

            {/* ── Risk Summary ── */}
            <div className={`screening-summary ${getRiskClass()}`}>
              <div className="summary-content">
                <span className="section-label">OVERALL SCREENING RESULT</span>
                <h2>
                  {result.risk_assessment.risk_level === "HIGH"
                    ? "High Risk Document"
                    : result.risk_assessment.risk_level === "MEDIUM"
                    ? "Further Review Required"
                    : "Low Risk Document"}
                </h2>
                <p>{getRiskMessage()}</p>
              </div>

              <div className="summary-score">
                <ScoreRing score={result.risk_assessment.risk_score} />

                <div className="score-label">
                  <span>RISK SCORE</span>
                  <strong>{result.risk_assessment.risk_level}</strong>
                </div>
              </div>
            </div>

            {/* ── Signal Cards ── */}
            <div className="screening-signals">
              <div
                className={`signal-card ${getSignalClass(
                  result.ocr_confidence,
                  "higher_is_better"
                )}`}
              >
                <span>OCR CONFIDENCE</span>
                <strong>{result.ocr_confidence}%</strong>
                <small>Text extraction quality</small>
              </div>

              <div
                className={`signal-card ${
                  result.face_verification.status === "success"
                    ? getSignalClass(
                        result.face_verification.similarity_score,
                        "higher_is_better"
                      )
                    : ""
                }`}
              >
                <span>FACE SIMILARITY</span>
                <strong>
                  {result.face_verification.status === "success"
                    ? `${result.face_verification.similarity_score}%`
                    : "N/A"}
                </strong>
                <small>
                  {result.face_verification.verification ||
                    "Verification unavailable"}
                </small>
              </div>

              <div
                className={`signal-card ${getSignalClass(
                  getTamperingLabel(),
                  "string"
                )}`}
              >
                <span>TAMPERING SIGNAL</span>
                <strong>{getTamperingLabel()}</strong>
                <small>ELA score: {result.tampering_analysis.ela_score}</small>
              </div>

              <div
                className={`signal-card ${getSignalClass(
                  result.data_consistency.status,
                  "string"
                )}`}
              >
                <span>DATA CONSISTENCY</span>
                <strong>{result.data_consistency.status}</strong>
                <small>
                  {result.data_consistency.issues.length === 0
                    ? "All required fields detected"
                    : `${result.data_consistency.issues.length} issue(s) found`}
                </small>
              </div>
            </div>

            {/* ── Main Results Grid ── */}
            <div className="results-grid">
              {/* Risk Breakdown */}
              <div className="result-card">
                <div className="result-card-header">
                  <div>
                    <span className="section-label">RISK ANALYSIS</span>
                    <h3>Risk Breakdown</h3>
                  </div>
                </div>

                <div className="risk-breakdown">
                  {[
                    {
                      label: "Image Quality",
                      value: result.risk_assessment.risk_breakdown.image_quality,
                      max: 10,
                      weight: "10%",
                    },
                    {
                      label: "Tampering Detection",
                      value:
                        result.risk_assessment.risk_breakdown
                          .tampering_detection,
                      max: 30,
                      weight: "30%",
                    },
                    {
                      label: "Field Validation",
                      value:
                        result.risk_assessment.risk_breakdown.field_validation,
                      max: 20,
                      weight: "20%",
                    },
                    {
                      label: "Face Verification",
                      value:
                        result.risk_assessment.risk_breakdown.face_verification,
                      max: 30,
                      weight: "30%",
                    },
                    {
                      label: "Data Consistency",
                      value:
                        result.risk_assessment.risk_breakdown.data_consistency,
                      max: 10,
                      weight: "10%",
                    },
                  ].map(({ label, value, max, weight }) => (
                    <div className="risk-item" key={label}>
                      <div className="risk-item-top">
                        <span>{label}</span>
                        <strong>
                          {value}/{max}
                        </strong>
                      </div>
                      <div className="risk-bar">
                        <div
                          className="risk-fill"
                          style={{ width: `${(value / max) * 100}%` }}
                        />
                      </div>
                      <small>Weight: {weight}</small>
                    </div>
                  ))}
                </div>
              </div>

              {/* Extracted Information */}
              <div className="result-card">
                <div className="result-card-header">
                  <div>
                    <span className="section-label">OCR OUTPUT</span>
                    <h3>Extracted Information</h3>
                  </div>
                </div>

                <div className="info-list">
                  {[
                    { label: "Name", value: result.fields.name },
                    { label: "Date of Birth", value: result.fields.date_of_birth },
                    { label: "Gender", value: result.fields.gender },
                    { label: "Document Number", value: result.fields.document_number },
                  ].map(({ label, value }) => (
                    <div className="info-row" key={label}>
                      <span>{label}</span>
                      <strong>{value || "Not detected"}</strong>
                    </div>
                  ))}
                </div>
              </div>

              {/* Face Verification */}
              <div className="result-card">
                <div className="result-card-header">
                  <div>
                    <span className="section-label">BIOMETRIC SIGNAL</span>
                    <h3>Face Verification</h3>
                  </div>
                </div>

                <div className="verification-box">
                  <strong>
                    {result.face_verification.status === "success"
                      ? result.face_verification.verification
                      : "UNAVAILABLE"}
                  </strong>
                  <span>
                    Similarity:{" "}
                    {result.face_verification.status === "success"
                      ? `${result.face_verification.similarity_score}%`
                      : "N/A"}
                  </span>
                </div>
              </div>

              {/* Document Analysis */}
              <div className="result-card">
                <div className="result-card-header">
                  <div>
                    <span className="section-label">IMAGE ANALYSIS</span>
                    <h3>Document Analysis</h3>
                  </div>
                </div>

                <div className="info-list">
                  {[
                    {
                      label: "Image Width",
                      value: `${result.document_analysis.image_width}px`,
                    },
                    {
                      label: "Image Height",
                      value: `${result.document_analysis.image_height}px`,
                    },
                    {
                      label: "Blur Score",
                      value: result.document_analysis.blur_score,
                    },
                    {
                      label: "Brightness",
                      value: result.document_analysis.brightness,
                    },
                  ].map(({ label, value }) => (
                    <div className="info-row" key={label}>
                      <span>{label}</span>
                      <strong>{value}</strong>
                    </div>
                  ))}
                </div>
              </div>

              {/* Tampering Detection */}
              <div className="result-card">
                <div className="result-card-header">
                  <div>
                    <span className="section-label">MANIPULATION CHECK</span>
                    <h3>Tampering Detection</h3>
                  </div>
                </div>

                <div className="verification-box">
                  <strong>{getTamperingLabel()}</strong>
                  <span>
                    ELA Score: {result.tampering_analysis.ela_score}
                  </span>
                </div>
              </div>

              {/* Data Consistency */}
              <div className="result-card">
                <div className="result-card-header">
                  <div>
                    <span className="section-label">DATA VALIDATION</span>
                    <h3>Data Consistency</h3>
                  </div>
                </div>

                <div className="verification-box">
                  <strong>{result.data_consistency.status}</strong>
                  <span>
                    {result.data_consistency.issues.length === 0
                      ? "No consistency issues detected"
                      : `${result.data_consistency.issues.length} issue(s) detected`}
                  </span>
                </div>

                {result.data_consistency.issues.length > 0 && (
                  <ul className="issue-list">
                    {result.data_consistency.issues.map((issue, index) => (
                      <li key={index}>{issue}</li>
                    ))}
                  </ul>
                )}
              </div>
            </div>

            {/* ── Risk Reasons ── */}
            <div className="result-card reasons-card" style={{ marginTop: 18 }}>
              <div className="result-card-header">
                <div>
                  <span className="section-label">EXPLAINABLE ANALYSIS</span>
                  <h3>Risk Reasons</h3>
                </div>
              </div>

              {result.risk_assessment.reasons.length > 0 ? (
                <div className="reason-list">
                  {result.risk_assessment.reasons.map((reason, index) => (
                    <div className="reason-item" key={index}>
                      <span>!</span>
                      <p>{reason}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="no-reasons">
                  No major anomaly detected across screening signals.
                </div>
              )}
            </div>

            {/* ── Download ── */}
            <button className="download-button" onClick={downloadReport}>
              Download Screening Report
            </button>

            <div className="disclaimer">
              <strong>Prototype Disclaimer:</strong> This system provides
              preliminary risk screening only. It is not a legal determination of
              document authenticity or final identity verification. Manual
              verification is recommended for high-risk cases.
            </div>
          </section>
        )}
      </main>

      <footer className="footer">
        <span>AI-Based Fake Identity &amp; Document Screening System</span>
        <span>•</span>
        <span>Prototype for Hackathon Demonstration</span>
      </footer>
    </div>
  );
}

export default App;
