import React, { useState, useEffect } from 'react';

const API_BASE_URL = '/api/tasks';

function TasksList() {
  const [tasks, setTasks] = useState([]);
  const [newTaskText, setNewTaskText] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Загружаем список задач при монтировании компонента
  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    setLoading(true);
    try {
      const response = await fetch(API_BASE_URL);
      if (!response.ok) {
        throw new Error('Ошибка при загрузке задач');
      }
      const data = await response.json();
      setTasks(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async () => {
    if (!newTaskText.trim()) return;
    try {
      const response = await fetch(API_BASE_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: newTaskText }),
      });
      if (!response.ok) throw new Error('Ошибка при добавлении задачи');
      const newTask = await response.json();
      setTasks([...tasks, newTask]);
      setNewTaskText('');
    } catch (err) {
      alert(err.message);
    }
  };

  const handleDelete = async (id) => {
    try {
      const response = await fetch(`${API_BASE_URL}/${id}`, {
        method: 'DELETE',
      });
      if (response.status === 204) {
        setTasks(tasks.filter((task) => task.id !== id));
      } else {
        throw new Error('Задача не удалена');
      }
    } catch (err) {
      alert(err.message);
    }
  };

  const handleToggleDone = async (task) => {
    const updatedDoneStatus = !task.done;
    try {
      const response = await fetch(`${API_BASE_URL}/${task.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ done: updatedDoneStatus }),
      });
      if (!response.ok) throw new Error('Ошибка при обновлении задачи');
      const updatedTask = await response.json();
      setTasks(tasks.map((t) => (t.id === task.id ? updatedTask : t)));
    } catch (err) {
      alert(err.message);
    }
  };

  const handleUpdateText = async (task, newText) => {
    try {
      const response = await fetch(`${API_BASE_URL}/${task.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: newText }),
      });
      if (!response.ok) throw new Error('Ошибка при обновлении задачи');
      const updatedTask = await response.json();
      setTasks(tasks.map((t) => (t.id === task.id ? updatedTask : t)));
    } catch (err) {
      alert(err.message);
    }
  };

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div>Ошибка: {error}</div>;

  return (
    <div>
      <h2>Список задач</h2>
      <div className="new-task-controls">
  <input
    type="text"
    placeholder="Введите новую задачу..."
    value={newTaskText}
    onChange={(e) => setNewTaskText(e.target.value)}
    onKeyDown={(e) => e.key === 'Enter' && handleAddTask()}
  />
  <button onClick={handleAddTask}>Добавить</button>
</div>

      <ul>
        {tasks.map((task) => (
          <li key={task.id} style={{ marginBottom: '10px' }}>
            <input
              type="checkbox"
              checked={task.done}
              onChange={() => handleToggleDone(task)}
            />
            <input
              type="text"
              value={task.text}
              onChange={(e) => handleUpdateText(task, e.target.value)}
              style={{ textDecoration: task.done ? 'line-through' : 'none' }}
            />
            <button onClick={() => handleDelete(task.id)} style={{ marginLeft: '10px' }}>
              Удалить
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TasksList;