import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { Skill } from "@/types";

export function useSkills() {
  return useQuery<Skill[]>({
    queryKey: ["skills"],
    queryFn: async () => {
      const res = await fetch(api.skills.list.path);
      if (!res.ok) throw new Error("Failed to fetch skills");
      return res.json();
    },
  });
}
