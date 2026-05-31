export const tasks = [
  {
    id: 1,
    title: "Write orchestration diagram",
    status: "done",
    dueDate: "2026-06-01",
    completed: true
  },
  {
    id: 2,
    title: "Add CSV export button",
    status: "in-progress",
    dueDate: "2026-06-07",
    completed: false
  },
  {
    id: 3,
    title: "Review scoped tools",
    status: "todo",
    dueDate: "2026-06-10",
    completed: false
  }
];

export function getTasks() {
  return tasks;
}
