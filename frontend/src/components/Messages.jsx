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
            <h2>messages</h2>
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
    const createdAtDate = new Date(message.created_at);

    // Format the date as "Month Day, Year"
    const formattedDate = createdAtDate.toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "numeric",
        minute: "numeric",
    });
    return (
        <div className="message-list-item">
            <div className="column">
                <div className="row">
                    <div className="chat-user">{message.user_id}</div>
                    <div className="chat-date">{formattedDate}</div>
                </div>
                <div className="row">
                    <div>{message.text}</div>
                </div>
            </div>
        </div>
    );
}

export default MessagesQueryContainer;
