import React, { useState } from 'react';

interface FAQItem {
  question: string;
  answer: string;
}

interface FAQProps {
  title: string;
  faqs: FAQItem[];
}

export default function FAQ({ title, faqs }: FAQProps) {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const toggleFAQ = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <section id="faq" style={{ maxWidth: 960, margin: '40px auto', padding: '0 16px' }}>
      <h2 style={{ fontSize: 32, marginBottom: 32, textAlign: 'center' }}>
        {title}
      </h2>
      <div style={{ maxWidth: 800, margin: '0 auto' }}>
        {faqs.map((faq, index) => (
          <div 
            key={index} 
            style={{ 
              border: '1px solid #eee', 
              borderRadius: 8, 
              marginBottom: 12,
              overflow: 'hidden'
            }}
          >
            <button
              onClick={() => toggleFAQ(index)}
              style={{
                width: '100%',
                padding: '20px',
                background: '#fff',
                border: 'none',
                textAlign: 'left',
                cursor: 'pointer',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                fontSize: 16,
                fontWeight: 600
              }}
            >
              <span>{faq.question}</span>
              <span style={{ 
                fontSize: 20, 
                transform: openIndex === index ? 'rotate(45deg)' : 'rotate(0deg)',
                transition: 'transform 0.2s ease'
              }}>
                +
              </span>
            </button>
            {openIndex === index && (
              <div style={{ 
                padding: '0 20px 20px 20px', 
                background: '#f9f9f9',
                fontSize: 14,
                lineHeight: 1.6,
                opacity: 0.8
              }}>
                {faq.answer}
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}
