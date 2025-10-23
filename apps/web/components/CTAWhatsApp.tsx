import React from 'react';

interface CTAWhatsAppProps {
  title: string;
  subtitle: string;
  buttonText: string;
  whatsappNumber?: string;
}

export default function CTAWhatsApp({ title, subtitle, buttonText, whatsappNumber }: CTAWhatsAppProps) {
  const whatsappUrl = whatsappNumber 
    ? `https://api.whatsapp.com/send?phone=${whatsappNumber.replace('+', '')}`
    : '#';

  return (
    <section id="contato" style={{ maxWidth: 960, margin: '40px auto', padding: '0 16px', textAlign: 'center' }}>
      <h2 style={{ fontSize: 32, marginBottom: 16 }}>{title}</h2>
      <p style={{ fontSize: 18, opacity: 0.8, marginBottom: 24 }}>
        {subtitle}
      </p>
      <a 
        href={whatsappUrl} 
        style={{ 
          display: 'inline-block',
          padding: '16px 24px', 
          background: '#25D366', 
          color: '#fff', 
          borderRadius: 8, 
          textDecoration: 'none',
          fontSize: 16,
          fontWeight: 600,
          boxShadow: '0 2px 8px rgba(37, 211, 102, 0.3)'
        }}
      >
        {buttonText}
      </a>
    </section>
  );
}
