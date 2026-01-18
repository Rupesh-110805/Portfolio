import type { Express } from "express";
import type { Server } from "http";
import { storage } from "./storage";
import { api } from "@shared/routes";
import { z } from "zod";
import { projects, skills } from "@shared/schema";
import { db } from "./db";

export async function registerRoutes(
  httpServer: Server,
  app: Express
): Promise<Server> {
  // Projects
  app.get(api.projects.list.path, async (req, res) => {
    const projects = await storage.getProjects();
    res.json(projects);
  });

  app.post(api.projects.create.path, async (req, res) => {
    try {
      const input = api.projects.create.input.parse(req.body);
      const project = await storage.createProject(input);
      res.status(201).json(project);
    } catch (err) {
      if (err instanceof z.ZodError) {
        return res.status(400).json({ message: err.errors[0].message });
      }
      throw err;
    }
  });

  // Skills
  app.get(api.skills.list.path, async (req, res) => {
    const skills = await storage.getSkills();
    res.json(skills);
  });

  // Messages
  app.post(api.messages.create.path, async (req, res) => {
    try {
      const input = api.messages.create.input.parse(req.body);
      const message = await storage.createMessage(input);
      res.status(201).json(message);
    } catch (err) {
      if (err instanceof z.ZodError) {
        return res.status(400).json({ message: err.errors[0].message });
      }
      throw err;
    }
  });

  // Seed data if empty
  await seedDatabase();

  return httpServer;
}

async function seedDatabase() {
  const existingProjects = await storage.getProjects();
  if (existingProjects.length === 0) {
    await db.insert(projects).values([
      {
        title: "Django Chat App",
        description: "A real-time chat application with WebSockets, Docker, and PostgreSQL. Features Google OAuth, live user status, emoji reactions, and admin moderation.",
        techStack: ["Django", "Django Channels", "WebSockets", "Docker", "PostgreSQL", "Redis"],
        githubLink: "https://github.com/Rupesh-110805/Django-Chat-App",
        imageUrl: "https://images.unsplash.com/photo-1611746435392-5021db4c2411?auto=format&fit=crop&q=80&w=1000",
      },
      {
        title: "DDoS Attack Detector",
        description: "Real-time DDoS detection system using Shannon's entropy analysis of network traffic, achieving over 90% accuracy. Features a live visualization dashboard.",
        techStack: ["Flask", "Flask-SocketIO", "Chart.js", "Bootstrap", "Python"],
        githubLink: "https://github.com/Rupesh-110805/DDoS-Attack-Detector-Entropy-Based-",
        imageUrl: "https://images.unsplash.com/photo-1558494949-ef2bb6db8744?auto=format&fit=crop&q=80&w=1000",
      }
    ]);
  }

  const existingSkills = await storage.getSkills();
  if (existingSkills.length === 0) {
    await db.insert(skills).values([
      // Languages
      { name: "C++", category: "Languages" },
      { name: "Python", category: "Languages" },
      { name: "SQL", category: "Languages" },
      { name: "JavaScript", category: "Languages" },
      
      // Web Development
      { name: "React", category: "Frameworks" },
      { name: "Django", category: "Frameworks" },
      { name: "FastAPI", category: "Frameworks" },
      { name: "Flask", category: "Frameworks" },

      // Tools
      { name: "Linux", category: "Tools" },
      { name: "Docker", category: "Tools" },
      { name: "Git/GitHub", category: "Tools" },
      { name: "GitHub Actions", category: "Tools" },
      { name: "PostgreSQL", category: "Tools" },
      { name: "Redis", category: "Tools" },
    ]);
  }
}
