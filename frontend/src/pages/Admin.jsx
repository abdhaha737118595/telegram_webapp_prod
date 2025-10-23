import React, { useState } from 'react'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function Admin(){
  const [adminId, setAdminId] = useState('')
  const [targetId, setTargetId] = useState('')
  const [amount, setAmount] = useState('')
  const [msg, setMsg] = useState('')

  async function doTopup(){
    try{
      const res = await axios.post(API_BASE + '/api/admin/topup', {
        admin_telegram_id: adminId,
        target_telegram_id: targetId,
        amount: amount,
        note: 'admin topup via UI'
      })
      setMsg('Success: new balance = ' + res.data.new_balance)
    }catch(e){
      setMsg('Error: ' + (e.response?.data?.detail || e.message))
    }
  }

  return (
    <div style={{padding:20,fontFamily:'Arial'}}>
      <h2>Admin Top-up</h2>
      <div style={{marginBottom:8}}>
        <label>Admin Telegram ID: </label>
        <input value={adminId} onChange={e=>setAdminId(e.target.value)} />
      </div>
      <div style={{marginBottom:8}}>
        <label>Target Telegram ID: </label>
        <input value={targetId} onChange={e=>setTargetId(e.target.value)} />
      </div>
      <div style={{marginBottom:8}}>
        <label>Amount: </label>
        <input value={amount} onChange={e=>setAmount(e.target.value)} />
      </div>
      <button onClick={doTopup}>Top-up</button>
      <p>{msg}</p>
    </div>
  )
}
