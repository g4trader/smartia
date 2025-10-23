import React from 'react';

interface SmartIASprintProps {
  title: string;
  description: string;
  features: string[];
  guarantee: string;
}

export default function SmartIASprint({ title, description, features, guarantee }: SmartIASprintProps) {
  return (
    <section id="smart-ia-sprint" style={{ maxWidth: 960, margin: '40px auto', padding: '0 16px' }}>
      <div style={{ 
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 
        borderRadius: 16, 
        padding: 40, 
        color: '#fff',
        textAlign: 'center'
      }}>
        <h2 style={{ fontSize: 32, marginBottom: 16, fontWeight: 700 }}>
          {title}
        </h2>
        <p style={{ fontSize: 18, opacity: 0.9, marginBottom: 32, lineHeight: 1.6 }}>
          {description}
        </p>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 24, marginBottom: 32 }}>
          {features.map((feature, index) => (
            <div key={index} style={{ textAlign: 'left' }}>
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                marginBottom: 8 
              }}>
                <div style={{ 
                  width: 20, 
                  height: 20, 
                  background: '#fff', 
                  borderRadius: '50%', 
                  marginRight: 12,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: 12,
                  fontWeight: 'bold',
                  color: '#667eea'
                }}>
                  ✓
                </div>
                <span style={{ fontSize: 16, fontWeight: 600 }}>
                  {feature}
                </span>
              </div>
            </div>
          ))}
        </div>

        <div style={{ 
          background: 'rgba(255, 255, 255, 0.1)', 
          borderRadius: 12, 
          padding: 20,
          border: '1px solid rgba(255, 255, 255, 0.2)'
        }}>
          <h3 style={{ fontSize: 18, marginBottom: 8, fontWeight: 600 }}>
            🛡️ Garantia de Entrega
          </h3>
          <p style={{ fontSize: 14, opacity: 0.9, margin: 0 }}>
            {guarantee}
          </p>
        </div>
      </div>
    </section>
  );
}
