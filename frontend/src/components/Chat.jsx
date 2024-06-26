/* eslint-disable no-unused-vars */
/* eslint-disable react/prop-types */
import { useQuery } from "react-query";
import { NavLink, useParams } from "react-router-dom";
import { useApi } from "../hooks";
import NewChat from "./NewChat";

function AttrRow ( { chat, attr } ) {
  const className = [
    "flex flex-row",
    "items-center justify-between",
    "border-b border-slate-500",
    "p-2",
  ].join( " " );

  const parseValue = ( chat, attr ) => {
    if ( attr === "intake_date" ) {
      return new Date( chat[ attr ] ).toDateString();
    } else if ( attr === "fixed" || attr === "vaccinated" ) {
      return chat[ attr ] ? "\u2713" : "\u2715";
    }
    return chat[ attr ].toString();
  }

  const parseAttr = ( attr ) => attr.split( "_" ).join( " " );

  return (
    <div className={ className }>
      <div className="font-mono text-sm text-slate-500">{ parseAttr( attr ) }:</div>
      <div>{ parseValue( chat, attr ) }</div>
    </div>
  )
}

function NoChat () {
  return (
    <div className="font-bold text-2xl py-4 text-center">
      loading...
    </div>
  );
}

function ChatCard ( { messages } ) {
  const cardClassName = [
    "bg-lgrn text-black",
    "border-2 border-slate-900",
    "shadow-md shadow-slate-900",
    "bg-slate-500",
    "mb-2"
  ].join( " " );

  return (
    <div className="flex flex-col">
      <h2 className="text-center text-2xl text-grn font-bold py-4">
        Messages
      </h2>
      <div>
        { messages.map( ( message ) => (
          <div className={ cardClassName } key={ message.id }>
            <div className="flex justify-content-space-between">{ message.user.username } on { new Date( message.created_at ).toLocaleDateString( "en-US", { year: "numeric", month: "long", day: "numeric" } ) }</div>
            <div>{ message.text }</div>
          </div>
        ) ) }
      </div>
      { messages.length > 0 && <NewChat></NewChat> }
    </div>
  )
}

function ChatCardQueryContainer ( { chatId } ) {
  const api = useApi();
  const { data } = useQuery( {
    queryKey: [ "chats", chatId ],
    queryFn: () => (
      api.get( `/chats/${ chatId }/messages` )
        .then( ( response ) => response.json() )
    ),
    enabled: chatId !== undefined,
  } );

  if ( data?.messages ) {
    return <ChatCard messages={ data.messages } />
  }

  return <NoChat />;
}

function Chat () {
  const { chatId } = useParams();

  if ( chatId ) {
    return (
      <ChatCardQueryContainer chatId={ chatId } />
    );
  }

  return <div>select a chat</div>
}

export default Chat;
