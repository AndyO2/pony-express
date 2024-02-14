/* eslint-disable react-hooks/rules-of-hooks */
/* eslint-disable react/prop-types */
import { useQuery } from "react-query";
import { Link, useParams } from "react-router-dom";
import MessagesQueryContainer from "./Messages";
import "./Chats.css";

function Chats() {
    const { chatId } = useParams();
    return (
        <div className="chats-page">
            <ChatListContainer></ChatListContainer>
            <MessagesQueryContainer
                className="chat-list-container"
                chatId={chatId}
            />
        </div>
    );
}

function ChatListContainer() {
    const { data } = useQuery({
        queryKey: ["chats"],
        queryFn: () => fetch("http://127.0.0.1:8000/chats").then((response) => response.json()),
    });

    if (data?.chats) {
        return (
            <div className="chat-list-container">
                <h2>pony express</h2>
                <ChatList chats={data.chats} />
            </div>
        );
    }

    return <h2>chat list</h2>;
}

function ChatList({ chats }) {
    return (
        <div className="chat-list">
            {chats.map((chat) => (
                <ChatListItem
                    key={chat.id}
                    chat={chat}
                />
            ))}
        </div>
    );
}

function ChatListItem({ chat }) {
    const createdAtDate = new Date(chat.created_at);

    // Format the date as "Month Day, Year"
    const formattedDate = createdAtDate.toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
    });

    return (
        <Link
            key={chat.id}
            to={`/chats/${chat.id}`}
            className="chat-list-item">
            <div className="chat-list-item-title">{chat.name}</div>
            <ul>
                {chat.user_ids.map((userId, index) => (
                    <li
                        className="chat-list-item-detail"
                        key={index}>
                        {userId}
                    </li>
                ))}
            </ul>
            <div className="chat-list-item-detail">created at: {formattedDate}</div>
        </Link>
    );
}

export default Chats;
