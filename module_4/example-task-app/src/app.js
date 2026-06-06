import { getTasks } from "./tasks.js";

export function renderTaskList(root = document.getElementById("task-list")) {
  if (!root) {
    return;
  }

  root.innerHTML = "";

  for (const task of getTasks()) {
    const item = document.createElement("li");
    item.dataset.taskId = String(task.id);
    item.textContent = `${task.title} - ${task.status}`;
    root.appendChild(item);
  }
}

renderTaskList();
