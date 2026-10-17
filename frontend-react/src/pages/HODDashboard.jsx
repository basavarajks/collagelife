import { useEffect, useState } from 'react';
import { BookOpen, Building2, CalendarDays, ClipboardList, FileText, LayoutDashboard, LogOut, Menu, Megaphone, Users, X } from 'lucide-react';
import { getApiErrorMessage } from '../services/api';
import { hodApi } from '../services/hodApi';

const sections = [
  ['dashboard', 'Dashboard', LayoutDashboard],
  ['department', 'Department Profile', Building2],
  ['faculty', 'Faculty Overview', Users],
  ['students', 'Student Overview', Users],
  ['academic', 'Academic Structure', CalendarDays],
  ['assignments', 'Faculty Assignments', ClipboardList],
  ['announcements', 'Department Announcements', Megaphone],
  ['reports', 'Department Reports', FileText],
];

function HODDashboard({ auth, onLogout }) {
  const [section, setSection] = useState('dashboard');
  const [mobileOpen, setMobileOpen] = useState(false);
  const [selectedDepartment, setSelectedDepartment] = useState(auth.user?.departments?.[0]?.id || '');
  const [dashboard, setDashboard] = useState(null);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');

  const loadDashboard = async () => {
    try { setError(''); const response = await hodApi.dashboard(selectedDepartment); setDashboard(response.data?.data || null); }
    catch (requestError) { setError(getApiErrorMessage(requestError)); }
  };
  useEffect(() => { loadDashboard(); }, [selectedDepartment]);

  const departmentId = selectedDepartment || dashboard?.department?.id;
  const render = () => {
    if (section === 'dashboard') return <Overview data={dashboard} />;
    if (section === 'department') return <DepartmentPanel departmentId={departmentId} setError={setError} />;
    if (section === 'faculty') return <UnavailablePanel title="Faculty Overview" message="Faculty records are not yet linked to departments. No faculty records are fabricated." />;
    if (section === 'students') return <UnavailablePanel title="Student Overview" message="Student records are not implemented yet. The API returns an empty, department-scoped state." />;
    if (section === 'academic') return <AcademicPanel departmentId={departmentId} setError={setError} />;
    if (section === 'assignments') return <UnavailablePanel title="Faculty Assignments" message="Faculty assignment records are planned for a later phase." />;
    if (section === 'announcements') return <AnnouncementsPanel departmentId={departmentId} setError={setError} setNotice={setNotice} />;
    if (section === 'reports') return <ReportsPanel departmentId={departmentId} setError={setError} />;
    return null;
  };

  return <div className="hod-shell">
    <aside className={`hod-sidebar ${mobileOpen ? 'open' : ''}`}><div className="hod-brand"><strong>SDMS</strong><button type="button" aria-label="Close navigation" onClick={() => setMobileOpen(false)}><X size={18} /></button></div><nav>{sections.map(([key, label, Icon]) => <button key={key} className={section === key ? 'active' : ''} type="button" onClick={() => { setSection(key); setMobileOpen(false); }}><Icon size={18} /><span>{label}</span></button>)}</nav><button type="button" className="hod-logout" onClick={onLogout}><LogOut size={18} />Logout</button></aside>
    {mobileOpen && <button className="hod-backdrop" type="button" aria-label="Close navigation" onClick={() => setMobileOpen(false)} />}
    <main className="hod-main"><header className="hod-header"><button type="button" className="hod-menu" aria-label="Open navigation" onClick={() => setMobileOpen(true)}><Menu size={22} /></button><div><p className="eyebrow">HOD workspace</p><h1>{sections.find(([key]) => key === section)?.[1]}</h1></div><div className="hod-user"><strong>{auth.user?.full_name}</strong><span>{dashboard?.department?.name || 'Department not assigned'}</span></div></header>
      {auth.user?.departments?.length > 1 && <label className="hod-department-select">Department scope<select value={selectedDepartment} onChange={(event) => setSelectedDepartment(event.target.value)}>{auth.user.departments.map((item) => <option key={item.id} value={item.id}>{item.name} ({item.code})</option>)}</select></label>}
      {notice && <p className="success-message" role="status">{notice}</p>}{error && <p className="error-message" role="alert">{error}</p>}<section className="hod-content">{render()}</section>
    </main>
  </div>;
}

