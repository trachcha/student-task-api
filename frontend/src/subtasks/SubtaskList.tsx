import { useEffect, useRef, useState, type FormEvent } from "react";
import { api } from "../api/client";
import type { Subtask } from "../api/types";

interface SubtaskListProps {
  taskId: number;
  parentCompleted: boolean;
}

export default function SubtaskList({ taskId, parentCompleted }: SubtaskListProps) {
  const [subtasks, setSubtasks] = useState<Subtask[]>([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(true);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editingTitle, setEditingTitle] = useState("");

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

  const prevParent = useRef(parentCompleted);
  useEffect(() => {
    if (parentCompleted && !prevParent.current) {
      setSubtasks((prev) => prev.map((s) => ({ ...s, completed: true })));
    }
    prevParent.current = parentCompleted;
  }, [parentCompleted]);

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

  function startEdit(subtask: Subtask) {
    setEditingId(subtask.id);
    setEditingTitle(subtask.title);
  }

  function cancelEdit() {
    setEditingId(null);
    setEditingTitle("");
  }

  async function saveEdit(subtask: Subtask) {
    const newTitle = editingTitle.trim();
    if (!newTitle || newTitle === subtask.title) {
      cancelEdit();
      return;
    }
    await api.updateSubtask(taskId, subtask.id, {
      title: newTitle,
      completed: subtask.completed,
    });
    cancelEdit();
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
            {editingId === subtask.id ? (
              <div className="subtask-edit">
                <input
                  type="text"
                  autoFocus
                  value={editingTitle}
                  onChange={(e) => setEditingTitle(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") saveEdit(subtask);
                    if (e.key === "Escape") cancelEdit();
                  }}
                />
                <button type="button" onClick={() => saveEdit(subtask)}>
                  Save
                </button>
                <button type="button" onClick={cancelEdit}>
                  Cancel
                </button>
              </div>
            ) : (
              <>
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
                <div className="subtask-actions">
                  <button type="button" onClick={() => startEdit(subtask)}>
                    Rename
                  </button>
                  <button
                    type="button"
                    className="icon-button"
                    onClick={() => handleDelete(subtask.id)}
                  >
                    x
                  </button>
                </div>
              </>
            )}
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
