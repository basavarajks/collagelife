function StatCard({ stat }) {
  return (
    <article className="card stat-card">
      <h3>{stat.value}</h3>
      <p>{stat.label}</p>
      <small>{stat.note}</small>
    </article>
  );
}

export default StatCard;
