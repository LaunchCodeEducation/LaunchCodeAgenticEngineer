import assert from "node:assert/strict";
import { test } from "node:test";
import { getTasks } from "../src/tasks.js";

test("starter task data contains visible tasks", () => {
  const tasks = getTasks();

  assert.ok(Array.isArray(tasks));
  assert.ok(tasks.length >= 1);
  assert.ok(tasks.every((task) => typeof task.id === "number"));
  assert.ok(tasks.every((task) => typeof task.title === "string"));
});

test("task data includes fields required by the CSV PRD", () => {
  const [task] = getTasks();

  assert.deepEqual(Object.keys(task), [
    "id",
    "title",
    "status",
    "dueDate",
    "completed"
  ]);
});
