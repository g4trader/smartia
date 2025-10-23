import React from 'react';

interface HeroProps {
  title: string;
  subtitle: string;
  primaryCta: { text: string; href: string };
  secondaryCta: { text: string; href: string };
}

export default function Hero({ title, subtitle, primaryCta, secondaryCta }: HeroProps) {
  return (
    <section style={{ maxWidth: 960, margin: '40px auto', padding: '0 16px' }}>
      <h1 style={{ fontSize: 40, lineHeight: 1.1, marginBottom: 16 }}>
        {title}
      </h1>
      <p style={{ fontSize: 18, opacity: 0.85 }}>
        {subtitle}
      </p>
      <div style={{ display: 'flex', gap: 12, marginTop: 24, flexWrap: 'wrap' }}>
        <a 
          href={primaryCta.href} 
          style={{ 
            padding: '12px 16px', 
            background: '#111', 
            color: '#fff', 
            borderRadius: 8, 
            textDecoration: 'none',
            display: 'inline-block'
          }}
        >
          {primaryCta.text}
        </a>
        <a 
          href={secondaryCta.href} 
          style={{ 
            padding: '12px 16px', 
            border: '1px solid #111', 
            borderRadius: 8, 
            textDecoration: 'none',
            display: 'inline-block'
          }}
        >
          {secondaryCta.text}
        </a>
      </div>
    </section>
  );
}
