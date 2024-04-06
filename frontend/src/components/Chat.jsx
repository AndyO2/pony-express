/* eslint-disable no-unused-vars */
/* eslint-disable react/prop-types */
import { useQuery } from "react-query";
import { NavLink, useParams } from "react-router-dom";
import { useApi } from "../hooks";
import NewChat from "./NewChat";

function AttrRow({ animal, attr }) {
  const className = [
    "flex flex-row",
    "items-center justify-between",
    "border-b border-slate-500",
    "p-2",
  ].join(" ");

  const parseValue = (animal, attr) => {
    if (attr === "intake_date") {
      return new Date(animal[attr]).toDateString();
    } else if (attr === "fixed" || attr === "vaccinated") {
      return animal[attr] ? "\u2713" : "\u2715";
    }
    return animal[attr].toString();
  }

  const parseAttr = (attr) => attr.split("_").join(" ");

  return (
    <div className={className}>
      <div className="font-mono text-sm text-slate-500">{parseAttr(attr)}:</div>
      <div>{parseValue(animal, attr)}</div>
    </div>
  )
}

function NoChat() {
  return (
    <div className="font-bold text-2xl py-4 text-center">
      loading...
    </div>
  );
}

function ChatCard({ animal }) {
  const attributes = [
    "kind",
    "age",
    "intake_date",
    "fixed",
    "vaccinated",
  ];

  const cardClassName = [
    "bg-lgrn text-black",
    "border-2 border-slate-900",
    "shadow-md shadow-slate-900",
  ].join(" ");

  return (
    <div className="flex flex-col w-64">
      <h2 className="text-center text-2xl text-grn font-bold py-4">
        {animal.name}
      </h2>
      <div className={cardClassName}>
        {attributes.map((attr) => (
          <AttrRow key={attr} animal={animal} attr={attr} />
        ))}
      </div>
    </div>
  )
}

function ChatCardQueryContainer({ chatId }) {
  const api = useApi();
  const { data } = useQuery({
    queryKey: ["chats", chatId],
    queryFn: () => (
      api.get(`/chats/${chatId}`)
        .then((response) => response.json())
    ),
    enabled: chatId !== undefined,
  });

  if (data?.chat) {
    return <ChatCard animal={data.animal} />
  }

  return <NoChat />;
}

function Chat() {
  const { animalId } = useParams();

  if (animalId) {
    return (
      <ChatCardQueryContainer animalId={animalId} />
    );
  }

  return <NewChat />;
}

export default Chat;