function Overview({ data }) { if (!data) return <p>Loading department dashboard…</p>; const cards = [['Active students', data.students], ['Active faculty', data.faculty], ['Subjects', data.subjects], ['Published announcements', data.announcements]]; return <><div className="hod-cards">{cards.map(([label, value]) => <article className="hod-stat" key={label}><span>{label}</span><strong>{value ?? 0}</strong></article>)}</div><div className="hod-grid"><article className="hod-panel"><h2>Department</h2><p><strong>{data.department.name}</strong> ({data.department.code})</p><p>{data.department.description || 'No department description has been configured.'}</p><p>Academic year: {data.current_academic_year || 'Not configured'}</p></article><article className="hod-panel"><h2>Availability</h2><p>{data.availability?.students ? 'Student module available.' : 'Student module is not implemented yet.'}</p><p>{data.availability?.faculty ? 'Faculty module available.' : 'Faculty department records are not implemented yet.'}</p></article></div></>; }
function DepartmentPanel({ departmentId, setError }) { const [department, setDepartment] = useState(null); useEffect(() => { hodApi.department(departmentId).then((r) => setDepartment(r.data?.data?.department)).catch((e) => setError(getApiErrorMessage(e))); }, [departmentId]); if (!department) return <p>Loading department profile…</p>; return <article className="hod-panel"><h2>{department.name}</h2><dl className="hod-details"><dt>Code</dt><dd>{department.code}</dd><dt>Status</dt><dd>{department.is_active ? 'Active' : 'Inactive'}</dd><dt>Assigned HOD</dt><dd>{department.head_name || 'Not configured'}</dd><dt>Description</dt><dd>{department.description || 'Not configured'}</dd></dl><p className="muted-note">Department identifiers and scope are managed by an authorized Admin/Principal.</p></article>; }
function AcademicPanel({ departmentId, setError }) { const [items, setItems] = useState(null); useEffect(() => { hodApi.academicStructure(departmentId).then((r) => setItems(r.data?.data?.items || [])).catch((e) => setError(getApiErrorMessage(e))); }, [departmentId]); if (!items) return <p>Loading academic structure…</p>; return <article className="hod-panel"><h2>Academic structure</h2>{items.length ? items.map((item) => <div className="hod-list-row" key={item.id}><strong>{item.name}{item.is_current ? ' · Current' : ''}</strong><span>{item.start_date} – {item.end_date} · {item.semesters.length} semester(s)</span></div>) : <p>No academic years configured.</p>}</article>; }
function AnnouncementsPanel({ departmentId, setError, setNotice }) { const [items, setItems] = useState([]); const [form, setForm] = useState({ title: '', message: '', department_id: departmentId }); const load = () => hodApi.announcements(departmentId).then((r) => setItems(r.data?.data?.items || [])).catch((e) => setError(getApiErrorMessage(e))); useEffect(() => { setForm((value) => ({ ...value, department_id: departmentId })); load(); }, [departmentId]); const submit = async (event) => { event.preventDefault(); try { await hodApi.createAnnouncement({ ...form, department_id: departmentId }); setForm({ title: '', message: '', department_id: departmentId }); setNotice('Department announcement draft created.'); load(); } catch (e) { setError(getApiErrorMessage(e)); } }; return <><form className="hod-panel hod-form" onSubmit={submit}><h2>Create department announcement draft</h2><label>Title<input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required /></label><label>Message<textarea value={form.message} onChange={(e) => setForm({ ...form, message: e.target.value })} required /></label><button className="button-link button-primary" type="submit">Save draft</button></form><article className="hod-panel"><h2>Published announcements</h2>{items.length ? items.map((item) => <div className="hod-list-row" key={item.id}><div><strong>{item.title}</strong><p>{item.message}</p></div><span>{item.status}</span></div>) : <p>No published announcements are available for this department.</p>}</article></>; }
function ReportsPanel({ departmentId, setError }) { const [data, setData] = useState(null); useEffect(() => { hodApi.reports(departmentId).then((r) => setData(r.data?.data)).catch((e) => setError(getApiErrorMessage(e))); }, [departmentId]); if (!data) return <p>Loading department reports…</p>; return <article className="hod-panel"><h2>Department reports</h2><div className="hod-report-grid"><div><strong>{data.student_count}</strong><span>Students</span></div><div><strong>{data.faculty_count}</strong><span>Faculty</span></div><div><strong>{data.announcement_count}</strong><span>Announcements</span></div></div><p className="muted-note">{data.message}</p></article>; }
function UnavailablePanel({ title, message }) { return <article className="hod-panel"><h2>{title}</h2><p>{message}</p></article>; }
export default HODDashboard;
