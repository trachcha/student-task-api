import { useEffect, useState, type FormEvent } from "react";
import { api } from "../api/client";
import type { Subtask } from "../api/types";

export default function SubtaskList({ taskId }: { taskId: number }) {
  const [subtasks, setSubtasks] = useState<Subtask[]>([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(true);

  async function refresh() {
    setSubtasks(await api.listSubtasks(taskId));
  }

  useEffect(() => {
    let active = true;
    api
      .listSubtasks(taskId)
      .then((data) => {
        if (active) {
          setSubtasks(data);
        }
      })
      .finally(() => {
        if (active) {
          setLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, [taskId]);

  async function handleAdd(event: FormEvent) {
    event.preventDefault();
    if (!title.trim()) {
      return;
    }
    await api.createSubtask(taskId, title.trim());
    setTitle("");
    await refresh();
  }

  async function handleToggle(subtask: Subtask) {
    await api.updateSubtask(taskId, subtask.id, {
      title: subtask.title,
      completed: !subtask.completed,
    });
    await refresh();
  }

  async function handleDelete(subtaskId: number) {
    await api.deleteSubtask(taskId, subtaskId);
    await refresh();
  }

  if (loading) {
    return <p className="subtask-empty">Loading subtasks...</p>;
  }

  return (
    <div className="subtasks">
      {subtasks.length === 0 && <p className="subtask-empty">No subtasks yet.</p>}
      <ul>
        {subtasks.map((subtask) => (
          <li key={subtask.id}>
            <label>
              <input
                type="checkbox"
                checked={subtask.completed}
                onChange={() => handleToggle(subtask)}
              />
              <span className={subtask.completed ? "done" : ""}>
                {subtask.title}
              </span>
            </label>
            <button
              type="button"
              className="icon-button"
              onClick={() => handleDelete(subtask.id)}
            >
              x
            </button>
          </li>
        ))}
      </ul>
      <form className="subtask-form" onSubmit={handleAdd}>
        <input
          type="text"
          placeholder="Add a subtask"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <button type="submit">Add</button>
      </form>
    </div>
  );
}
