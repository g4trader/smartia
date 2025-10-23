import React from 'react';

interface ComoFuncionaProps {
  steps: string[];
}

export default function ComoFunciona({ steps }: ComoFuncionaProps) {
  return (
    <section id="como-funciona" style={{ maxWidth: 960, margin: '40px auto', padding: '0 16px' }}>
      <h2 style={{ fontSize: 32, marginBottom: 24 }}>Como funciona</h2>
      <ol style={{ fontSize: 16, lineHeight: 1.6, paddingLeft: 20 }}>
        {steps.map((step, index) => (
          <li key={index} style={{ marginBottom: 16 }}>
            {step}
          </li>
        ))}
      </ol>
    </section>
  );
}
