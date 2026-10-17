import { Bolt, Building2, Cog, Cpu, Radio } from 'lucide-react';

const iconByKey = {
  cse: Cpu,
  ece: Radio,
  me: Cog,
  ce: Building2,
  eee: Bolt,
};

function DepartmentCard({ department }) {
  const Icon = iconByKey[department.key] || Building2;

  return (
    <article className="card department-card">
      <Icon size={22} aria-hidden="true" />
      <h3>{department.title}</h3>
      <p>{department.description}</p>
      {department.learnMoreUrl ? (
        <a href={department.learnMoreUrl}>Learn More</a>
      ) : (
        <p className="disabled-note">Learn More not configured in Phase 1 demo.</p>
      )}
    </article>
  );
}

export default DepartmentCard;
