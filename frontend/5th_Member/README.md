
# 5th Member Frontend

A modern, lightweight frontend built with **React (Vite)** and **Material UI**, serving as the user interface for the **5th Member** system — a personal AI platform powered by **Ollama**, **Qdrant**, and **FastAPI**.

---

## Features

*  **User Authentication** — Simple modal-based login system (username & password).
*  **Fast & Lightweight** — Built with **Vite** for blazing-fast development and builds.
*  **Material UI** — Clean, responsive design components.
*  **AI Integration** — Connects with backend AI logic using REST API.
*  **Modular Codebase** — Easy to extend for chat, RAG, or other AI tools.

---

## Tech Stack

| Layer              | Technology                                                    |
| ------------------ | ------------------------------------------------------------- |
| Frontend Framework | [React](https://react.dev/) (via [Vite](https://vitejs.dev/)) |
| UI Library         | [Material UI](https://mui.com/)                               |
| State Management   | React Hooks                                                   |
| API Communication  | Axios                                                         |
| Styling            | MUI theme customization                                       |
| Deployment         | Docker / Vercel / Netlify ready                               |

---

## Folder Structure

```
5th_Member/
│
├── src/
│   ├── components/
│   │   ├── Login.tsx
│   │   ├── ProfileMenu.tsx
│   │   └── ...
│   ├── App.tsx
│   ├── main.tsx
│   ├── Orb.tsx
│   └── ...
│ 
├── package.json
└── vite.config.js
```

---

## Setup & Installation


### 1. Install Dependencies

```bash
npm install
```

### 2. Run Development Server

```bash
npm run dev
```

Then open → [http://localhost:5173](http://localhost:5173)

---

## API Integration

The frontend connects to your FastAPI backend at:

```
POST /api/register
POST /api/login
```

These endpoints handle user registration and authentication, using **Qdrant** as a storage layer for user data.

---

## Docker (Optional)

You can easily containerize your frontend:

```bash
docker build -t 5thMember-frontend .
docker run -p 5173:80 5thMember-frontend
```

---

## Future Plans

* Integrate **chat interface** with Ollama text model
* Add **session memory** and **contextual history**
* Dark/light mode support
* Role-based dashboard

---

## Contributing

Pull requests and feedback are always welcome!
To contribute:

```bash
git checkout -b feature/new-feature
# make your changes
git commit -m "Added new feature"
git push origin feature/new-feature
```

---

## Author

**Utsav Acharya**

> Creator of 5th Member
>  Python • FastAPI • React • AI • Docker

---

## License

This project is open-source under the **MIT License**.
