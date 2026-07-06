import { useEffect, useMemo, useState } from 'react'
import './App.css'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const STORAGE_KEY = 'agente-ai-history'

function App() {
  const [question, setQuestion] = useState('')
  const [useTrusted, setUseTrusted] = useState(true)
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)
  const [targetId, setTargetId] = useState(null)
  const [similarity, setSimilarity] = useState(0)
  const [status, setStatus] = useState('')
  const [history, setHistory] = useState([])

  useEffect(() => {
    const savedHistory = window.localStorage.getItem(STORAGE_KEY)
    if (savedHistory) {
      try {
        setHistory(JSON.parse(savedHistory))
      } catch {
        window.localStorage.removeItem(STORAGE_KEY)
      }
    }
  }, [])

  const examples = useMemo(() => [
    'Qual é a política de brindes para diretores?',
    'Quais regras aplicam a viagens corporativas?',
    'Como proceder em caso de conflito de interesse?'
  ], [])

  async function handleSubmit(event) {
    event.preventDefault()
    if (!question.trim()) {
      setAnswer('Por favor, digite uma pergunta.')
      return
    }

    setLoading(true)
    setStatus('')
    try {
      const response = await fetch(`${API_BASE}/api/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, use_trusted: useTrusted })
      })

      const data = await response.json()
      setAnswer(data.answer || 'Nenhuma resposta recebida.')
      setTargetId(data.target_id ?? null)
      setSimilarity(data.similarity ?? 0)
      const nextEntry = { question, answer: data.answer || 'Nenhuma resposta recebida.', createdAt: new Date().toISOString() }
      const nextHistory = [nextEntry, ...history].slice(0, 8)
      setHistory(nextHistory)
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(nextHistory))
      setStatus('Consulta concluída com sucesso.')
    } catch (error) {
      setAnswer('Não foi possível conectar com o backend.')
      setStatus(error.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleFeedback(type) {
    if (!targetId && type !== 'ignored') {
      setStatus('Nenhum match disponível para registrar feedback.')
      return
    }

    try {
      const response = await fetch(`${API_BASE}/api/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          feedback_type: type,
          target_id: targetId,
          similarity,
          question
        })
      })

      const data = await response.json()
      setStatus(data.message || 'Feedback registrado.')
    } catch (error) {
      setStatus('Falha ao registrar feedback.')
    }
  }

  return (
    <main className="app-shell">
      <section className="hero-card">
        <div className="hero-copy">
          <p className="eyebrow">Trusted Compliance Agent</p>
          <h1>Consulte políticas com segurança e velocidade.</h1>
          <p className="subtitle">
            Interface moderna para perguntas sobre compliance com resposta confiável e feedback em tempo real.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="panel">
          <label className="switch-row">
            <input
              type="checkbox"
              checked={useTrusted}
              onChange={() => setUseTrusted((value) => !value)}
            />
            <span>Usar Trusted Answer Search</span>
          </label>

          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ex.: Qual é a política de brindes para diretores?"
            rows={5}
          />

          <div className="actions">
            <button type="submit" disabled={loading}>
              {loading ? 'Consultando...' : 'Consultar'}
            </button>
          </div>

          <div className="examples">
            {examples.map((example) => (
              <button key={example} type="button" onClick={() => setQuestion(example)}>
                {example}
              </button>
            ))}
          </div>
        </form>
      </section>

      <section className="result-card">
        <h2>Resposta</h2>
        <div className="answer-box">
          {loading ? 'Consultando resposta...' : answer || 'Aguardando consulta...'}
        </div>

        {(targetId || answer) && (
          <div className="feedback-row">
            <button type="button" onClick={() => handleFeedback('positive')}>👍 Útil</button>
            <button type="button" onClick={() => handleFeedback('negative')}>👎 Não útil</button>
            <button type="button" onClick={() => handleFeedback('ignored')}>Ignorar</button>
          </div>
        )}

        {status ? <p className="status">{status}</p> : null}

        {history.length > 0 ? (
          <div className="history-list">
            <h3>Histórico recente</h3>
            <ul>
              {history.map((entry) => (
                <li key={`${entry.createdAt}-${entry.question}`}>
                  <strong>{entry.question}</strong>
                  <span>{entry.answer}</span>
                </li>
              ))}
            </ul>
          </div>
        ) : null}
      </section>
    </main>
  )
}

export default App
