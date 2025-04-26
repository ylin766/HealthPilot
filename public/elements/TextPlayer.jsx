export default function TextPlayer() {
    return (
      <div className="p-4 max-w-md text-white text-sm">
        <h2 className="text-base font-semibold mb-2">{props.title}</h2>
        <p className="whitespace-pre-line">{props.content}</p>
      </div>
    );
  }
  