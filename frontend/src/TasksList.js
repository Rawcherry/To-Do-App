import React, { useState, useEffect } from 'react';

const API_BASE_URL = '/api/tasks';

function TasksList() {
  const [tasks, setTasks] = useState([]);
  const [newTaskText, setNewTaskText] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // loading list of task while mounting 
  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    setLoading(true);
    try {
      const response = await fetch(API_BASE_URL);
      if (!response.ok) {
        throw new Error('error while loading task');
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
      if (!response.ok) throw new Error('error while adding task');
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
        throw new Error('task was not deleted');
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
      if (!response.ok) throw new Error('error while loading task list');
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
      if (!response.ok) throw new Error('error while patching tasks');
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
      {/* central block  */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          width: '100%',
          marginBottom: '25px',
        }}
      >
        <input
          type="text"
          placeholder="Введите новую задачу..."
          value={newTaskText}
          onChange={(e) => setNewTaskText(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleAddTask()}
          style={{
            flex: 1,
            padding: '12px 20px',
            border: '2px solid #ccc',
            borderRadius: '10px',
            fontSize: '1em',
          }}
        />
        <button
          onClick={handleAddTask}
          style={{
            marginLeft: '15px',
            padding: '14px 25px',
            backgroundColor: '#ff6347',
            color: '#fff',
            border: 'none',
            borderRadius: '10px',cursor: 'pointer',
            fontSize: '1em',
            transition: 'background-color 0.2s, transform 0.1s',
          }}
          onMouseOver={(e) => (e.target.style.backgroundColor = '#ff3b2e')}
          onMouseOut={(e) => (e.target.style.backgroundColor = '#ff6347')}
        >
          Добавить
        </button>
      </div>

      {/* list of tasks*/}
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
              style={{
                textDecoration: task.done ? 'line-through' : 'none',
                marginLeft: '10px',
                padding: '8px',
                border: '1px solid #ccc',
                borderRadius: '4px',
                width: '60%',
              }}
            />
            <button
              onClick={() => handleDelete(task.id)}
              style={{
                marginLeft: '10px',
                padding: '8px 12px',
                borderRadius: '4px',
                border: 'none',
                backgroundColor: '#f44336',
                color: '#fff',
                cursor: 'pointer',
                transition: 'background-color 0.2s',
              }}
              onMouseOver={(e) => (e.target.style.backgroundColor = '#d32f2f')}
              onMouseOut={(e) => (e.target.style.backgroundColor = '#f44336')}
            >
              Удалить
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TasksList;
