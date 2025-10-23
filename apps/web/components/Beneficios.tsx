import React from 'react';

interface Beneficio {
  title: string;
  description: string;
}

interface BeneficiosProps {
  beneficios: Beneficio[];
}

export default function Beneficios({ beneficios }: BeneficiosProps) {
  return (
    <section id="beneficios" style={{ maxWidth: 960, margin: '40px auto', padding: '0 16px' }}>
      <h2 style={{ fontSize: 32, marginBottom: 24 }}>Benefícios imediatos</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 20 }}>
        {beneficios.map((beneficio, index) => (
          <div key={index} style={{ padding: 20, border: '1px solid #eee', borderRadius: 12 }}>
            <h3 style={{ fontSize: 18, marginBottom: 8, fontWeight: 600 }}>
              {beneficio.title}
            </h3>
            <p style={{ fontSize: 14, opacity: 0.8, lineHeight: 1.5 }}>
              {beneficio.description}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}
