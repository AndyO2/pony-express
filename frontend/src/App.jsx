import { QueryClient, QueryClientProvider } from "react-query";
import { BrowserRouter, Navigate, Routes, Route } from "react-router-dom";
import "./App.css";

const queryClient = new QueryClient();

function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <BrowserRouter>
                <Routes>
                    <Route
                        path="/"
                        element={<h1>placeholder</h1>}
                    />
                    <Route
                        path="/chats"
                        element={<h1>/chats</h1>}
                    />
                    <Route
                        path="/chats/:chatId"
                        element={<h1>/chats/chatId</h1>}
                    />
                </Routes>
            </BrowserRouter>
        </QueryClientProvider>
    );
}

export default App;
