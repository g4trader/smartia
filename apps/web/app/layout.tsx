import '../styles/globals.css';

export const metadata = { 
  title: 'SmartIA WhatsApp Agents',
  description: 'Agentes de IA no WhatsApp que vendem, atendem e reativam clientes'
};

export default function RootLayout({children}:{children:React.ReactNode}){
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
