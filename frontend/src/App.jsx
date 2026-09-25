import { useState } from "react";
import {
  FileText,
  Upload,
  Send,
  Bot,
  User,
  LoaderCircle,
  AlertCircle,
} from "lucide-react";

function App() {
  const [documentId, setDocumentId] = useState(null);
  const [documentName, setDocumentName] = useState(null);

  const [question, setQuestion] = useState("");
  const [lastQuestion, setLastQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [sources, setSources] = useState([]);

  const [uploading, setUploading] = useState(false);
  const [asking, setAsking] = useState(false);

  const [error, setError] = useState(null);

  // Temporary user ID.
  // Later this will come from authentication.
  const userId = "user_1";

  // =========================================================
  // Read error response safely
  // IMPORTANT:
  // We read response.body only ONCE.
  // =========================================================

  async function getErrorMessage(response, fallbackMessage) {
    try {
      const text = await response.text();

      if (!text) {
        return fallbackMessage;
      }

      try {
        const data = JSON.parse(text);

        if (typeof data.detail === "string") {
          return data.detail;
        }

        if (typeof data.message === "string") {
          return data.message;
        }

        return fallbackMessage;
      } catch {
        return text;
      }
    } catch {
      return fallbackMessage;
    }
  }

  // =========================================================
  // Upload PDF
  // =========================================================

  async function handleUpload(event) {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    if (file.type !== "application/pdf") {
      setError("Please select a PDF file.");
      return;
    }

    setUploading(true);
    setError(null);

    const formData = new FormData();

    formData.append("file", file);
    formData.append("user_id", userId);

    try {
      const response = await fetch("/api/documents/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const message = await getErrorMessage(
          response,
          "Failed to upload document.",
        );

        throw new Error(message);
      }

      const data = await response.json();

      console.log("Upload response:", data);

      setDocumentId(data.document_id);
      setDocumentName(file.name);

      // Reset conversation for new document
      setQuestion("");
      setLastQuestion("");
      setAnswer(null);
      setSources([]);
    } catch (error) {
      console.error("Upload error:", error);

      setError(
        error.message || "Something went wrong while uploading the document.",
      );
    } finally {
      setUploading(false);

      // Allow selecting the same file again
      event.target.value = "";
    }
  }

  // =========================================================
  // Ask Question
  // =========================================================

  async function handleAsk() {
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || !documentId || asking) {
      return;
    }

    setAsking(true);
    setError(null);

    // Keep question visible while API request is running
    setLastQuestion(trimmedQuestion);

    try {
      const response = await fetch("/api/ask", {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          question: trimmedQuestion,
          user_id: userId,
          document_id: documentId,
        }),
      });

      if (!response.ok) {
        const message = await getErrorMessage(
          response,
          "Failed to get an answer.",
        );

        throw new Error(message);
      }

      const data = await response.json();

      console.log("Ask response:", data);

      setAnswer(data.answer || "");
      setSources(data.sources || []);

      // Clear input after successful request
      setQuestion("");
    } catch (error) {
      console.error("Ask error:", error);

      setError(
        error.message || "Something went wrong while getting the answer.",
      );
    } finally {
      setAsking(false);
    }
  }

  // =========================================================
  // Keyboard handling
  //
  // Enter       -> Ask
  // Shift+Enter -> New line
  // =========================================================

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();

      handleAsk();
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      {/* =====================================================
          HEADER
      ====================================================== */}

      <header className="h-16 border-b border-slate-200 bg-white flex items-center justify-between px-6">
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 rounded-lg bg-blue-600 flex items-center justify-center">
            <FileText className="h-5 w-5 text-white" />
          </div>

          <div>
            <h1 className="font-semibold text-lg">MedRAG</h1>

            <p className="text-xs text-slate-500">Medical Document Assistant</p>
          </div>
        </div>

        <span className="text-sm text-slate-500">Medical AI</span>
      </header>

      {/* =====================================================
          MAIN
      ====================================================== */}

      <main className="flex h-[calc(100vh-4rem)]">
        {/* ===================================================
            SIDEBAR
        ==================================================== */}

        <aside className="w-72 border-r border-slate-200 bg-white p-5">
          <h2 className="font-semibold mb-5">Documents</h2>

          {/* Upload button */}

          <label
            className={`
              flex
              items-center
              justify-center
              gap-2
              w-full
              h-11
              rounded-lg
              text-white
              text-sm
              font-medium
              transition
              ${
                uploading
                  ? "bg-blue-400 cursor-not-allowed"
                  : "bg-blue-600 hover:bg-blue-700 cursor-pointer"
              }
            `}
          >
            {uploading ? (
              <LoaderCircle className="h-4 w-4 animate-spin" />
            ) : (
              <Upload className="h-4 w-4" />
            )}

            {uploading ? "Uploading..." : "Upload PDF"}

            <input
              type="file"
              accept="application/pdf,.pdf"
              className="hidden"
              onChange={handleUpload}
              disabled={uploading}
            />
          </label>

          {/* Uploaded document */}

          {documentId && (
            <div className="mt-6">
              <div className="flex items-center gap-3 p-3 rounded-lg bg-blue-50 border border-blue-100">
                <div className="h-9 w-9 rounded-lg bg-white flex items-center justify-center shrink-0">
                  <FileText className="h-5 w-5 text-blue-600" />
                </div>

                <div className="min-w-0">
                  <p className="text-sm font-medium truncate">{documentName}</p>

                  <p className="text-xs text-green-600">Ready</p>
                </div>
              </div>
            </div>
          )}
        </aside>

        {/* ===================================================
            CHAT
        ==================================================== */}

        <section className="flex-1 flex flex-col">
          {/* Chat header */}

          <div className="h-16 border-b border-slate-200 bg-white px-8 flex items-center">
            <div>
              <h2 className="font-semibold">Medical Assistant</h2>

              <p className="text-xs text-slate-500">
                Ask questions about your medical report
              </p>
            </div>
          </div>

          {/* =================================================
              MESSAGES
          ================================================== */}

          <div className="flex-1 overflow-y-auto px-8 py-8">
            {/* Error */}

            {error && (
              <div className="max-w-4xl mx-auto mb-6">
                <div className="flex items-start gap-3 rounded-lg border border-red-200 bg-red-50 px-4 py-3">
                  <AlertCircle className="h-5 w-5 text-red-500 shrink-0 mt-0.5" />

                  <div className="min-w-0">
                    <p className="text-sm font-medium text-red-700">
                      Something went wrong
                    </p>

                    <p className="text-sm text-red-600 mt-1 break-words">
                      {error}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Empty state */}

            {!lastQuestion && !answer && !asking && !error && (
              <div className="h-full flex items-center justify-center">
                <div className="text-center max-w-md">
                  <div className="mx-auto h-14 w-14 rounded-2xl bg-blue-100 flex items-center justify-center mb-5">
                    <Bot className="h-7 w-7 text-blue-600" />
                  </div>

                  <h3 className="text-xl font-semibold mb-2">
                    Ask about your medical report
                  </h3>

                  <p className="text-sm text-slate-500 leading-6">
                    {documentId
                      ? "Your report is ready. Ask a question to get started."
                      : "Upload a medical PDF and ask questions about the information contained in it."}
                  </p>
                </div>
              </div>
            )}

            {/* Conversation */}

            {(lastQuestion || answer || asking) && (
              <div className="max-w-4xl mx-auto space-y-6">
                {/* =========================================
                    USER MESSAGE
                ========================================== */}

                {lastQuestion && (
                  <div className="flex justify-end">
                    <div className="flex items-start gap-3 max-w-2xl">
                      <div className="bg-blue-600 text-white rounded-2xl rounded-tr-sm px-4 py-3 text-sm whitespace-pre-wrap">
                        {lastQuestion}
                      </div>

                      <div className="h-8 w-8 rounded-full bg-slate-200 flex items-center justify-center shrink-0">
                        <User className="h-4 w-4 text-slate-600" />
                      </div>
                    </div>
                  </div>
                )}

                {/* =========================================
                    LOADING
                ========================================== */}

                {asking && (
                  <div className="flex items-start gap-3 max-w-3xl">
                    <div className="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center shrink-0">
                      <Bot className="h-4 w-4 text-blue-600" />
                    </div>

                    <div className="bg-white border border-slate-200 rounded-2xl rounded-tl-sm px-5 py-4">
                      <div className="flex items-center gap-2">
                        <LoaderCircle className="h-4 w-4 text-blue-600 animate-spin" />

                        <span className="text-sm text-slate-500">
                          Analyzing your report...
                        </span>
                      </div>
                    </div>
                  </div>
                )}

                {/* =========================================
                    AI ANSWER
                ========================================== */}

                {answer && !asking && (
                  <div className="flex items-start gap-3 max-w-3xl">
                    <div className="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center shrink-0">
                      <Bot className="h-4 w-4 text-blue-600" />
                    </div>

                    <div className="bg-white border border-slate-200 rounded-2xl rounded-tl-sm px-5 py-4">
                      <p className="text-sm leading-6 whitespace-pre-wrap">
                        {answer}
                      </p>
                    </div>
                  </div>
                )}

                {/* =========================================
                    SOURCES
                ========================================== */}

                {answer && !asking && sources.length > 0 && (
                  <div className="ml-11">
                    <h3 className="text-sm font-semibold mb-3">Sources</h3>

                    <div className="space-y-2">
                      {sources.map((source, index) => (
                        <div
                          key={`${source.document_id}-${source.chunk_index}-${index}`}
                          className="flex items-center gap-3 bg-white border border-slate-200 rounded-lg px-4 py-3"
                        >
                          <FileText className="h-4 w-4 text-blue-600 shrink-0" />

                          <div className="text-xs text-slate-600">
                            <span className="font-medium">
                              Page {source.page ?? "N/A"}
                            </span>

                            <span className="mx-2">•</span>

                            <span>Chunk {source.chunk_index ?? "N/A"}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* =================================================
              INPUT
          ================================================== */}

          <div className="border-t border-slate-200 bg-white p-5">
            <div className="max-w-4xl mx-auto">
              <div className="flex gap-3">
                <textarea
                  rows="1"
                  value={question}
                  onChange={(event) => {
                    setQuestion(event.target.value);

                    if (error) {
                      setError(null);
                    }
                  }}
                  onKeyDown={handleKeyDown}
                  placeholder={
                    documentId
                      ? "Ask a question about your report..."
                      : "Upload a report first..."
                  }
                  disabled={!documentId || asking}
                  className="
                    flex-1
                    resize-none
                    border
                    border-slate-300
                    rounded-xl
                    px-4
                    py-3
                    text-sm
                    outline-none
                    focus:border-blue-500
                    focus:ring-2
                    focus:ring-blue-100
                    disabled:bg-slate-100
                    disabled:cursor-not-allowed
                  "
                />

                <button
                  onClick={handleAsk}
                  disabled={!documentId || !question.trim() || asking}
                  className="
                    h-11
                    w-11
                    rounded-xl
                    bg-blue-600
                    text-white
                    flex
                    items-center
                    justify-center
                    hover:bg-blue-700
                    disabled:bg-slate-300
                    disabled:cursor-not-allowed
                    transition
                    shrink-0
                  "
                >
                  {asking ? (
                    <LoaderCircle className="h-4 w-4 animate-spin" />
                  ) : (
                    <Send className="h-4 w-4" />
                  )}
                </button>
              </div>

              <p className="text-xs text-slate-400 mt-2 text-center">
                Press Enter to ask • Shift + Enter for a new line
              </p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
