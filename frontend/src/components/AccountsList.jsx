export default function AccountsList({ data }) {
  if (!data) {
    return <p>No data.</p>
  }
  console.log(data)

  return (
    <div>
      {data.map((account, index) => (
        <p key={index}>{account.name}</p>
      ))}
    </div>
  )
}
