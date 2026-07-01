const BASE_URL = '/api'

export async function getConnectionStatus() {
  const res = await fetch(`${BASE_URL}/simplefin/status`)
  return res.json()
}

export async function connectSimpleFin(setupToken) {
  const res = await fetch(`${BASE_URL}/simplefin/connect`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ setup_token: setupToken }),
  })
  if (!res.ok) {
    const error = await res.json()
    throw new Error(error.detail || 'Failed to connect')
  }
  return res.json()
}

export async function getAccounts() {
  const res = await fetch(`${BASE_URL}/accounts/`)
  if (!res.ok) {
    const error = await res.json()
    throw new Error(error.detail || 'Failed to fetch accounts')
  }
  return res.json()
}
