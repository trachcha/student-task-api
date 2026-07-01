import { useCallback, useEffect, useState, type FormEvent } from "react";
import { ApiError, api } from "../api/client";
import type { Subject, Task, TaskFilters } from "../api/types";
import SubjectPanel from "../subjects/SubjectPanel";
import SubtaskList from "../subtasks/SubtaskList";

type CompletedFilter = "all" | "active" | "completed";

export default function TaskListPage() {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [selectedSubjectId, setSelectedSubjectId] = useState<number | null>(null);
  const [completedFilter, setCompletedFilter] = useState<CompletedFilter>("all");
  const [search, setSearch] = useState("");
  const [newTitle, setNewTitle] = useState("");
  const [newSubjectId, setNewSubjectId] = useState<number | null>(null);
  const [expandedTaskId, setExpandedTaskId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadSubjects = useCallback(async () => {
    setSubjects(await api.listSubjects());
  }, []);

  const loadTasks = useCallback(async () => {
    const filters: TaskFilters = {};
    if (selectedSubjectId !== null) {
      filters.subject_id = selectedSubjectId;
    }
    if (completedFilter !== "all") {
      filters.completed = completedFilter === "completed";
    }
    if (search.trim()) {
      filters.q = search.trim();
    }
    try {
      setTasks(await api.listTasks(filters));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not load tasks");
    }
  }, [selectedSubjectId, completedFilter, search]);

  useEffect(() => {
    loadSubjects();
  }, [loadSubjects]);

  useEffect(() => {
    const handle = setTimeout(loadTasks, 200);
    return () => clearTimeout(handle);
  }, [loadTasks]);

  async function handleCreate(event: FormEvent) {
    event.preventDefault();
    if (!newTitle.trim()) {
      return;
    }
    setError(null);
    try {
      await api.createTask(newTitle.trim(), newSubjectId);
      setNewTitle("");
      setNewSubjectId(null);
      await loadTasks();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not create task");
    }
  }

  async function handleToggle(task: Task) {
    await api.updateTask(task.id, {
      title: task.title,
      completed: !task.completed,
      subject_id: task.subject_id,
    });
    await loadTasks();
  }

  async function handleSubjectChange(task: Task, subjectId: number | null) {
    await api.updateTask(task.id, {
      title: task.title,
      completed: task.completed,
      subject_id: subjectId,
    });
    await loadTasks();
  }

  async function handleRename(task: Task) {
    const title = prompt("Task title", task.title);
    if (title === null || !title.trim() || title.trim() === task.title) {
      return;
    }
    await api.updateTask(task.id, {
      title: title.trim(),
      completed: task.completed,
      subject_id: task.subject_id,
    });
    await loadTasks();
  }

  async function handleDelete(task: Task) {
    if (!confirm(`Delete task "${task.title}"?`)) {
      return;
    }
    await api.deleteTask(task.id);
    await loadTasks();
  }

  const subjectName = (id: number | null) =>
    subjects.find((s) => s.id === id)?.name ?? "No subject";

  return (
    <div className="task-layout">
      <SubjectPanel
        subjects={subjects}
        selectedSubjectId={selectedSubjectId}
        onSelect={setSelectedSubjectId}
        onChanged={() => {
          loadSubjects();
          loadTasks();
        }}
      />

      <section className="task-content">
        <form className="task-create" onSubmit={handleCreate}>
          <input
            type="text"
            placeholder="What needs doing?"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
          />
          <select
            value={newSubjectId ?? ""}
            onChange={(e) =>
              setNewSubjectId(e.target.value ? Number(e.target.value) : null)
            }
          >
            <option value="">No subject</option>
            {subjects.map((subject) => (
              <option key={subject.id} value={subject.id}>
                {subject.name}
              </option>
            ))}
          </select>
          <button type="submit">Add task</button>
        </form>

        <div className="task-filters">
          <input
            type="search"
            placeholder="Search titles..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <select
            value={completedFilter}
            onChange={(e) => setCompletedFilter(e.target.value as CompletedFilter)}
          >
            <option value="all">All</option>
            <option value="active">Active</option>
            <option value="completed">Completed</option>
          </select>
        </div>

        {error && <p className="error">{error}</p>}

        <ul className="task-list">
          {tasks.length === 0 && <li className="task-empty">No tasks found.</li>}
          {tasks.map((task) => (
            <li key={task.id} className="task-item">
              <div className="task-row">
                <label className="task-main">
                  <input
                    type="checkbox"
                    checked={task.completed}
                    onChange={() => handleToggle(task)}
                  />
                  <span className={task.completed ? "done" : ""}>
                    {task.title}
                  </span>
                </label>
                <div className="task-actions">
                  <select
                    value={task.subject_id ?? ""}
                    onChange={(e) =>
                      handleSubjectChange(
                        task,
                        e.target.value ? Number(e.target.value) : null,
                      )
                    }
                    title={subjectName(task.subject_id)}
                  >
                    <option value="">No subject</option>
                    {subjects.map((subject) => (
                      <option key={subject.id} value={subject.id}>
                        {subject.name}
                      </option>
                    ))}
                  </select>
                  <button
                    type="button"
                    onClick={() =>
                      setExpandedTaskId(
                        expandedTaskId === task.id ? null : task.id,
                      )
                    }
                  >
                    {expandedTaskId === task.id ? "Hide" : "Subtasks"}
                  </button>
                  <button type="button" onClick={() => handleRename(task)}>
                    Rename
                  </button>
                  <button
                    type="button"
                    className="danger"
                    onClick={() => handleDelete(task)}
                  >
                    Delete
                  </button>
                </div>
              </div>
              {expandedTaskId === task.id && <SubtaskList taskId={task.id} />}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
