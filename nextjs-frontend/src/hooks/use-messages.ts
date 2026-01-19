import { useMutation } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { MessageCreate } from "@/types";

export function useSendMessage() {
  return useMutation({
    mutationFn: async (data: MessageCreate) => {
      const res = await fetch(api.messages.create.path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) {
        if (res.status === 400 || res.status === 422) {
          const error = await res.json();
          throw new Error(error.message || error.detail || "Validation error");
        }
        throw new Error("Failed to send message");
      }
      return res.json();
    },
  });
}
