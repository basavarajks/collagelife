import ImageWithFallback from './ImageWithFallback';

function GalleryGrid({ gallery, note }) {
  return (
    <section className="section section-muted" id="gallery" aria-labelledby="gallery-title">
      <div className="container">
        <h2 id="gallery-title">Campus Gallery</h2>
        <p className="section-note">{note}</p>
        <div className="gallery-grid">
          {gallery.length === 0 ? (
            <p className="empty-state">Gallery images are not available.</p>
          ) : (
            gallery.map((image, index) => (
              <figure key={`${image.alt}-${index}`} className="gallery-item">
                <ImageWithFallback src={image.src} alt={image.alt} className="gallery-image" fallbackText="Gallery image unavailable" />
                <figcaption>{image.alt}</figcaption>
              </figure>
            ))
          )}
        </div>
      </div>
    </section>
  );
}

export default GalleryGrid;
