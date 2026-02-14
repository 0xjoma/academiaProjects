import React, { useState, useEffect } from "react";
import * as d3 from "d3";

const GanttChart = () => {
  const [hoveredTask, setHoveredTask] = useState(null);

  const tasks = [
    {
      id: 1,
      name: "Project Part 1",
      description: "Risk Management Plan Outline and Research",
      start: new Date(2025, 5, 23), // June 23, 2025
      end: new Date(2025, 5, 28), // June 28, 2025
      color: "#3B82F6",
    },
    {
      id: 2,
      name: "Project Part 2",
      description: "Risk Assessment Plan",
      start: new Date(2025, 5, 28), // June 28, 2025
      end: new Date(2025, 6, 12), // July 12, 2025
      color: "#10B981",
    },
    {
      id: 3,
      name: "Project Part 3",
      description: "Risk Mitigation Plan",
      start: new Date(2025, 6, 12), // July 12, 2025
      end: new Date(2025, 6, 19), // July 19, 2025
      color: "#F59E0B",
    },
    {
      id: 4,
      name: "Project Part 4",
      description:
        "Business Impact Analysis (BIA) and Business Continuity Plan (BCP)",
      start: new Date(2025, 6, 19), // July 19, 2025
      end: new Date(2025, 7, 4), // August 4, 2025
      color: "#EF4444",
    },
    {
      id: 5,
      name: "Project Part 5",
      description: "Final Risk Management Plan",
      start: new Date(2025, 7, 4), // August 4, 2025
      end: new Date(2025, 7, 9), // August 9, 2025
      color: "#8B5CF6",
    },
  ];

  // Calculate project timeline
  const projectStart = d3.min(tasks, (d) => d.start);
  const projectEnd = d3.max(tasks, (d) => d.end);
  const totalDuration = Math.ceil(
    (projectEnd - projectStart) / (1000 * 60 * 60 * 24)
  );

  // Format date for display
  const formatDate = (date) => {
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  // Calculate task duration in days
  const getDuration = (task) => {
    return Math.ceil((task.end - task.start) / (1000 * 60 * 60 * 24));
  };

  // Calculate task position and width
  const getTaskPosition = (task) => {
    const startOffset = Math.ceil(
      (task.start - projectStart) / (1000 * 60 * 60 * 24)
    );
    const duration = getDuration(task);
    const left = (startOffset / totalDuration) * 100;
    const width = (duration / totalDuration) * 100;
    return { left: `${left}%`, width: `${width}%` };
  };

  // Generate timeline markers
  const getTimelineMarkers = () => {
    const markers = [];
    const current = new Date(projectStart);

    while (current <= projectEnd) {
      markers.push(new Date(current));
      current.setDate(current.getDate() + 7); // Weekly markers
    }

    return markers;
  };

  const timelineMarkers = getTimelineMarkers();

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-white mb-2">
            Risk Management Project Timeline
          </h1>
          <p className="text-gray-400">
            {formatDate(projectStart)} - {formatDate(projectEnd)} (
            {totalDuration} days)
          </p>
        </div>

        <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-8 shadow-2xl border border-gray-700">
          {/* Timeline Header */}
          <div className="relative mb-4 pb-4 border-b border-gray-700">
            <div className="flex justify-between text-xs text-gray-400">
              {timelineMarkers.map((date, index) => (
                <div
                  key={index}
                  className="absolute transform -translate-x-1/2"
                  style={{
                    left: `${(index / (timelineMarkers.length - 1)) * 100}%`,
                  }}
                >
                  <div className="whitespace-nowrap">
                    {date.toLocaleDateString("en-US", {
                      month: "short",
                      day: "numeric",
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Gantt Bars */}
          <div className="space-y-6 mt-16">
            {tasks.map((task, index) => {
              const position = getTaskPosition(task);
              const isHovered = hoveredTask === task.id;

              return (
                <div key={task.id} className="relative">
                  {/* Task Label */}
                  <div className="mb-2">
                    <h3 className="text-white font-semibold">{task.name}</h3>
                    <p className="text-gray-400 text-sm">{task.description}</p>
                  </div>

                  {/* Task Bar Container */}
                  <div className="relative h-12 bg-gray-700/30 rounded-lg overflow-hidden">
                    {/* Task Bar */}
                    <div
                      className={`absolute h-full rounded-lg transition-all duration-300 cursor-pointer ${
                        isHovered ? "shadow-lg transform scale-y-110" : ""
                      }`}
                      style={{
                        backgroundColor: task.color,
                        left: position.left,
                        width: position.width,
                        opacity: isHovered ? 1 : 0.9,
                      }}
                      onMouseEnter={() => setHoveredTask(task.id)}
                      onMouseLeave={() => setHoveredTask(null)}
                    >
                      <div className="h-full flex items-center px-3">
                        <span className="text-white text-sm font-medium whitespace-nowrap">
                          {getDuration(task)} days
                        </span>
                      </div>
                    </div>

                    {/* Dependency Lines */}
                    {index > 0 && (
                      <div
                        className="absolute h-0.5 bg-gray-500/50 top-1/2 transform -translate-y-1/2"
                        style={{
                          left: getTaskPosition(tasks[index - 1]).left,
                          width: `calc(${position.left} - ${
                            getTaskPosition(tasks[index - 1]).left
                          })`,
                        }}
                      />
                    )}
                  </div>

                  {/* Hover Info */}
                  {isHovered && (
                    <div className="absolute z-10 mt-2 p-3 bg-gray-900 rounded-lg shadow-xl border border-gray-600 text-sm">
                      <div className="text-white font-semibold">
                        {task.description}
                      </div>
                      <div className="text-gray-400 mt-1">
                        {formatDate(task.start)} - {formatDate(task.end)}
                      </div>
                      <div className="text-gray-400">
                        Duration: {getDuration(task)} days
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Legend */}
          <div className="mt-8 pt-6 border-t border-gray-700">
            <h3 className="text-white font-semibold mb-3">Project Phases</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {tasks.map((task) => (
                <div key={task.id} className="flex items-center space-x-2">
                  <div
                    className="w-4 h-4 rounded"
                    style={{ backgroundColor: task.color }}
                  />
                  <span className="text-gray-400 text-sm">{task.name}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Summary Statistics */}
          <div className="mt-6 grid grid-cols-3 gap-4 text-center">
            <div className="bg-gray-700/30 rounded-lg p-4">
              <div className="text-2xl font-bold text-white">
                {tasks.length}
              </div>
              <div className="text-gray-400 text-sm">Total Phases</div>
            </div>
            <div className="bg-gray-700/30 rounded-lg p-4">
              <div className="text-2xl font-bold text-white">
                {totalDuration}
              </div>
              <div className="text-gray-400 text-sm">Total Days</div>
            </div>
            <div className="bg-gray-700/30 rounded-lg p-4">
              <div className="text-2xl font-bold text-white">
                {Math.ceil(totalDuration / 7)}
              </div>
              <div className="text-gray-400 text-sm">Total Weeks</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GanttChart;
