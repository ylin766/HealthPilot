export default function ImagePlayer() {
  return (
    <div className="w-full flex flex-col items-center gap-2 p-4">
      <h2 className="text-base font-semibold mb-2">{props.title}</h2>
      {props.imageUrl && (
        <img
          src={props.imageUrl}
          alt="Image Preview"
          className="rounded-lg max-w-full h-auto shadow-md"
        />
      )}
      {props.note && (
        <div
          className="text-sm text-center max-w-md"
          style={{ color: "hsl(var(--foreground))" }}
        >
          {props.note}
        </div>
      )}
    </div>
  );
}
