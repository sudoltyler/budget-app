import { useEffect, useState } from 'react'
import ConnectBank from './components/ConnectBank'
import AccountsList from './components/AccountsList'
import { getConnectionStatus, getAccounts, syncAccounts } from './api/client'

export default function App() {
  const [connected, setConnected] = useState(false);
  const [accountsData, setAccountsData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getConnectionStatus().then((status) => setConnected(status.connected));
  }, []);

  useEffect(() => {
    if (connected) {
      getAccounts()
        .then(setAccountsData)
        .catch((err) => setError(err.message));
    }
  }, [connected]);

  function handleClickSync() {
    syncAccounts()
      .then(() => getAccounts())
      .then(setAccountsData)
      .catch((err) => setError(err.message))
  };

  return (
    <div style={{ maxWidth: 600, margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h1>Budget App</h1>
      {!connected ? (
        <ConnectBank onConnected={() => setConnected(true)} />
      ) : (
        <>
          {error && <p style={{ color: 'red' }}>{error}</p>}
          <AccountsList data={accountsData} />
          <button onClick={handleClickSync}>Sync</button>
        </>
      )}
    </div>
  )
};
