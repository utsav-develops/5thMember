import { useState } from 'react'
import './App.css'
import Orb from './Orb';
import { ThemeProvider, createTheme, useColorScheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Input from '@mui/material/Input';
import SendRoundedIcon from '@mui/icons-material/SendRounded';
import { Button, CircularProgress, Typography  } from '@mui/material';
import Box from '@mui/material/Box';
import Avatar from '@mui/material/Avatar';
import ProfileMenu from './components/ProfileMenu';
import Login from './components/Login';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

function App() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [loginDialog, setLoginDialog] = useState(false);
  const [response, setResponse] = useState('');
  const [user, setUser] = useState<{ username: string } | null>(
    JSON.parse(localStorage.getItem('user') || 'null')
  );

  const handleLogin = (username: string) => {
    setUser({ username });
  };

  console.log(user);  

  const handleLogout = () => {
    localStorage.removeItem('user');
    setUser(null);
  };

  const runApi = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setText('');
    setResponse("");

    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: text, user_id: user?.username }),
    });

    if (!res.body) {
      throw new Error('Response body is null');
    }
    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      setResponse((prev) => prev + chunk);
    }

    setLoading(false);
  }

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
    <>



    <div style={{position: 'absolute', top: '20px', left: '20px', color: 'inherit', fontSize: '14px', opacity: 0.7}}>
      Powered by <u>5th Member</u>
    </div>
    <text style={{position: 'absolute', top: '10px', right: '10px', color: 'inherit', fontSize: '12px', opacity: 0.5}}>
      v0.0.1
    </text>
    <div style={{position: 'absolute', bottom: '10px', right: '10px', color: 'inherit', fontSize: '12px', }} >
        {user ? (
        <>
          {/* <Typography variant="h6">Welcome, {user.username}</Typography> */}
          <Avatar alt={user.username} src="/avatar.jpg" sx={{ width: 50, height: 50, marginLeft: '10px' }}/>
          <Button onClick={handleLogout}>Logout</Button>
        </>
      ) : (
        <Button variant="contained" onClick={() => setLoginDialog(true)}>
          Login
        </Button>
      )}
    </div>
    <div className="body" style={{justifyContent: 'center', alignItems: 'center', display: 'flex', flexDirection: 'column', height: '80vh', width: '60vw',}}>

        <Orb
          hoverIntensity={0.5}
          rotateOnHover={true}
          hue={0.5}
          forceHoverState={loading}
        />
        <Box
          sx={{
            width: '100%',
            padding: 2,
            borderRadius: 4,
            borderColor: 'primary.main',
            borderWidth: 1.5,
            borderStyle: 'solid',
          }}
      >
        <Input disabled={!user} style={{width: '100%'}} placeholder="Ask me anything...." value={text} onChange={(e) => setText(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && runApi()}/>
        <div style={{justifyContent:'space-between', flexDirection:'row', display:'flex', marginTop:'10px'}}>
          <div> 
            <text>
              {user ? 
                response || (loading ? "Thinking..." : "Response will appear here")
              : "Please login so that The 5th Member can assist you :)"}
            </text> 
            </div>
            {loading ? 
              <Button 
                sx={{
                width: 60,
                height: 48,
                minWidth: 48,
                borderRadius: 2, // 🔳 makes it square
              }}
              variant = "contained" disabled>
                <CircularProgress size={24} color='inherit' />
              </Button>
            :
              <Button variant = "contained"
                sx={{
                width: 60,
                height: 48,
                minWidth: 48,
                borderRadius: 2, // 🔳 makes it square
              }}
              disabled={!user}
              > 
                <SendRoundedIcon fontSize='medium' onClick={runApi}/>
              </Button>
            }
          
        </div>

      </Box>
      </div>
        <Login open={loginDialog} onClose={() => setLoginDialog(false)} onLogin={handleLogin} />
    </>
    </ThemeProvider>

  )
}

export default App
