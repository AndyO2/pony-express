import { QueryClient, QueryClientProvider } from "react-query";
import { BrowserRouter, Navigate, Routes, Route } from "react-router-dom";
import "./App.css";
import Chats from "./components/Chats";

const queryClient = new QueryClient();

function NotFound() {
    return <h1>404: not found</h1>;
}

function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <BrowserRouter>
                <Routes>
                    <Route
                        path="/"
                        element={<Chats></Chats>}
                    />
                    <Route
                        path="/chats"
                        element={<Chats></Chats>}
                    />
                    <Route
                        path="/chats/:chatId"
                        element={<Chats></Chats>}
                    />
                    <Route
                        path="/error/404"
                        element={<NotFound />}
                    />
                    <Route
                        path="*"
                        element={<Navigate to="/error/404" />}
                    />
                </Routes>
            </BrowserRouter>
        </QueryClientProvider>
    );
}

export default App;
