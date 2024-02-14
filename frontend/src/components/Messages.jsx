/* eslint-disable react-hooks/rules-of-hooks */
/* eslint-disable react/prop-types */
import { useQuery } from "react-query";
import "./Messages.css";

function MessagesQueryContainer({ chatId }) {
    if (!chatId) {
        return <h2>select a chat</h2>;
    }

    const { data } = useQuery({
        queryKey: ["chats", chatId],
        queryFn: () => fetch(`http://127.0.0.1:8000/chats/${chatId}/messages`).then((response) => response.json()),
    });

    if (data && data.messages) {
        return <MessagesListContainer messages={data.messages} />;
    }

    return <h2>loading...</h2>;
}

function MessagesListContainer({ messages }) {
    return (
        <div className="messages-card-container">
            <h2>Messages</h2>
            <MessagesList messages={messages}></MessagesList>
        </div>
    );
}

function MessagesList({ messages }) {
    return (
        <div className="messages-list">
            {messages.map((message) => (
                <MessageCard
                    message={message}
                    key={message.id}></MessageCard>
            ))}
        </div>
    );
}

function MessageCard({ message }) {
    return (
        <div className="message-list-item">
            <div className="column">
                <div className="row">
                    <div>{message.user_id}</div>
                    <div>{message.created_at}</div>
                </div>
                <div className="row">
                    <div>{message.text}</div>
                </div>
            </div>
        </div>
    );
}

export default MessagesQueryContainer;
