
// //import { useState } from "react";
// import { useEffect, useState } from "react";
// import "./App.css";

// function App() {
//   const [issue, setIssue] = useState("");
//   const [category, setCategory] = useState("Billing");
//   const [message, setMessage] = useState("");

//   const [tickets, setTickets] = useState([]);
// const [loading, setLoading] = useState(false);

// async function loadTickets() {
//   setLoading(true);

//   try {
//     const response = await fetch("http://127.0.0.1:8000/tickets");
//     if (!response.ok) throw new Error("Could not load tickets");

//     const data = await response.json();
//     setTickets(data);
//   } catch (error) {
//     setMessage(`Error loading tickets: ${error.message}`);
//   } finally {
//     setLoading(false);
//   }
// }

// useEffect(() => {
//   loadTickets();
// }, []);

//   async function handleSubmit(event) {
//     event.preventDefault();
//     setMessage("Submitting ticket...");

//     try {
//       const response = await fetch("http://127.0.0.1:8000/tickets", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({
//           customer_issue: issue,
//           category: category,
//         }),
//       });

//       const data = await response.json();

//       if (!response.ok) {
//         throw new Error(data.detail || "Could not create ticket");
//       }

//       setMessage(`Ticket created! ID: ${data.ticket_id ?? data.id ?? "Check response"}`);
//       setIssue("");
//     } catch (error) {
//       setMessage(`Error: ${error.message}. Check that the backend is running.`);
//     }
//   }

//   return (
//     <main className="app">
//       <header className="header">
//         <div className="brand">Support<span>AI</span></div>
//         <span className="status">● Support Portal</span>
//       </header>

//       <section className="hero">
//         <p className="eyebrow">AI CUSTOMER SUPPORT</p>
//         <h1>How can we help you?</h1>
//         <p>Tell us what's wrong. We'll help you track your support request.</p>
//       </section>

//       <section className="panel">
//         <h2>Create a support ticket</h2>
//         <p className="muted">Describe your issue and submit a request.</p>

//         <form onSubmit={handleSubmit}>
//           <label htmlFor="issue">Describe your issue</label>
//           <textarea
//             id="issue"
//             value={issue}
//             onChange={(event) => setIssue(event.target.value)}
//             placeholder="Example: I was charged twice for my subscription..."
//             required
//             minLength={5}
//           />

//           <label htmlFor="category">Category</label>
//           <select
//             id="category"
//             value={category}
//             onChange={(event) => setCategory(event.target.value)}
//           >
//             <option>Billing</option>
//             <option>Account</option>
//             <option>Technical</option>
//             <option>General</option>
//           </select>

//           <button type="submit">Submit ticket →</button>
//         </form>

//         {message && <p className="message" role="status">{message}</p>}
          






//       </section>

//       <footer>AI Customer Support Ticket Assistant · Built with React & FastAPI</footer>
//     </main>
//   );
// }

// export default App;



import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [issue, setIssue] = useState("");
  //const [category, setCategory] = useState("Billing");
  const [message, setMessage] = useState("");
  const [aiResponse, setAiResponse] = useState("");
  const [aiLoading, setAiLoading] = useState(false);
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  async function loadTickets() {
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/tickets`);

      if (!response.ok) {
        throw new Error("Could not load tickets");
      }

      const data = await response.json();
      setTickets(data);
    } catch (error) {
      setMessage(`Error loading tickets: ${error.message}`);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadTickets();
  }, []);

  async function updateTicketStatus(ticketId, newStatus) {
    try {
      const response = await fetch(
        `${API_URL}/tickets/${ticketId}/status`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ status: newStatus }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Could not update status");
      }

      setMessage(`Ticket #${ticketId} status updated to ${newStatus}`);
      await loadTickets();
    } catch (error) {
      setMessage(`Error updating status: ${error.message}`);
    }
  }
  
