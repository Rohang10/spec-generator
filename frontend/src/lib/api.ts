const API_BASE = process.env.NEXT_PUBLIC_API_URL;

export async function generateSpec(requirementsText: string) {
  const res = await fetch(`${API_BASE}/specs/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ requirements_text: requirementsText }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw data.detail || {
      status: res.status,
      code: "UNKNOWN_ERROR",
      message: "Something went wrong",
    };
  }

  return data;
}
export async function refineSpec(spec:unknown, instruction: string) {
  const res = await fetch(`${API_BASE}/specs/refine`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ spec,instruction }),
  });
  const data = await res.json();
  if (!res.ok) {
    throw data.detail || {
      status: res.status,
      code: "UNKNOWN_ERROR",
      message: "Something went wrong",
    };
  }
  return data;
}
