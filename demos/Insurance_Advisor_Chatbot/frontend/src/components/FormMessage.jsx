import { useState } from 'react'
import ReactMarkdown from 'react-markdown'

function FormMessage({ text, fields, onSubmit }) {
  const [formData, setFormData] = useState({});
  
  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };
  
  const handleSubmit = () => {
    onSubmit(formData);
  };
  
  return (
    <div className="message bot" style={{ width: '100%' }}>
      <ReactMarkdown>{text}</ReactMarkdown>
      <div className="custom-form" style={{ marginTop: '1rem', background: '#f9fafb', padding: '1rem', borderRadius: '12px', border: '1px solid #e5e7eb' }}>
        {fields.map((field, index) => (
          <div key={index} style={{ marginBottom: '0.75rem' }}>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', marginBottom: '0.25rem', color: '#374151' }}>{field}</label>
            <input 
              type="text" 
              placeholder={`Enter ${field}`} 
              style={{ width: '100%', padding: '0.5rem', borderRadius: '8px', border: '1px solid #d1d5db', boxSizing: 'border-box' }}
              value={formData[field] || ''}
              onChange={(e) => handleChange(field, e.target.value)}
            />
          </div>
        ))}
        <button 
          className="btn-primary" 
          style={{ width: '100%', padding: '0.75rem', borderRadius: '8px', fontWeight: '600', marginTop: '0.5rem' }}
          onClick={handleSubmit}
        >
          Submit Details
        </button>
      </div>
    </div>
  );
}

export default FormMessage;
