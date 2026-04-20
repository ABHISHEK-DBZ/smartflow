
import React, { useState } from 'react';

const TRIVIA_QUESTIONS = [
  { q: "Which team holds the record for most home wins this season?", options: ["Lions", "Tigers", "Bears", "Eagles"], a: "Lions" },
  { q: "What year did this stadium officially open?", options: ["1998", "2005", "2012", "2020"], a: "2012" }
];

export default function LiveTrivia({ onEarnPoints }) {
  const [currentQ, setCurrentQ] = useState(0);
  const [answered, setAnswered] = useState(false);
  const [correct, setCorrect] = useState(false);

  if (currentQ >= TRIVIA_QUESTIONS.length) {
    return (
      <div className="glass stagger-5" style={{ padding: '16px 20px', marginBottom: '24px', textAlign: 'center' }}>
        <div style={{ fontSize: '24px', marginBottom: '8px' }}>🎉</div>
        <p style={{ color: 'var(--cyan)', fontWeight: 700 }}>All trivia completed!</p>
        <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Check back later for more questions</p>
      </div>
    );
  }

  const question = TRIVIA_QUESTIONS[currentQ];

  const handleAnswer = (opt) => {
    if (answered) return;
    const isCorrect = opt === question.a;
    setCorrect(isCorrect);
    setAnswered(true);
    if (isCorrect && onEarnPoints) onEarnPoints(50);
    setTimeout(() => {
      setAnswered(false);
      setCurrentQ(q => q + 1);
    }, 2000);
  };

  return (
    <div className="glass stagger-5" aria-label="Game Day Trivia" style={{ padding: '16px 20px', marginBottom: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '13px', letterSpacing: '3px', color: 'var(--text-muted)', textTransform: 'uppercase', margin: 0 }}>
          🧠 GAME DAY TRIVIA
        </h2>
        <span style={{ fontSize: '11px', color: 'var(--cyan)' }}>Earn 50 Pts</span>
      </div>
      
      <p style={{ fontSize: '14px', fontWeight: 600, marginBottom: '16px', lineHeight: 1.4 }}>{question.q}</p>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
        {question.options.map(opt => {
          let bg = 'rgba(255,255,255,0.05)';
          let border = '1px solid var(--border)';
          if (answered) {
            if (opt === question.a) {
              bg = 'rgba(0,255,136,0.15)';
              border = '1px solid var(--green)';
            } else if (!correct && opt !== question.a) {
              bg = 'rgba(255,71,87,0.15)';
              border = '1px solid var(--red)';
            }
          }
          
          return (
            <button
              key={opt}
              onClick={() => handleAnswer(opt)}
              disabled={answered}
              style={{
                padding: '12px',
                background: bg,
                border,
                borderRadius: '8px',
                color: 'var(--text)',
                cursor: answered ? 'default' : 'pointer',
                fontSize: '13px',
                transition: 'all 0.2s',
                textAlign: 'center'
              }}
            >
              {opt}
            </button>
          );
        })}
      </div>
      
      {answered && (
        <div style={{ marginTop: '12px', textAlign: 'center', fontSize: '12px', color: correct ? 'var(--green)' : 'var(--red)', fontWeight: 700 }}>
          {correct ? '+50 Fan Score! 🎉' : 'Incorrect! Better luck next time.'}
        </div>
      )}
    </div>
  );
}
