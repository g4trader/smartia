import React from 'react';

interface Plano {
  nome: string;
  descricao: string;
  preco: string;
  destacado?: boolean;
  features?: string[];
}

interface PlanosProps {
  planos: Plano[];
}

export default function Planos({ planos }: PlanosProps) {
  return (
    <section id="planos" style={{ maxWidth: 960, margin: '40px auto', padding: '0 16px' }}>
      <h2 style={{ fontSize: 32, marginBottom: 24, textAlign: 'center' }}>Planos</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 20 }}>
        {planos.map((plano, index) => (
          <div 
            key={index} 
            style={{ 
              border: plano.destacado ? '2px solid #111' : '1px solid #eee', 
              borderRadius: 12, 
              padding: 24,
              position: 'relative',
              background: plano.destacado ? '#f9f9f9' : '#fff'
            }}
          >
            {plano.destacado && (
              <div style={{ 
                position: 'absolute', 
                top: -10, 
                left: '50%', 
                transform: 'translateX(-50%)',
                background: '#111',
                color: '#fff',
                padding: '4px 12px',
                borderRadius: 20,
                fontSize: 12,
                fontWeight: 600
              }}>
                MAIS POPULAR
              </div>
            )}
            <h3 style={{ fontSize: 20, marginBottom: 8, fontWeight: 600 }}>
              {plano.nome}
            </h3>
            <p style={{ fontSize: 14, opacity: 0.8, marginBottom: 16, lineHeight: 1.5 }}>
              {plano.descricao}
            </p>
            {plano.features && (
              <ul style={{ fontSize: 14, marginBottom: 20, paddingLeft: 16 }}>
                {plano.features.map((feature, featureIndex) => (
                  <li key={featureIndex} style={{ marginBottom: 4, opacity: 0.8 }}>
                    {feature}
                  </li>
                ))}
              </ul>
            )}
            <div style={{ fontSize: 24, fontWeight: 700, marginBottom: 16 }}>
              {plano.preco}
            </div>
            <a 
              href="#contato" 
              style={{ 
                display: 'block',
                padding: '12px 16px', 
                background: plano.destacado ? '#111' : 'transparent', 
                color: plano.destacado ? '#fff' : '#111',
                border: '1px solid #111',
                borderRadius: 8, 
                textDecoration: 'none',
                textAlign: 'center',
                fontWeight: 600
              }}
            >
              Escolher plano
            </a>
          </div>
        ))}
      </div>
    </section>
  );
}
