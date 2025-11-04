import { useState } from "react";

interface PromptAreaProps {
  placeholder: string;
}

function PromptArea({placeholder}: PromptAreaProps) {
  const [inputValue, setInputValue] = useState('');
  function handleInput(event) {
    setInputValue(event.target.innerText);
  }
  const classSpan:string = `whitespace-pre-wrap outline-none
                            cursor-text after:text-gray-500
                            pointer-events-auto`;
  return (
    <div
      id="prompt-text-area"
      className="w-90 min-h-10 whitespace-pre-wrap
      break-words resize-none overflow-y-auto outline-none
      border-1 border-solid rounded-sm px-2 py-2"
    >
      <span
        className={
          (inputValue.trim().length <= 0)
            ? `${classSpan} placeholder`
            : classSpan
        }
        contentEditable
        onInput={handleInput}
        data-placeholder={placeholder}
        tabIndex={0}
      >
      </span>
    </div>
  );
}

export function ChatHeader() {
  return (
    <div className="flex mx-auto px-4">
      <p class="text-lg"><a href='/'>Diagene</a></p>
    </div>
  );
}

export function ChatWindow() {
  return (
    <div className="flex mx-auto px-4 flex-col">
      <div className="flex justify-center min-h-50">
        <div className="flex mb-16 mt-16">
          <p className="text-2xl text-center">
            How can I help you today?
          </p>
        </div>
      </div>
      <div className="flex justify-center min-w-50">
        <div className="flex">
          <PromptArea placeholder="What is troubling you right now?"/>
        </div>
      </div>
    </div>
  );
}

