'use client';
import {useState, useEffect} from 'react';

type Agent = 'sdr'|'ecom'|'auto'|'rfm';
type Message = {
  from: 'user'|'bot';
  text: string;
  timestamp: string;
  state?: string;
};

const AGENT_DESCRIPTIONS = {
  sdr: 'Agent SDR - Qualificação de leads e vendas',
  ecom: 'Agent E-commerce - FAQ e vendas online',
  auto: 'Agent Autoatendimento - Agendamentos e CRM',
  rfm: 'Agent RFM - Reativação de clientes'
};

export default function ChatSimulator(){
  const [agent, setAgent] = useState<Agent>('sdr');
  const [messages, setMessages] = useState<Message[]>([
    {from:'bot', text:'Olá! Eu sou seu agente inteligente. Como posso ajudar?', timestamp: new Date().toLocaleTimeString()}
  ]);
  const [input, setInput] = useState('');
  const [currentState, setCurrentState] = useState('initial');
  const [isLoading, setIsLoading] = useState(false);
  const base = process.env.NEXT_PUBLIC_API_BASE || 'https://smartia-api-642830139828.us-central1.run.app';

  // Reset conversation when agent changes
  useEffect(() => {
    setMessages([{from:'bot', text:'Olá! Eu sou seu agente inteligente. Como posso ajudar?', timestamp: new Date().toLocaleTimeString()}]);
    setCurrentState('initial');
  }, [agent]);

  async function send(){
    if(!input.trim() || isLoading) return;
    
    const userMsg: Message = {
      from: 'user', 
      text: input.trim(),
      timestamp: new Date().toLocaleTimeString()
    };
    setMessages(prev=>[...prev, userMsg]);
    setInput('');
    setIsLoading(true);
    
    try{
      const r = await fetch(`${base}/simulate/${agent}`,{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ 
          message: userMsg.text,
          phone: 'demo_user'
        })
      });
      const data = await r.json();
      const botMsg: Message = {
        from: 'bot', 
        text: data.reply || '...',
        timestamp: new Date().toLocaleTimeString(),
        state: data.state
      };
      setMessages(prev=>[...prev, botMsg]);
      setCurrentState(data.state || 'initial');
    }catch(e){
      const errorMsg: Message = {
        from: 'bot',
        text: '[erro de demo]: verifique se a API está rodando',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev=>[...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  }

  function handleKeyPress(e: React.KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  }

  return (
    <div className="card">
      <div className="mb-4">
        <h3 className="text-lg font-semibold mb-2">{AGENT_DESCRIPTIONS[agent]}</h3>
        <div className="flex gap-2 mb-2">
          {(['sdr','ecom','auto','rfm'] as Agent[]).map(a=>(
            <button 
              key={a} 
              onClick={()=>setAgent(a)} 
              className={`badge ${agent===a?'ring-2 ring-blue-400 bg-blue-500':'hover:bg-slate-700'}`}
            >
              {a.toUpperCase()}
            </button>
          ))}
        </div>
        <div className="text-sm text-slate-400">
          Estado atual: <span className="font-mono bg-slate-800 px-2 py-1 rounded">{currentState}</span>
        </div>
      </div>
      
      <div className="h-64 overflow-y-auto border border-slate-700 rounded-lg p-3 bg-[#0e142a] mb-3">
        {messages.map((m,i)=>(
          <div key={i} className={`my-2 ${m.from==='user'?'text-right':''}`}>
            <div className={`inline-block px-3 py-2 rounded-xl max-w-[80%] ${m.from==='user'?'bg-blue-500 text-white':'bg-slate-800 text-slate-100'}`}>
              {m.text}
            </div>
            <div className={`text-xs text-slate-500 mt-1 ${m.from==='user'?'text-right':''}`}>
              {m.timestamp.toLocaleTimeString()}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="my-2">
            <div className="inline-block px-3 py-2 rounded-xl bg-slate-800 text-slate-100">
              <span className="animate-pulse">Digitando...</span>
            </div>
          </div>
        )}
      </div>
      
      <div className="flex gap-2">
        <input 
          value={input} 
          onChange={e=>setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Digite sua mensagem..." 
          className="flex-1 bg-slate-900 text-slate-100 rounded-md px-3 py-2 border border-slate-700 focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
          disabled={isLoading}
        />
        <button 
          onClick={send} 
          className="btn"
          disabled={isLoading || !input.trim()}
        >
          {isLoading ? '...' : 'Enviar'}
        </button>
      </div>
    </div>
  )
}
