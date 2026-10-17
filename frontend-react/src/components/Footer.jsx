const currentYear = new Date().getFullYear();

function Footer({ college }) {
  return (
    <footer className="site-footer" id="contact">
      <div className="container footer-grid">
        <section>
          <h3>{college.name}</h3>
          <p>Phase 1 demo footer. Replace with verified institution details.</p>
        </section>
        <section>
          <h4>Contact</h4>
          <p>{college.contact.address}</p>
          <p>{college.contact.phone}</p>
          <p>{college.contact.email}</p>
          <p>{college.contact.website}</p>
        </section>
      </div>
      <p className="copyright">© {currentYear} SDMS Phase 1 Demo</p>
    </footer>
  );
}

export default Footer;
