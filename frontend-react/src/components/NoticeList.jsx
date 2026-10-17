function NoticeList({ notices, note }) {
  return (
    <section className="section" id="notices" aria-labelledby="notices-title">
      <div className="container">
        <h2 id="notices-title">Notices & Announcements</h2>
        <p className="section-note">{note}</p>
        <div className="card-grid">
          {notices.length === 0 ? (
            <p className="empty-state">No notices available.</p>
          ) : (
            notices.map((notice) => (
              <article key={`${notice.title}-${notice.date}`} className="card notice-card">
                <h3>{notice.title}</h3>
                <p>{notice.description}</p>
                <p className="notice-date">Published: {notice.date}</p>
                {notice.link ? (
                  <a href={notice.link}>View Details</a>
                ) : (
                  <p className="disabled-note">Attachment/view link not configured.</p>
                )}
              </article>
            ))
          )}
        </div>
      </div>
    </section>
  );
}

export default NoticeList;
