import { useState } from 'react';
import {
  Modal,
  Box,
  Typography,
  TextField,
  Button,
  Stack,
} from '@mui/material';

export default function Login({ open, onClose, onLogin }: {
  open: boolean;
  onClose: () => void;
  onLogin: (username: string, password: string) => void;
}) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async () => {
    if (!username || !password) return;
    const res = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: username, password: password }),
    });
    console.log(res);
    if(!res.ok){
      alert(`Login failed: ${res.statusText}`);
      return;
    }
    
    localStorage.setItem('user', JSON.stringify({ username, password }));
    onLogin(username, password);
    onClose();
  };

  const handleRegister = async () => {
    if (!username || !password) return;
    const res = await fetch("http://localhost:8000/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: username, password: password }),
    });
    console.log(res);
    if(!res.ok){
      alert(`Registration Failed: ${res.statusText}`);
      return;
      
    }
    
    alert("Registration Successful! You can now log in.");
  };


  return (
    <Modal open={open} onClose={onClose}>
      <Box
        sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          bgcolor: 'background.paper',
          p: 4,
          borderRadius: 2,
          boxShadow: 24,
          width: 320,
        }}
      >
        <Typography variant="h6" mb={2}>
          Login
        </Typography>
        <Stack spacing={2}>
          <TextField
            label="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            fullWidth
          />
          <TextField
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            fullWidth
          />
          <Button
            variant="contained"
            onClick={handleSubmit}
            fullWidth
            disabled={!username || !password}
          >
            Login
          </Button>
          <Button
            variant="outlined"
            onClick={handleRegister}
            fullWidth
            disabled={!username || !password}
          >
            Register
          </Button>
        </Stack>
      </Box>
    </Modal>
  );
}
