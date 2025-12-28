import ThemeToggle from "./ThemeToggle";

export default function Header() {
  return (
    <div className="flex justify-between items-center mb-8">
      <h1 className="text-3xl font-bold bg-linear-to-r from-indigo-400 to-purple-500 bg-clip-text text-transparent">
        AI Spec Generator
      </h1>
      <ThemeToggle />
    </div>
  );
}
