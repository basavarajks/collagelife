import { useState } from 'react';

function ImageWithFallback({ src, alt, className, fallbackText = 'Image unavailable' }) {
  const [hasError, setHasError] = useState(false);

  if (!src || hasError) {
    return (
      <div className={`image-fallback ${className || ''}`} role="img" aria-label={fallbackText}>
        <span>{fallbackText}</span>
      </div>
    );
  }

  return <img src={src} alt={alt} className={className} onError={() => setHasError(true)} />;
}

export default ImageWithFallback;
