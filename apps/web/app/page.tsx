import ChatSimulator from '@/components/ChatSimulator';

export default function Page(){
  return (
    <main>
      {/* Hero Section */}
      <section className="container">
        <div className="card mb-6">
          <div className="flex flex-col gap-2">
            <span className="badge">SmartIA – WhatsApp Agents</span>
            <h1 className="text-4xl font-bold">Agentes de IA no WhatsApp que vendem, atendem e reativam clientes</h1>
            <p className="text-slate-300 max-w-2xl">
              Demonstração completa de como nossos agentes conversacionais integram vendas, atendimento e dados – com visual de alta tecnologia e fluxo lógico de ponta a ponta.
            </p>
            <div className="flex gap-3 mt-2">
              <a href="#demo" className="btn">Ver demonstração</a>
              <a href="#planos" className="btn" style={{background:'#1f2937', color:'#e5e7eb'}}>Falar com especialista</a>
            </div>
          </div>
        </div>
      </section>

      {/* Provas Section */}
      <section className="container mb-8">
        <h2 className="text-2xl font-bold mb-4">Resultados Comprovados</h2>
        <div className="grid md:grid-cols-3 gap-4">
          {[
            {metric: '+300%', desc: 'Aumento na qualificação de leads'},
            {metric: '85%', desc: 'Redução no tempo de resposta'},
            {metric: 'R$ 2.5M', desc: 'Vendas geradas em 6 meses'}
          ].map((x,i)=>(
            <div className="card text-center" key={i}>
              <div className="text-3xl font-bold text-blue-400 mb-2">{x.metric}</div>
              <p className="text-slate-300">{x.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Produtos Section */}
      <section className="container mb-8">
        <h2 className="text-2xl font-bold mb-4">Nossos Agentes Inteligentes</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            {
              title:'Agent SDR',
              desc:'Qualifica leads e entrega oportunidades quentes ao time de vendas.',
              features:['Qualificação automática', 'Scoring de leads', 'Agendamento de calls'],
              color: 'bg-blue-500'
            },
            {
              title:'Agent E‑commerce',
              desc:'Responde FAQ, apresenta catálogo e conclui vendas por link.',
              features:['Catálogo inteligente', 'Checkout por link', 'FAQ dinâmica'],
              color: 'bg-green-500'
            },
            {
              title:'Agent Autoatendimento',
              desc:'Agenda, confirma, integra com CRM e envia pagamentos.',
              features:['Agendamento automático', 'Integração CRM', 'Pagamentos'],
              color: 'bg-purple-500'
            },
            {
              title:'Agent RFM',
              desc:'Segmenta por comportamento e reativa bases adormecidas.',
              features:['Segmentação RFM', 'Campanhas personalizadas', 'Reativação'],
              color: 'bg-orange-500'
            },
          ].map((x,i)=>(
            <div className="card" key={i}>
              <div className={`w-12 h-12 ${x.color} rounded-lg mb-3 flex items-center justify-center`}>
                <span className="text-white font-bold">{x.title.split(' ')[1]}</span>
              </div>
              <h3 className="font-semibold mb-2">{x.title}</h3>
              <p className="text-slate-300 mb-3">{x.desc}</p>
              <ul className="text-sm text-slate-400 space-y-1">
                {x.features.map((feature, idx) => (
                  <li key={idx} className="flex items-center">
                    <span className="w-1 h-1 bg-blue-400 rounded-full mr-2"></span>
                    {feature}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      {/* Demo Section */}
      <section id="demo" className="container mb-8">
        <h2 className="text-2xl font-bold mb-2">Demonstração Interativa</h2>
        <p className="text-slate-300 mb-4">Simule uma conversa e veja como cada agente responde com state machine inteligente.</p>
        <ChatSimulator/>
      </section>

      {/* Planos Section */}
      <section id="planos" className="container mb-8">
        <h2 className="text-2xl font-bold mb-4">Planos e Investimento</h2>
        <div className="grid md:grid-cols-3 gap-4">
          {[
            {
              name: 'Starter',
              price: 'R$ 2.997',
              period: '/mês',
              features: ['1 Agente', 'Até 1.000 conversas', 'Suporte básico', 'Relatórios simples'],
              popular: false
            },
            {
              name: 'Professional',
              price: 'R$ 4.997',
              period: '/mês',
              features: ['3 Agentes', 'Até 5.000 conversas', 'Suporte prioritário', 'Relatórios avançados', 'Integração CRM'],
              popular: true
            },
            {
              name: 'Enterprise',
              price: 'Sob consulta',
              period: '',
              features: ['Agentes ilimitados', 'Conversas ilimitadas', 'Suporte dedicado', 'Customizações', 'SLA garantido'],
              popular: false
            }
          ].map((plan, i) => (
            <div className={`card relative ${plan.popular ? 'ring-2 ring-blue-500' : ''}`} key={i}>
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                  <span className="bg-blue-500 text-white px-3 py-1 rounded-full text-sm">Mais Popular</span>
                </div>
              )}
              <h3 className="text-xl font-bold mb-2">{plan.name}</h3>
              <div className="mb-4">
                <span className="text-3xl font-bold">{plan.price}</span>
                <span className="text-slate-400">{plan.period}</span>
              </div>
              <ul className="space-y-2 mb-4">
                {plan.features.map((feature, idx) => (
                  <li key={idx} className="flex items-center text-slate-300">
                    <span className="w-4 h-4 bg-green-500 rounded-full mr-2 flex items-center justify-center">
                      <span className="text-white text-xs">✓</span>
                    </span>
                    {feature}
                  </li>
                ))}
              </ul>
              <a 
                href="mailto:contato@smartiasolutions.com.br" 
                className={`btn w-full text-center ${plan.popular ? 'bg-blue-500 hover:bg-blue-600' : ''}`}
              >
                {plan.name === 'Enterprise' ? 'Falar com especialista' : 'Começar agora'}
              </a>
            </div>
          ))}
        </div>
      </section>

      {/* FAQ Section */}
      <section className="container mb-8">
        <h2 className="text-2xl font-bold mb-4">Perguntas Frequentes</h2>
        <div className="space-y-4">
          {[
            {
              q: 'Quanto tempo leva para implementar?',
              a: 'A implementação completa leva entre 15-30 dias, incluindo configuração, treinamento e testes.'
            },
            {
              q: 'Preciso de conhecimento técnico?',
              a: 'Não! Nossa equipe cuida de toda a implementação e configuração. Você só precisa fornecer as informações do seu negócio.'
            },
            {
              q: 'Funciona com qualquer CRM?',
              a: 'Sim, integramos com os principais CRMs do mercado: Salesforce, HubSpot, Pipedrive, RD Station e outros.'
            },
            {
              q: 'Como é cobrado?',
              a: 'Cobrança mensal baseada no plano escolhido. Sem taxas de setup ou implementação.'
            }
          ].map((faq, i) => (
            <div className="card" key={i}>
              <h3 className="font-semibold mb-2">{faq.q}</h3>
              <p className="text-slate-300">{faq.a}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mb-8">
        <div className="card text-center bg-gradient-to-r from-blue-600 to-purple-600">
          <h2 className="text-2xl font-bold mb-2">Pronto para revolucionar seu atendimento?</h2>
          <p className="text-slate-200 mb-4">Agende uma demonstração personalizada e veja como nossos agentes podem transformar seu negócio.</p>
          <div className="flex gap-3 justify-center">
            <a href="mailto:contato@smartiasolutions.com.br" className="btn bg-white text-blue-600 hover:bg-gray-100">
              Agendar demonstração
            </a>
            <a href="tel:+5511999999999" className="btn bg-transparent border-2 border-white text-white hover:bg-white hover:text-blue-600">
              Ligar agora
            </a>
          </div>
        </div>
      </section>
    </main>
  )
}
// Deploy test
// Updated for deploy test
