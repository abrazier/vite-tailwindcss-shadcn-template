import React from "react";
import TaskList from "@/features/tasks/TaskList";
import TaskForm from "@/features/tasks/TaskForm";

const Home: React.FC = () => {
  return (
    <div className="max-w-xl mx-auto py-8">
      <h1 className="text-2xl font-bold mb-4">Task Manager</h1>
      <TaskForm />
      <div className="my-6" />
      <TaskList />
    </div>
  );
};

export default Home;
