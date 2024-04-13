/* eslint-disable react-hooks/rules-of-hooks */
/* eslint-disable react/prop-types */
import "./Chats.css";
import LeftNav from "./LeftNav";
import Chat from './Chat';

function Chats () {
  return (
    <div className="flex flex-row h-screen w-full">
      <div className="w-40">
        <LeftNav />
      </div>
      <div className="w-auto pt-8">
        <Chat></Chat>
      </div>
    </div>
  );
}

export default Chats;
