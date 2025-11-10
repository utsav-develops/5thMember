import { useState } from 'react';
import { Menu, MenuItem, IconButton, Avatar } from '@mui/material';

export default function ProfileMenu() {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
  const userId =  localStorage.getItem('userId');

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <>
      <IconButton onClick={handleClick} size="small" sx={{ ml: 2 }}>
        <Avatar alt={userId || "User"} src="/avatar.jpg" />
      </IconButton>
      <Menu
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
        PaperProps={{
          elevation: 4,
          sx: { mt: 1, minWidth: 150 }
        }}
      >
        <MenuItem onClick={handleClose}>Utsav</MenuItem>
        <MenuItem onClick={handleClose}>Sushant</MenuItem>
        <MenuItem onClick={handleClose}>Rajesh</MenuItem>
      </Menu>
    </>
  );
}
