import { Menu, X, LogIn } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import ImageWithFallback from './ImageWithFallback';

const navLinks = [
  { label: 'Home', href: '#home' },
  { label: 'About Us', href: '#about' },
  { label: 'Departments', href: '#departments' },
  { label: 'Campus Life', href: '#activities' },
  { label: 'Gallery', href: '#gallery' },
  { label: 'Notices', href: '#notices' },
  { label: 'Contact', href: '#contact' },
];

function Header({ college }) {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onEsc = (event) => {
      if (event.key === 'Escape') {
        setOpen(false);
      }
    };

    window.addEventListener('keydown', onEsc);
    return () => window.removeEventListener('keydown', onEsc);
  }, []);

  const closeMenu = () => setOpen(false);

  return (
    <header className="site-header" id="home">
      <div className="container nav-wrapper">
        <a href="#home" className="brand" aria-label="Go to homepage top">
          <ImageWithFallback
            src={college.logo}
            alt={`${college.name} logo`}
            className="brand-logo"
            fallbackText="Logo unavailable"
          />
          <span>{college.name}</span>
        </a>

        <button
          className="menu-toggle"
          type="button"
          aria-label={open ? 'Close menu' : 'Open menu'}
          aria-controls="primary-navigation"
          aria-expanded={open}
          onClick={() => setOpen((current) => !current)}
        >
          {open ? <X size={20} /> : <Menu size={20} />}
        </button>

        <nav id="primary-navigation" className={`nav-links ${open ? 'open' : ''}`} aria-label="Primary">
          {navLinks.map((link) => (
            <a key={link.label} href={link.href} onClick={closeMenu}>
              {link.label}
            </a>
          ))}
          <Link className="login-button" to="/login" onClick={closeMenu}>
            <LogIn size={16} />
            <span>Login</span>
          </Link>
        </nav>
      </div>
    </header>
  );
}

export default Header;
