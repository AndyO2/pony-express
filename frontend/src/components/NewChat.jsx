/* eslint-disable no-unused-vars */
/* eslint-disable react/prop-types */
import { useState } from "react";
import { useMutation, useQueryClient } from "react-query";
import { useNavigate } from "react-router-dom";
import { useAuth, useApi } from "../hooks";
import { useParams } from "react-router-dom";
import Button from "./Button";

function Input ( props ) {
  return (
    <div className="flex flex-col py-2">
      <input
        placeholder="new message"
        { ...props }
        className="border rounded bg-transparent px-2 py-1"
      />
    </div>
  );
}

function NewChatForm () {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const { token } = useAuth();
  const api = useApi();
  const { chatId } = useParams();

  const [ message, setMessage ] = useState( "" );

  const mutation = useMutation( {
    mutationFn: () => (
      api.post(
        `/chats/${ chatId }/messages`,
        {
          token,
          chatId
        }
      ).then( ( response ) => response.json() )
    ),
    onSuccess: ( data ) => {
      queryClient.invalidateQueries( {
        queryKey: [ "chats" ],
      } );
      if ( data.detail.error ) {
        console.log( data.detail.error );
        navigate( `/chats/${ chatId }` );
      }
      else {
        console.log( 'success' );
        navigate( `/chats/${ data.message.chat_id }` );
      }
    },
    onError: () => {
      console.log( 'error' );
    }
  } );

  const onSubmit = ( e ) => {
    e.preventDefault();
    mutation.mutate();
  };

  return (
    <form className="flex items-center" onSubmit={ onSubmit }>
      <Input
        name="message"
        type="text"
        value={ message }
        onChange={ ( e ) => setMessage( e.target.value ) }
      />
      <Button type="submit">send</Button>
    </form>
  );
}

function NewChat () {
  return (
    <div className="w-96">
      <NewChatForm />
    </div>
  );
}

export default NewChat;
