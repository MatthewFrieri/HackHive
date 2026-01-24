const action_mapping = {
  F: "Fold",
  X: "Check",
  C: "Call",
  R: "Raise",
};

export default function FormatAction(action: string) {
  if (action == "") {
    return action;
  }
  const action_prefix = action[0] as keyof typeof action_mapping;
  const amount = action_prefix == "R" ? `: ${action.slice(1)}` : "";
  return `${action_mapping[action_prefix]}${amount}`;
}
