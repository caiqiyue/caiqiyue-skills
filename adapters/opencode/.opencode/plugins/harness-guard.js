export const HarnessGuard = async () => {
  return {
    event: async ({ event }) => {
      if (event?.type === "session.created") {
        console.log("[personal-harness] Enforce one active feature and verified completion.")
      }
    },
  }
}
