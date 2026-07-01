import { useState } from 'react'
import { connectSimpleFin } from '../api/client'

export default function ConnectBank({ onConnected }) {
  const [token, setToken] = useState('')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      await connectSimpleFin(token.trim())
      onConnected()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>
        SimpleFIN Setup Token
        <input
          type="text"
          value={token}
          onChange={(e) => setToken(e.target.value)}
          placeholder="Paste your setup token here"
          style={{ display: 'block', width: '100%', marginTop: '0.25rem' }}
        />
      </label>
      <button type="submit" disabled={loading || !token} style={{ marginTop: '0.5rem' }}>
        {loading ? 'Connecting...' : 'Connect'}
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </form>
  )
}
