export default function TypingIndicator() {
  return (
    <svg
      width="30"
      height="10"
      viewBox="0 0 120 30"
      xmlns="http://www.w3.org/2000/svg"
      fill="currentColor"
      className="opacity-70"
    >
      <circle cx="15" cy="15" r="15">
        <animate
          attributeName="opacity"
          values="0;1;0"
          dur="1s"
          repeatCount="indefinite"
        />
      </circle>
      <circle cx="60" cy="15" r="15">
        <animate
          attributeName="opacity"
          values="0;1;0"
          dur="1s"
          begin="0.2s"
          repeatCount="indefinite"
        />
      </circle>
      <circle cx="105" cy="15" r="15">
        <animate
          attributeName="opacity"
          values="0;1;0"
          dur="1s"
          begin="0.4s"
          repeatCount="indefinite"
        />
      </circle>
    </svg>
  );
}
