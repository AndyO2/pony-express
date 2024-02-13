/* eslint-disable react/prop-types */
import { useQuery } from "react-query";
import { Link, useParams } from "react-router-dom";
import "./Chats.css";

function ChatListItem({ chat }) {
    return (
        <Link
            key={chat.id}
            to={`/chats/${chat.id}`}
            className="chat-list-item"></Link>
    );
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

function ChatCard({ chat }) {
    const attributes = ["kind", "age", "intake_date", "fixed", "vaccinated"];

    return (
        <div className="chat-card">
            {attributes.map((attr) => (
                <div
                    key={attr}
                    className="chat-card-attr">
                    {attr}: {chat[attr].toString()}
                </div>
            ))}
        </div>
    );
}

function ChatCardContainer({ chat }) {
    return (
        <div className="animal-card-container">
            <h2>{chat.name}</h2>
            <ChatCard animal={chat} />
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
                <h2>chats</h2>
                <ChatList chats={data.chats} />
            </div>
        );
    }

    return <h2>chat list</h2>;
}

function ChatCardQueryContainer({ chatId }) {
    if (!chatId) {
        return <h2>pick a chat</h2>;
    }

    // eslint-disable-next-line react-hooks/rules-of-hooks
    const { data } = useQuery({
        queryKey: ["chats", chatId],
        queryFn: () => fetch(`http://127.0.0.1:8000/chats/${chatId.id}`).then((response) => response.json()),
    });

    if (data && data.chat) {
        return <ChatCardContainer chat={data.chat} />;
    }

    return <h2>loading...</h2>;
}

function Chats() {
    const { chatID } = useParams();
    return (
        <div className="chats-page">
            <ChatListContainer></ChatListContainer>
            <ChatCardQueryContainer chatID={chatID}></ChatCardQueryContainer>
        </div>
    );
}

export default Chats;
