import { useState, type FormEvent } from "react";
import { ApiError, api } from "../api/client";
import type { Subject } from "../api/types";

interface SubjectPanelProps {
  subjects: Subject[];
  selectedSubjectId: number | null;
  onSelect: (subjectId: number | null) => void;
  onChanged: () => void;
}

export default function SubjectPanel({
  subjects,
  selectedSubjectId,
  onSelect,
  onChanged,
}: SubjectPanelProps) {
  const [name, setName] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function handleAdd(event: FormEvent) {
    event.preventDefault();
    if (!name.trim()) {
      return;
    }
    setError(null);
    try {
      await api.createSubject(name.trim());
      setName("");
      onChanged();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not add subject");
    }
  }

  async function handleDelete(subject: Subject) {
    if (!confirm(`Delete subject "${subject.name}"? Its tasks are kept.`)) {
      return;
    }
    await api.deleteSubject(subject.id);
    if (selectedSubjectId === subject.id) {
      onSelect(null);
    }
    onChanged();
  }

  return (
    <aside className="subject-panel">
      <h2>Subjects</h2>
      <ul className="subject-list">
        <li>
          <button
            type="button"
            className={selectedSubjectId === null ? "active" : ""}
            onClick={() => onSelect(null)}
          >
            All tasks
          </button>
        </li>
        {subjects.map((subject) => (
          <li key={subject.id}>
            <button
              type="button"
              className={selectedSubjectId === subject.id ? "active" : ""}
              onClick={() => onSelect(subject.id)}
            >
              {subject.name}
            </button>
            <button
              type="button"
              className="icon-button"
              title="Delete subject"
              onClick={() => handleDelete(subject)}
            >
              x
            </button>
          </li>
        ))}
      </ul>

      <form className="subject-form" onSubmit={handleAdd}>
        <input
          type="text"
          placeholder="New subject"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <button type="submit">Add</button>
      </form>
      {error && <p className="error">{error}</p>}
    </aside>
  );
}
