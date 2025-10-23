import Head from 'next/head'

export default function Home() {
  return (
    <>
      <Head>
        <title>Smart IA Solutions – Clínica Inteligente</title>
        <meta name="description" content="Automação com IA para WhatsApp: agenda, confirmações e CRM em um só lugar." />
      </Head>
      <main style={{fontFamily:'system-ui, sans-serif'}}>
        <header style={{padding:'24px 16px', borderBottom:'1px solid #eee'}}>
          <div style={{maxWidth:960, margin:'0 auto', display:'flex', justifyContent:'space-between', alignItems:'center'}}>
            <strong>Smart IA Solutions</strong>
            <a href="#contato" style={{padding:'10px 16px', border:'1px solid #000', borderRadius:8, textDecoration:'none'}}>Falar no WhatsApp</a>
          </div>
        </header>

        <section style={{maxWidth:960, margin:'40px auto', padding:'0 16px'}}>
          <h1 style={{fontSize:40, lineHeight:1.1, marginBottom:16}}>Transforme sua clínica com IA integrada ao WhatsApp</h1>
          <p style={{fontSize:18, opacity:.85}}>
            Agende, confirme e gerencie pacientes automaticamente. Menos esforço, mais resultado.
          </p>
          <div style={{display:'flex', gap:12, marginTop:24}}>
            <a href="#planos" style={{padding:'12px 16px', background:'#111', color:'#fff', borderRadius:8, textDecoration:'none'}}>Ver planos</a>
            <a href="#como-funciona" style={{padding:'12px 16px', border:'1px solid #111', borderRadius:8, textDecoration:'none'}}>Como funciona</a>
          </div>
        </section>

        <section id="como-funciona" style={{maxWidth:960, margin:'40px auto', padding:'0 16px'}}>
          <h2>Como funciona</h2>
          <ol>
            <li>Paciente envia mensagem no WhatsApp e é atendido por um agente virtual 24h.</li>
            <li>Ele escolhe um horário disponível e recebe confirmação automática.</li>
            <li>Lembretes reduzem faltas; histórico e CRM ficam organizados.</li>
          </ol>
        </section>

        <section id="beneficios" style={{maxWidth:960, margin:'40px auto', padding:'0 16px'}}>
          <h2>Benefícios imediatos</h2>
          <ul>
            <li>Liberdade: acabe com a sobrecarga de mensagens e agendamentos.</li>
            <li>Organização: consultas e pacientes em um só lugar.</li>
            <li>Pontualidade: lembretes automáticos reduzem faltas.</li>
            <li>Eficiência: mais consultas realizadas, menos tempo perdido.</li>
          </ul>
        </section>

        <section id="planos" style={{maxWidth:960, margin:'40px auto', padding:'0 16px'}}>
          <h2>Planos</h2>
          <div style={{display:'grid', gridTemplateColumns:'repeat(auto-fit, minmax(260px, 1fr))', gap:16}}>
            <div style={{border:'1px solid #eee', borderRadius:12, padding:16}}>
              <h3>Setup Inicial</h3>
              <p>Implantação e integração do agente.</p>
              <strong>R$ 6.000,00</strong>
            </div>
            <div style={{border:'1px solid #eee', borderRadius:12, padding:16}}>
              <h3>Manutenção</h3>
              <p>Suporte, ajustes e monitoramento.</p>
              <strong>R$ 500,00 / mês</strong>
            </div>
          </div>
        </section>

        <section id="contato" style={{maxWidth:960, margin:'40px auto', padding:'0 16px'}}>
          <h2>Pronto para começar?</h2>
          <p>Converse com nosso atendimento por IA no WhatsApp.</p>
          <a href={process.env.NEXT_PUBLIC_WHATSAPP_NUMBER ? `https://api.whatsapp.com/send?phone=${process.env.NEXT_PUBLIC_WHATSAPP_NUMBER.replace('+','')}` : '#'} style={{padding:'12px 16px', background:'#25D366', color:'#fff', borderRadius:8, textDecoration:'none'}}>Abrir WhatsApp</a>
        </section>

        <footer style={{padding:'24px 16px', borderTop:'1px solid #eee'}}>
          <div style={{maxWidth:960, margin:'0 auto', fontSize:12, opacity:.7}}>
            © {new Date().getFullYear()} Smart IA Solutions
          </div>
        </footer>
      </main>
    </>
  )
}
