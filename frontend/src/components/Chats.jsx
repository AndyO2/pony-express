import { useQuery } from "react-query";
import { Link, useParams } from "react-router-dom";
import "./Chats.css";

// function AnimalListItem(chat) {
//     return (
//         <Link
//             key={chat.id}
//             to={`/animals/${chat.id}`}
//             className="animal-list-item">
//             <div className="animal-list-item-name">{animal.name}</div>
//             <div className="animal-list-item-detail">{animal.kind}</div>
//             <div className="animal-list-item-detail">{animal.age}</div>
//         </Link>
//     );
// }

// function AnimalList({ animals }) {
//     return (
//         <div className="animal-list">
//             {animals.map((animal) => (
//                 <AnimalListItem
//                     key={animal.id}
//                     chat={animal}
//                 />
//             ))}
//         </div>
//     );
// }

// function AnimalListContainer() {
//     const { data } = useQuery({
//         queryKey: ["animals"],
//         queryFn: () => fetch("http://127.0.0.1:8000/animals").then((response) => response.json()),
//     });

//     if (data?.animals) {
//         return (
//             <div className="animal-list-container">
//                 <h2>animals</h2>
//                 <AnimalList animals={data.animals} />
//             </div>
//         );
//     }

//     return <h2>animal list</h2>;
// }

function Chats() {
    const { chatID } = useParams();
    return (
        <div className="animals-page">
            <h1>Chats Page {chatID}</h1>
            <div>
                <div>Column 1</div>
                <div>Column 2</div>
            </div>
        </div>
    );
}

export default Chats;