async function getAIResponse(customerIssue) {
  setAiLoading(true);
  setAiResponse("");

  try {
    const response = await fetch(`${API_URL}/ai-assist`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        customer_issue: customerIssue,
        category: "General",
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "AI request failed");
    }

    if (data.success) {
      setAiResponse(data.response);
    } else {
      setAiResponse(data.error || "AI is temporarily unavailable.");
    }
  } catch (error) {
    setAiResponse(
      `AI is temporarily unavailable: ${error.message}`
    );
  } finally {
    setAiLoading(false);
  }
}


  async function handleSubmit(event) {
    event.preventDefault();
    setSubmitting(true);
    setMessage("");

    try {
      const response = await fetch(`${API_URL}/tickets`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          customer_issue: issue.trim(),
          category: "General",
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Could not create ticket");
      }

      const ticketId = data.ticket_id ?? data.id;

      setMessage(
        ticketId
          ? `Ticket created successfully! ID: ${ticketId}`
          : data.message || "Ticket request completed."
      );

      setIssue("");
      await getAIResponse(issue.trim());
      await loadTickets();
    } catch (error) {
      setMessage(`Error: ${error.message}. Check that the backend is running.`);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="app">
      <header className="header">
        <div className="brand">
          Support<span>AI</span>
        </div>
        <span className="status">● Support Portal</span>
      </header>

      <section className="hero">
        <p className="eyebrow">AI CUSTOMER SUPPORT</p>
        <h1>How can we help you?</h1>
        <p>
          Tell us what is wrong. We will help you track your support request.
        </p>
      </section>

      <section className="panel">
        <h2>Create a support ticket</h2>
        <p className="muted">
          Describe your issue and submit a request.
        </p>

        <form onSubmit={handleSubmit}>
          <label htmlFor="issue">Describe your issue</label>

          <textarea
            id="issue"
            value={issue}
            onChange={(event) => setIssue(event.target.value)}
            placeholder="Example: I was charged twice for my subscription..."
            required
            minLength={5}
          />

          {/* <label htmlFor="category">Category</label>

          <select
            id="category"
            value={category}
            onChange={(event) => setCategory(event.target.value)}
          >
            <option value="Billing">Billing</option>
            <option value="Account">Account</option>
            <option value="Technical">Technical</option>
            <option value="General">General</option>
          </select> */}

          <button type="submit" disabled={submitting}>
            {submitting ? "Submitting..." : "Submit ticket →"}
          </button>
        </form>

        {message && (
          <p className="message" role="status">
            {message}
          </p>
        )}
        
{aiLoading && (
  <p className="message">AI is analyzing your issue...</p>
)}

{aiResponse && (
  <section className="panel">
    <h2>AI Support Assistant</h2>
    <p className="ai-response">{aiResponse}</p>
  </section>
)}

      </section>

      <section className="ticket-section">
        <div className="ticket-heading">
          <div>
            <h2>Support Tickets</h2>
            <p className="muted">
              Track your submitted requests.
            </p>
          </div>

          <button
            type="button"
            onClick={loadTickets}
            disabled={loading}
          >
            {loading ? "Loading..." : "Refresh"}
          </button>
        </div>

        {loading && tickets.length === 0 ? (
          <p className="muted">Loading tickets...</p>
        ) : tickets.length === 0 ? (
          <p className="muted">No tickets found.</p>
        ) : (
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Issue</th>
                  <th>Category</th>
                  <th>Status</th>
                </tr>
              </thead>

              <tbody>
                {tickets.map((ticket) => (
                  <tr key={ticket.id}>
                    <td>#{ticket.id}</td>
                    <td>{ticket.customer_issue}</td>
                    <td>{ticket.category}</td>
                    <td>
                    <select
                        value={ticket.status}
                        onChange={(event) =>
                        updateTicketStatus(ticket.id, event.target.value)
                        }
                      >
                     <option value="Open">Open</option>
                     <option value="In Progress">In Progress</option>
                     <option value="Closed">Closed</option>
                    </select>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <footer>
        AI Customer Support Ticket Assistant · Built with React &amp; FastAPI
      </footer>
    </main>
  );
}

export default App;
