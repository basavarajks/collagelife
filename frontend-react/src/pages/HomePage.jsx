import { useEffect, useMemo, useState } from 'react';
import { ArrowRight, LogIn } from 'lucide-react';
import { Link } from 'react-router-dom';
import DepartmentCard from '../components/DepartmentCard';
import Footer from '../components/Footer';
import GalleryGrid from '../components/GalleryGrid';
import Header from '../components/Header';
import ImageWithFallback from '../components/ImageWithFallback';
import NoticeList from '../components/NoticeList';
import StatCard from '../components/StatCard';

function HomePage({ college }) {
  const [heroIndex, setHeroIndex] = useState(0);
  const heroImage = useMemo(() => college.heroImages[heroIndex] || '', [college.heroImages, heroIndex]);
  const heroAlt = useMemo(() => college.heroAlt[heroIndex] || 'Hero image unavailable', [college.heroAlt, heroIndex]);

  useEffect(() => {
    if (college.heroImages.length <= 1) {
      return undefined;
    }

    const interval = setInterval(() => {
      setHeroIndex((current) => (current + 1) % college.heroImages.length);
    }, 4500);

    return () => clearInterval(interval);
  }, [college.heroImages.length]);

  return (
    <>
      <Header college={college} />

      <main>
        <section className="hero" aria-labelledby="hero-title">
          <ImageWithFallback src={heroImage} alt={heroAlt} className="hero-image" fallbackText="Hero image unavailable" />
          <div className="hero-overlay" />
          <div className="container hero-content">
            <p className="hero-tag">Phase 1 Demo</p>
            <h1 id="hero-title">{college.tagline}</h1>
            <p>{college.aboutText}</p>
            <div className="hero-actions">
              <a href="#about" className="button-link button-primary">
                <span>Explore College</span>
                <ArrowRight size={16} />
              </a>
              <Link to="/login" className="button-link button-secondary">
                <LogIn size={16} />
                <span>Login Portal</span>
              </Link>
            </div>
          </div>
        </section>

        <section className="section" id="about" aria-labelledby="about-title">
          <div className="container">
            <h2 id="about-title">About Our College</h2>
            <p>{college.aboutText}</p>
            <div className="card-grid">
              {college.stats.map((stat) => (
                <StatCard key={stat.label} stat={stat} />
              ))}
            </div>
          </div>
        </section>

        <section className="section section-muted" aria-labelledby="principal-title">
          <div className="container principal-card">
            <ImageWithFallback
              src={college.principal.image}
              alt="Principal placeholder"
              className="principal-image"
              fallbackText="Principal photo placeholder"
            />
            <div>
              <h2 id="principal-title">Principal's Message</h2>
              <h3>{college.principal.name}</h3>
              <p className="section-note">{college.principal.designation}</p>
              <p>{college.principal.message}</p>
            </div>
          </div>
        </section>

        <section className="section" id="departments" aria-labelledby="departments-title">
          <div className="container">
            <h2 id="departments-title">Departments</h2>
            <p className="section-note">{college.departmentsNote}</p>
            <div className="card-grid">
              {college.departments.map((department) => (
                <DepartmentCard key={department.key} department={department} />
              ))}
            </div>
          </div>
        </section>

        <section className="section section-muted" id="activities" aria-labelledby="activities-title">
          <div className="container">
            <h2 id="activities-title">Campus Life & Activities</h2>
            <p className="section-note">{college.activitiesNote}</p>
            <ul className="activity-list">
              {college.activities.map((activity) => (
                <li key={activity}>{activity}</li>
              ))}
            </ul>
          </div>
        </section>

        <GalleryGrid gallery={college.gallery} note={college.galleryNote} />
        <NoticeList notices={college.notices} note={college.noticesNote} />
      </main>

      <Footer college={college} />
    </>
  );
}

export default HomePage;
