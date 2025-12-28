export default function Spinner() {
  return (
    <div className="flex flex-col items-center justify-center py-16 gap-6">
      <div className="w-16 h-16 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin" />
      <p className="text-slate-400 text-lg">
        Preparing structured specification…
      </p>
    </div>
  );
}
