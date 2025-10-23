import Head from 'next/head'
import Hero from '../components/Hero'
import ComoFunciona from '../components/ComoFunciona'
import Beneficios from '../components/Beneficios'
import Planos from '../components/Planos'
import SmartIASprint from '../components/SmartIASprint'
import FAQ from '../components/FAQ'
import CTAWhatsApp from '../components/CTAWhatsApp'

export default function Home() {
  return (
    <>
      <Head>
        <title>Smart IA Solutions – Clínica Inteligente</title>
        <meta name="description" content="Automação com IA para WhatsApp: agenda, confirmações e CRM em um só lugar." />
        
        {/* Open Graph / Facebook */}
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://smartia.com.br/" />
        <meta property="og:title" content="Smart IA Solutions – Clínica Inteligente" />
        <meta property="og:description" content="Automação com IA para WhatsApp: agenda, confirmações e CRM em um só lugar." />
        <meta property="og:image" content="https://smartia.com.br/og-image.jpg" />

        {/* Twitter */}
        <meta property="twitter:card" content="summary_large_image" />
        <meta property="twitter:url" content="https://smartia.com.br/" />
        <meta property="twitter:title" content="Smart IA Solutions – Clínica Inteligente" />
        <meta property="twitter:description" content="Automação com IA para WhatsApp: agenda, confirmações e CRM em um só lugar." />
        <meta property="twitter:image" content="https://smartia.com.br/og-image.jpg" />

        {/* Favicon */}
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
      </Head>
      <main style={{fontFamily:'system-ui, sans-serif'}}>
        <header style={{padding:'24px 16px', borderBottom:'1px solid #eee'}}>
          <div style={{maxWidth:960, margin:'0 auto', display:'flex', justifyContent:'space-between', alignItems:'center'}}>
            <strong>Smart IA Solutions</strong>
            <a href="#contato" style={{padding:'10px 16px', border:'1px solid #000', borderRadius:8, textDecoration:'none'}}>Falar no WhatsApp</a>
          </div>
        </header>

        <Hero 
          title="Transforme sua clínica com IA integrada ao WhatsApp"
          subtitle="Agende, confirme e gerencie pacientes automaticamente. Menos esforço, mais resultado."
          primaryCta={{ text: "Ver planos", href: "#planos" }}
          secondaryCta={{ text: "Como funciona", href: "#como-funciona" }}
        />

        <ComoFunciona 
          steps={[
            "Paciente envia mensagem no WhatsApp e é atendido por um agente virtual 24h.",
            "Ele escolhe um horário disponível e recebe confirmação automática.",
            "Lembretes reduzem faltas; histórico e CRM ficam organizados."
          ]}
        />

        <Beneficios 
          beneficios={[
            { title: "Liberdade", description: "Acabe com a sobrecarga de mensagens e agendamentos." },
            { title: "Organização", description: "Consultas e pacientes em um só lugar." },
            { title: "Pontualidade", description: "Lembretes automáticos reduzem faltas." },
            { title: "Eficiência", description: "Mais consultas realizadas, menos tempo perdido." }
          ]}
        />

        <SmartIASprint 
          title="Smart IA Sprint (30 dias)"
          description="Integração rápida com consultoria + execução completa em 30 dias"
          features={[
            "Análise completa do fluxo atual",
            "Configuração personalizada do agente IA",
            "Integração com sua agenda existente",
            "Treinamento da equipe",
            "Monitoramento e ajustes contínuos"
          ]}
          guarantee="Se não entregarmos o sistema funcionando em 30 dias, devolvemos 100% do investimento."
        />

        <Planos 
          planos={[
            {
              nome: "Setup Inicial",
              descricao: "Implantações e integração do agente IA personalizado",
              preco: "R$ 6.000,00",
              features: [
                "Configuração completa do sistema",
                "Integração com WhatsApp Business",
                "Personalização do fluxo de atendimento",
                "Treinamento da equipe"
              ]
            },
            {
              nome: "Manutenção",
              descricao: "Suporte, ajustes e monitoramento contínuo",
              preco: "R$ 500,00 / mês",
              destacado: true,
              features: [
                "Suporte técnico prioritário",
                "Ajustes e melhorias",
                "Monitoramento 24/7",
                "Relatórios mensais de performance"
              ]
            }
          ]}
        />

        <FAQ 
          title="Perguntas Frequentes"
          faqs={[
            {
              question: "Como funciona a integração com minha agenda atual?",
              answer: "Integramos com Google Calendar, Outlook ou qualquer sistema de agenda. O processo é simples e não interfere no seu fluxo atual de trabalho."
            },
            {
              question: "Qual o prazo para implementação?",
              answer: "O Smart IA Sprint garante implementação completa em 30 dias, incluindo configuração, testes e treinamento da equipe."
            },
            {
              question: "Há suporte mensal incluído?",
              answer: "Sim! O plano de manutenção inclui suporte técnico prioritário, ajustes e monitoramento contínuo do sistema."
            },
            {
              question: "Posso fazer mudanças na agenda depois?",
              answer: "Claro! O sistema se adapta automaticamente às mudanças na sua agenda. Você pode bloquear horários, adicionar novos slots ou modificar disponibilidade a qualquer momento."
            },
            {
              question: "Meus dados dos pacientes estão seguros?",
              answer: "Sim! Utilizamos criptografia de ponta a ponta e seguimos todas as normas de proteção de dados (LGPD). Seus dados ficam seguros e privados."
            },
            {
              question: "O sistema escala conforme minha clínica cresce?",
              answer: "Absolutamente! O sistema foi projetado para crescer com você. Suporta desde clínicas pequenas até grandes redes, com múltiplos profissionais e milhares de pacientes."
            }
          ]}
        />

        <CTAWhatsApp 
          title="Pronto para começar?"
          subtitle="Converse com nosso atendimento por IA no WhatsApp."
          buttonText="Abrir WhatsApp"
          whatsappNumber={process.env.NEXT_PUBLIC_WHATSAPP_NUMBER}
        />

        <footer style={{padding:'24px 16px', borderTop:'1px solid #eee'}}>
          <div style={{maxWidth:960, margin:'0 auto', fontSize:12, opacity:.7}}>
            © {new Date().getFullYear()} Smart IA Solutions
          </div>
        </footer>
      </main>
    </>
  )
}
