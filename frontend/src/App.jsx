import { QueryClient, QueryClientProvider } from "react-query";
import { BrowserRouter, Navigate, Routes, Route } from "react-router-dom";
import "./App.css";
import Chats from "./components/Chats";
import { AuthProvider, useAuth } from "./context/auth";
import { UserProvider } from "./context/user";
import Profile from "./components/Profile";
import Registration from "./components/Registration";
import Login from "./components/Login";
import TopNav from "./components/TopNav";

// TO RUN:
// cd frontend
// npm run dev

const queryClient = new QueryClient();

function NotFound() {
    return <h1>404: not found</h1>;
}

function Home() {
    const { isLoggedIn, logout } = useAuth();

    return (
        <div className="max-w-4/5 mx-auto text-center px-4 py-8">
            <div className="py-2">logged in: {isLoggedIn.toString()}</div>
        </div>
    );
}

function Header() {
    return (
        <header>
            <TopNav />
        </header>
    );
}

function AuthenticatedRoutes() {
    return (
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
                path="/profile"
                element={<Profile />}
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
    );
}

function UnauthenticatedRoutes() {
    return (
        <Routes>
            <Route
                path="/"
                element={<Home />}
            />
            <Route
                path="/login"
                element={<Login />}
            />
            <Route
                path="/register"
                element={<Registration />}
            />
            <Route
                path="*"
                element={<Navigate to="/login" />}
            />
        </Routes>
    );
}

function Main() {
    const { isLoggedIn } = useAuth();

    return <main className="max-h-main">{isLoggedIn ? <AuthenticatedRoutes /> : <UnauthenticatedRoutes />}</main>;
}

function App() {
    const className = ["h-screen max-h-screen", "max-w-2xl mx-auto", "bg-gray-700 text-white", "flex flex-col"].join(" ");
    return (
        <QueryClientProvider client={queryClient}>
            <AuthProvider>
                <BrowserRouter>
                    <UserProvider>
                        <div className={className}>
                            <Header />
                            <Main />
                        </div>
                    </UserProvider>
                </BrowserRouter>
            </AuthProvider>
        </QueryClientProvider>
    );
}

export default App;
