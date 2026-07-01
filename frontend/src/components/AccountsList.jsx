export default function AccountsList({ data }) {
  if (!data || !data.accounts || data.accounts.length === 0) {
    return <p>No accounts found.</p>
  }

  return (
    <div>
      {data.accounts.map((account) => (
        <div key={account.id} style={{ marginBottom: '1.5rem' }}>
          <h3>{account.name}</h3>
          <p>
            Balance: {account.balance} {account.currency}
          </p>
          <ul>
            {account.transactions?.slice(0, 5).map((tx) => (
              <li key={tx.id}>
                {tx.description}: {tx.amount}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  )
}
