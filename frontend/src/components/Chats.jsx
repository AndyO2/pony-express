/* eslint-disable react-hooks/rules-of-hooks */
/* eslint-disable react/prop-types */
import { useParams } from "react-router-dom";
import "./Chats.css";
import LeftNav from "./LeftNav";

function Chats() {
    const { chatId } = useParams();
    return (
    <div className="flex flex-row h-screen w-screen">
      <div className="w-40">
        <LeftNav />
      </div>
      <div className="mx-auto pt-8">
                
      </div>
    </div>
    );
}

// function ChatListContainer() {
//     const { data } = useQuery({
//         queryKey: ["chats"],
//         queryFn: () => fetch("http://127.0.0.1:8000/chats").then((response) => response.json()),
//     });

//     if (data?.chats) {
//         return (
//             <div className="chat-list-container">
//                 <h2>pony express</h2>
//                 <ChatList chats={data.chats} />
//             </div>
//         );
//     }

//     return <h2>chat list</h2>;
// }

// function ChatList ( { chats } ) {

//     return (
//         <div className="chat-list">
//             {chats?.map((chat) => (
//                 <ChatListItem
//                     key={chat.id}
//                     chat={chat}
//                 />
//             ))}
//         </div>
//     );
// }

// function ChatListItem({ chat }) {
//     const createdAtDate = new Date(chat.created_at);

//     // Format the date as "Month Day, Year"
//     const formattedDate = createdAtDate.toLocaleDateString("en-US", {
//         year: "numeric",
//         month: "long",
//         day: "numeric",
//     });

//     return (
//         <Link
//             key={chat.id}
//             to={`/chats/${chat.id}`}
//             className="chat-list-item">
//             <div className="chat-list-item-title">{chat.name}</div>
//             <ul>
//                 {chat.user_ids.map((userId, index) => (
//                     <li
//                         className="chat-list-item-detail"
//                         key={index}>
//                         {userId}
//                     </li>
//                 ))}
//             </ul>
//             <div className="chat-list-item-detail">created at: {formattedDate}</div>
//         </Link>
//     );
// }

export default Chats;
